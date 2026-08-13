use crate::breaker::Decision;
use crate::state::{AppState, Rotation};
use axum::body::Body;
use axum::extract::{Path, State};
use axum::http::{HeaderMap, HeaderName, Method, StatusCode, Uri};
use axum::response::{IntoResponse, Response};
use std::sync::Arc;
use tracing::{error, info, warn};

fn is_hop_by_hop(name: &HeaderName) -> bool {
    matches!(
        name.as_str(),
        "connection"
            | "keep-alive"
            | "proxy-authenticate"
            | "proxy-authorization"
            | "te"
            | "trailer"
            | "transfer-encoding"
            | "upgrade"
    )
}

fn json_error(status: StatusCode, code: &str, message: &str) -> Response {
    (
        status,
        axum::Json(serde_json::json!({ "error": code, "message": message })),
    )
        .into_response()
}

/// Convert an upstream response into a streaming client response — O(chunk),
/// bodies are never fully buffered on the response path.
fn upstream_response(resp: reqwest::Response) -> Response {
    let status = resp.status();
    let headers = resp.headers().clone();
    let stream = resp.bytes_stream();
    let mut builder = Response::builder().status(status.as_u16());
    for (name, value) in headers.iter() {
        if !is_hop_by_hop(name) && name != http::header::CONTENT_LENGTH {
            builder = builder.header(name, value);
        }
    }
    builder
        .body(Body::from_stream(stream))
        .unwrap_or_else(|_| {
            json_error(
                StatusCode::BAD_GATEWAY,
                "response_build_failed",
                "failed to build upstream response",
            )
        })
}

fn emit_rotation(state: &AppState, provider: &str, rotation: &Rotation) {
    warn!(
        provider = provider,
        from_key_env = %rotation.from_env,
        to_key_env = %rotation.to_env,
        reason = rotation.reason,
        "rotating API key"
    );
    state.spool.emit(serde_json::json!({
        "ts": chrono::Utc::now().to_rfc3339(),
        "kind": "key_rotated",
        "provider": provider,
        "from_key_env": rotation.from_env,
        "to_key_env": rotation.to_env,
        "reason": rotation.reason,
    }));
}

fn emit_breaker_open(state: &AppState, provider: &str, consecutive: u32) {
    error!(
        provider = provider,
        consecutive_failures = consecutive,
        "CIRCUIT BREAKER OPEN: failing fast with 503 until cooldown elapses"
    );
    state.spool.emit(serde_json::json!({
        "ts": chrono::Utc::now().to_rfc3339(),
        "kind": "breaker_open",
        "provider": provider,
        "consecutive_failures": consecutive,
    }));
}

fn emit_breaker_closed(state: &AppState, provider: &str) {
    info!(provider = provider, "circuit breaker closed");
    state.spool.emit(serde_json::json!({
        "ts": chrono::Utc::now().to_rfc3339(),
        "kind": "breaker_closed",
        "provider": provider,
    }));
}

pub async fn proxy_handler(
    State(state): State<Arc<AppState>>,
    Path((provider_name, path)): Path<(String, String)>,
    method: Method,
    uri: Uri,
    headers: HeaderMap,
    body: Body,
) -> Response {
    let provider = match state.providers.get(&provider_name) {
        Some(p) => p.clone(),
        None => {
            return json_error(
                StatusCode::NOT_FOUND,
                "unknown_provider",
                &format!("no provider named {}", provider_name),
            )
        }
    };

    // Breaker gate: open (inside cooldown) or probe already in flight -> 503.
    if provider.decide() == Decision::Reject {
        let retry_after = provider
            .cooldown_remaining()
            .map(|d| d.as_secs())
            .unwrap_or(1);
        return json_error(
            StatusCode::SERVICE_UNAVAILABLE,
            "circuit_breaker_open",
            &format!(
                "provider {} circuit breaker is open; retry in {}s",
                provider_name, retry_after
            ),
        );
    }

    // Buffer the body up to the replay cap so we can re-send after a key
    // rotation. Larger bodies cannot be replayed safely: fail fast.
    let body_bytes = match axum::body::to_bytes(body, provider.config.replay_buffer_cap_bytes).await
    {
        Ok(b) => b,
        Err(_) => {
            error!(
                provider = provider_name,
                cap_bytes = provider.config.replay_buffer_cap_bytes,
                "request body exceeds replay cap; failing fast (increase replay_buffer_cap_bytes)"
            );
            return json_error(
                StatusCode::BAD_GATEWAY,
                "body_too_large_for_replay",
                "request body exceeds the replay buffer cap and cannot be retried safely",
            );
        }
    };

    let mut url = format!(
        "{}/{}",
        provider.config.base_url.trim_end_matches('/'),
        path
    );
    if let Some(query) = uri.query() {
        url.push('?');
        url.push_str(query);
    }

    loop {
        let key = match provider.current_key() {
            Some(k) => k,
            None => {
                warn!(provider = provider_name, "no live API keys remaining");
                if provider.on_upstream_failure() {
                    let h = provider.health();
                    emit_breaker_open(&state, &provider_name, h.consecutive);
                }
                return json_error(
                    StatusCode::SERVICE_UNAVAILABLE,
                    "no_live_keys",
                    &format!("provider {} has no live API keys", provider_name),
                );
            }
        };

        let mut req = state
            .client
            .request(method.clone(), &url)
            .body(body_bytes.clone());
        for (name, value) in headers.iter() {
            if is_hop_by_hop(name)
                || name == http::header::AUTHORIZATION
                || name == http::header::HOST
            {
                continue;
            }
            req = req.header(name, value);
        }
        req = req.header(http::header::AUTHORIZATION, format!("Bearer {}", key));
        for (name, value) in &provider.config.extra_headers {
            req = req.header(name.as_str(), value.as_str());
        }

        match req.send().await {
            Ok(resp) => {
                let status = resp.status();
                if status == StatusCode::UNAUTHORIZED || status == StatusCode::FORBIDDEN {
                    match provider.mark_dead_and_advance() {
                        Some(rotation) => {
                            emit_rotation(&state, &provider_name, &rotation);
                            continue; // retry once with the next key
                        }
                        None => {
                            warn!(
                                provider = provider_name,
                                "upstream rejected the last live key ({}); no keys left to rotate",
                                status.as_u16()
                            );
                            if provider.on_upstream_failure() {
                                let h = provider.health();
                                emit_breaker_open(&state, &provider_name, h.consecutive);
                            }
                            return upstream_response(resp); // transparency to client
                        }
                    }
                } else if status == StatusCode::TOO_MANY_REQUESTS {
                    match provider.soft_advance() {
                        Some(rotation) => {
                            emit_rotation(&state, &provider_name, &rotation);
                            continue;
                        }
                        None => {
                            // Upstream is reachable; not a breaker failure.
                            provider.on_upstream_success();
                            return upstream_response(resp);
                        }
                    }
                } else if status.is_server_error() {
                    warn!(
                        provider = provider_name,
                        status = status.as_u16(),
                        "upstream 5xx"
                    );
                    if provider.on_upstream_failure() {
                        let h = provider.health();
                        emit_breaker_open(&state, &provider_name, h.consecutive);
                    }
                    return upstream_response(resp);
                } else {
                    // Success, including non-auth 4xx (client bugs must not
                    // rotate keys or count against the breaker).
                    if provider.on_upstream_success() {
                        emit_breaker_closed(&state, &provider_name);
                    }
                    return upstream_response(resp);
                }
            }
            Err(e) => {
                warn!(
                    provider = provider_name,
                    error = %e,
                    "upstream transport error/timeout"
                );
                if provider.on_upstream_failure() {
                    let h = provider.health();
                    emit_breaker_open(&state, &provider_name, h.consecutive);
                }
                return json_error(
                    StatusCode::BAD_GATEWAY,
                    "upstream_error",
                    &format!("upstream request failed: {}", e),
                );
            }
        }
    }
}
