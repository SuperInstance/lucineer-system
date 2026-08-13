use axum::body::Body;
use axum::http::{HeaderMap, StatusCode};
use axum::response::Response;
use axum::routing::any;
use axum::Router;
use fleet_gateway::config::{GatewayConfig, GatewaySection, ProviderConfig};
use fleet_gateway::AppState;
use std::collections::HashMap;
use std::net::SocketAddr;
use std::path::Path;
use std::sync::{Arc, Mutex};
use tempfile::TempDir;

/// Mock upstream: records the headers of every hit, answers per `script`
/// (hit index -> status code).
struct Mock {
    hits: Mutex<Vec<HeaderMap>>,
    script: Box<dyn Fn(usize) -> u16 + Send + Sync>,
}

impl Mock {
    fn hit_count(&self) -> usize {
        self.hits.lock().unwrap().len()
    }
}

async fn spawn_mock(script: impl Fn(usize) -> u16 + Send + Sync + 'static) -> (SocketAddr, Arc<Mock>) {
    let mock = Arc::new(Mock {
        hits: Mutex::new(Vec::new()),
        script: Box::new(script),
    });
    let m = mock.clone();
    let app = Router::new().fallback(any(move |headers: HeaderMap| {
        let m = m.clone();
        async move {
            let n = {
                let mut hits = m.hits.lock().unwrap();
                hits.push(headers);
                hits.len() - 1
            };
            let status = (m.script)(n);
            Response::builder()
                .status(StatusCode::from_u16(status).unwrap())
                .body(Body::from(format!("mock-hit-{}", n)))
                .unwrap()
        }
    }));
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    let addr = listener.local_addr().unwrap();
    tokio::spawn(async move {
        axum::serve(listener, app).await.unwrap();
    });
    (addr, mock)
}

fn test_config(
    name: &str,
    base_url: String,
    keys: Vec<&str>,
    spool_dir: &Path,
    threshold: u32,
    cooldown_secs: u64,
) -> GatewayConfig {
    GatewayConfig {
        gateway: GatewaySection {
            spool_dir: spool_dir.to_path_buf(),
            request_timeout_secs: 5,
        },
        providers: vec![ProviderConfig {
            name: name.to_string(),
            base_url,
            keys: keys.iter().map(|k| k.to_string()).collect(),
            breaker_threshold: threshold,
            breaker_cooldown_secs: cooldown_secs,
            extra_headers: HashMap::new(),
            replay_buffer_cap_bytes: 1024 * 1024,
        }],
    }
}

async fn spawn_gateway(config: GatewayConfig) -> SocketAddr {
    let state = Arc::new(AppState::from_config(&config).unwrap());
    let app = fleet_gateway::build_router(state);
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    let addr = listener.local_addr().unwrap();
    tokio::spawn(async move {
        axum::serve(listener, app).await.unwrap();
    });
    addr
}

#[tokio::test]
async fn rotates_key_on_401_and_retried_request_succeeds() {
    std::env::set_var("GW_T1_KEY_A", "sk-alpha-secret");
    std::env::set_var("GW_T1_KEY_B", "sk-beta-secret");
    let (mock_addr, mock) = spawn_mock(|n| if n == 0 { 401 } else { 200 }).await;
    let spool = TempDir::new().unwrap();
    let config = test_config(
        "t1",
        format!("http://{}", mock_addr),
        vec!["GW_T1_KEY_A", "GW_T1_KEY_B"],
        spool.path(),
        5,
        60,
    );
    let gw = spawn_gateway(config).await;

    let client = reqwest::Client::new();
    let resp = client
        .post(format!("http://{}/v1/t1/chat/completions?stream=false", gw))
        .header("authorization", "Bearer client-token-must-be-stripped")
        .header("content-type", "application/json")
        .body(r#"{"prompt":"hello"}"#)
        .send()
        .await
        .unwrap();
    assert_eq!(resp.status(), 200);
    assert_eq!(resp.text().await.unwrap(), "mock-hit-1");

    let hits = mock.hits.lock().unwrap();
    assert_eq!(hits.len(), 2, "first key 401 -> retried with second key");
    assert_eq!(hits[0]["authorization"], "Bearer sk-alpha-secret");
    assert_eq!(
        hits[1]["authorization"], "Bearer sk-beta-secret",
        "second key's Authorization reached upstream"
    );
    assert_ne!(
        hits[0]["authorization"], "Bearer client-token-must-be-stripped",
        "client Authorization must be stripped and replaced"
    );
    drop(hits);

    // CNS spool: rotation event, env names only — never key material.
    let spool_text = std::fs::read_to_string(spool.path().join("gateway.jsonl")).unwrap();
    let events: Vec<serde_json::Value> = spool_text
        .lines()
        .map(|l| serde_json::from_str(l).unwrap())
        .collect();
    let rotation = events
        .iter()
        .find(|e| e["kind"] == "key_rotated")
        .expect("key_rotated event must be written to the CNS spool");
    assert_eq!(rotation["provider"], "t1");
    assert_eq!(rotation["from_key_env"], "GW_T1_KEY_A");
    assert_eq!(rotation["to_key_env"], "GW_T1_KEY_B");
    assert!(
        !spool_text.contains("sk-alpha-secret") && !spool_text.contains("sk-beta-secret"),
        "key material must never hit the spool"
    );
}

#[tokio::test]
async fn non_auth_4xx_passes_through_without_rotation() {
    std::env::set_var("GW_T2_KEY_A", "sk-t2-alpha");
    std::env::set_var("GW_T2_KEY_B", "sk-t2-beta");
    let (mock_addr, mock) = spawn_mock(|_| 400).await;
    let spool = TempDir::new().unwrap();
    let config = test_config(
        "t2",
        format!("http://{}", mock_addr),
        vec!["GW_T2_KEY_A", "GW_T2_KEY_B"],
        spool.path(),
        5,
        60,
    );
    let gw = spawn_gateway(config).await;

    let client = reqwest::Client::new();
    let resp = client
        .post(format!("http://{}/v1/t2/thing", gw))
        .body("{}")
        .send()
        .await
        .unwrap();
    assert_eq!(resp.status(), 400, "non-auth 4xx passes through untouched");
    assert_eq!(mock.hit_count(), 1, "no rotation, no retry");

    let health: serde_json::Value = client
        .get(format!("http://{}/healthz", gw))
        .send()
        .await
        .unwrap()
        .json()
        .await
        .unwrap();
    assert_eq!(health["providers"]["t2"]["live_keys"], 2, "client bugs don't kill keys");
    assert_eq!(health["providers"]["t2"]["breaker"], "closed");
    assert_eq!(health["providers"]["t2"]["consecutive_failures"], 0);
}

#[tokio::test]
async fn all_keys_dead_opens_breaker_then_503s_without_upstream_hits() {
    std::env::set_var("GW_T3_KEY_A", "sk-t3-alpha");
    std::env::set_var("GW_T3_KEY_B", "sk-t3-beta");
    let (mock_addr, mock) = spawn_mock(|_| 401).await;
    let spool = TempDir::new().unwrap();
    let config = test_config(
        "t3",
        format!("http://{}", mock_addr),
        vec!["GW_T3_KEY_A", "GW_T3_KEY_B"],
        spool.path(),
        2,
        60,
    );
    let gw = spawn_gateway(config).await;
    let client = reqwest::Client::new();

    // Request 1: key A -> 401 -> rotate -> key B -> 401 -> no keys left,
    // breaker failure count 1. Last upstream response passes through.
    let resp = client
        .get(format!("http://{}/v1/t3/models", gw))
        .send()
        .await
        .unwrap();
    assert_eq!(resp.status(), 401);
    assert_eq!(mock.hit_count(), 2, "both keys tried once");

    // Request 2: no live keys -> breaker failure count 2 = threshold -> open.
    let resp = client
        .get(format!("http://{}/v1/t3/models", gw))
        .send()
        .await
        .unwrap();
    assert_eq!(resp.status(), 503);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["error"], "no_live_keys");

    // Request 3: breaker open -> instant 503, ZERO new upstream hits.
    let resp = client
        .get(format!("http://{}/v1/t3/models", gw))
        .send()
        .await
        .unwrap();
    assert_eq!(resp.status(), 503);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["error"], "circuit_breaker_open");
    assert_eq!(mock.hit_count(), 2, "open breaker must not call upstream");

    let health: serde_json::Value = client
        .get(format!("http://{}/healthz", gw))
        .send()
        .await
        .unwrap()
        .json()
        .await
        .unwrap();
    assert_eq!(health["providers"]["t3"]["breaker"], "open");
    assert_eq!(health["providers"]["t3"]["live_keys"], 0);
}

#[tokio::test]
async fn breaker_opens_on_5xx_then_half_open_probe_closes_it() {
    std::env::set_var("GW_T4_KEY_A", "sk-t4-alpha");
    // First two hits 500 (threshold), then healthy.
    let (mock_addr, mock) = spawn_mock(|n| if n < 2 { 500 } else { 200 }).await;
    let spool = TempDir::new().unwrap();
    let config = test_config(
        "t4",
        format!("http://{}", mock_addr),
        vec!["GW_T4_KEY_A"],
        spool.path(),
        2,
        1, // 1s cooldown so the test can wait it out
    );
    let gw = spawn_gateway(config).await;
    let client = reqwest::Client::new();

    for _ in 0..2 {
        let resp = client
            .get(format!("http://{}/v1/t4/x", gw))
            .send()
            .await
            .unwrap();
        assert_eq!(resp.status(), 500, "upstream 5xx passes through");
    }
    assert_eq!(mock.hit_count(), 2);

    // Breaker now open: instant 503, no upstream hit.
    let resp = client
        .get(format!("http://{}/v1/t4/x", gw))
        .send()
        .await
        .unwrap();
    assert_eq!(resp.status(), 503);
    assert_eq!(mock.hit_count(), 2, "open breaker must not call upstream");

    // After cooldown the half-open probe goes through, succeeds, closes.
    tokio::time::sleep(std::time::Duration::from_millis(1100)).await;
    let resp = client
        .get(format!("http://{}/v1/t4/x", gw))
        .send()
        .await
        .unwrap();
    assert_eq!(resp.status(), 200, "half-open probe succeeded");
    assert_eq!(mock.hit_count(), 3);

    let health: serde_json::Value = client
        .get(format!("http://{}/healthz", gw))
        .send()
        .await
        .unwrap()
        .json()
        .await
        .unwrap();
    assert_eq!(health["providers"]["t4"]["breaker"], "closed");
    assert_eq!(health["providers"]["t4"]["consecutive_failures"], 0);

    // Spool saw breaker_open and breaker_closed.
    let spool_text = std::fs::read_to_string(spool.path().join("gateway.jsonl")).unwrap();
    assert!(spool_text.contains("\"kind\":\"breaker_open\""));
    assert!(spool_text.contains("\"kind\":\"breaker_closed\""));
}

#[tokio::test]
async fn zero_resolvable_keys_starts_with_breaker_open() {
    // keys = [] and an env var that does not exist: both start open.
    let spool = TempDir::new().unwrap();
    let (mock_addr, mock) = spawn_mock(|_| 200).await;
    let config = GatewayConfig {
        gateway: GatewaySection {
            spool_dir: spool.path().to_path_buf(),
            request_timeout_secs: 5,
        },
        providers: vec![
            ProviderConfig {
                name: "empty".into(),
                base_url: format!("http://{}", mock_addr),
                keys: vec![],
                breaker_threshold: 5,
                breaker_cooldown_secs: 60,
                extra_headers: HashMap::new(),
                replay_buffer_cap_bytes: 1024 * 1024,
            },
            ProviderConfig {
                name: "unresolvable".into(),
                base_url: format!("http://{}", mock_addr),
                keys: vec!["GW_T5_DEFINITELY_NOT_SET_ANYWHERE".into()],
                breaker_threshold: 5,
                breaker_cooldown_secs: 60,
                extra_headers: HashMap::new(),
                replay_buffer_cap_bytes: 1024 * 1024,
            },
        ],
    };
    let gw = spawn_gateway(config).await;
    let client = reqwest::Client::new();

    for name in ["empty", "unresolvable"] {
        let resp = client
            .get(format!("http://{}/v1/{}/x", gw, name))
            .send()
            .await
            .unwrap();
        assert_eq!(resp.status(), 503, "provider {} starts with breaker open", name);
    }
    assert_eq!(mock.hit_count(), 0, "no upstream calls at all");

    let health: serde_json::Value = client
        .get(format!("http://{}/healthz", gw))
        .send()
        .await
        .unwrap()
        .json()
        .await
        .unwrap();
    assert_eq!(health["providers"]["empty"]["live_keys"], 0);
    assert_eq!(health["providers"]["empty"]["breaker"], "open");
    assert_eq!(health["providers"]["unresolvable"]["live_keys"], 0);
    assert_eq!(health["providers"]["unresolvable"]["breaker"], "open");
}

#[tokio::test]
async fn healthz_shape_and_no_secret_leak() {
    std::env::set_var("GW_T6_KEY_A", "sk-t6-topsecret-alpha");
    std::env::set_var("GW_T6_KEY_B", "sk-t6-topsecret-beta");
    let (mock_addr, _mock) = spawn_mock(|_| 200).await;
    let spool = TempDir::new().unwrap();
    let config = test_config(
        "t6",
        format!("http://{}", mock_addr),
        vec!["GW_T6_KEY_A", "GW_T6_KEY_B"],
        spool.path(),
        5,
        60,
    );
    let gw = spawn_gateway(config).await;
    let client = reqwest::Client::new();

    let resp = client
        .get(format!("http://{}/healthz", gw))
        .send()
        .await
        .unwrap();
    assert_eq!(resp.status(), 200);
    let body = resp.text().await.unwrap();
    let health: serde_json::Value = serde_json::from_str(&body).unwrap();

    assert_eq!(health["status"], "ok");
    assert!(health["uptime_secs"].is_number());
    let t6 = &health["providers"]["t6"];
    assert_eq!(t6["breaker"], "closed");
    assert_eq!(t6["live_keys"], 2, "key counts reported");
    assert_eq!(t6["total_keys"], 2);
    assert!(t6["consecutive_failures"].is_number());
    assert!(t6["cooldown_remaining_secs"].is_number());

    assert!(
        !body.contains("sk-t6-topsecret-alpha") && !body.contains("sk-t6-topsecret-beta"),
        "healthz must never contain key material"
    );
}

#[tokio::test]
async fn unknown_provider_is_404_and_no_config_providers_is_fatal() {
    let spool = TempDir::new().unwrap();
    std::env::set_var("GW_T7_KEY_A", "sk-t7");
    let (mock_addr, _mock) = spawn_mock(|_| 200).await;
    let config = test_config(
        "t7",
        format!("http://{}", mock_addr),
        vec!["GW_T7_KEY_A"],
        spool.path(),
        5,
        60,
    );
    let gw = spawn_gateway(config).await;
    let resp = reqwest::Client::new()
        .get(format!("http://{}/v1/nope/x", gw))
        .send()
        .await
        .unwrap();
    assert_eq!(resp.status(), 404);

    // Empty provider list is a startup config fault.
    let empty = GatewayConfig {
        gateway: GatewaySection {
            spool_dir: spool.path().to_path_buf(),
            request_timeout_secs: 5,
        },
        providers: vec![],
    };
    let err = match AppState::from_config(&empty) {
        Ok(_) => panic!("expected NoProviders fault"),
        Err(e) => e.to_string(),
    };
    assert!(err.contains("no providers"), "got: {}", err);
}
