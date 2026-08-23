"""
lucineer.cns_telemetry — shared CNS v3 telemetry emission helper.

Single production-grade emit path for USCP-v3 packets so that individual
lucineer modules import one helper instead of reimplementing the packet format.
"""
from __future__ import annotations
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CNS_INBOX = os.path.expanduser("~/.hermes/cns_inbox/")
CNS_OUTBOX = os.path.expanduser("~/.hermes/cns_outbox/")


@dataclass
class TelemetryQuantum:
    agent_id: str
    gamma: float = 0.5
    eta: float = 0.25
    delta: float = 0.25
    temperature: float = 1.0
    semantic_distance: float = 0.5
    melt_pressure: float = 0.0
    max_crystallization_rate: float = 0.0
    deterministic: bool = False
    molt_count: int = 0
    capability: float = 1.0
    tau: float = 0.5
    timestamp: str = ""
    is_dreaming: bool = False
    temperature_idle: float = 1.5
    temperature_task: float = 1.0
    temp_rise_rate: float = 0.0
    last_validation: str = ""
    time_since_validation_seconds: float = 0.0
    molt_phase: str = "stable"
    creative_value: float = 0.5
    kappa_delta: float = 0.5


def _to_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
def _build_identity(role: str, model: str, backend: str) -> dict[str, Any]:
    import hashlib
    commitment = hashlib.sha256(f"{role}||{model}||{backend}".encode()).hexdigest()[:16]
    return {
        "identity_hash": f"sha256:{commitment}",
        "role": role,
        "model": model,
        "backend": backend,
    }
def build_v3_payload(
    tq: TelemetryQuantum,
    *,
    role: str = "lucineer-agent",
    model: str = "lucineer",
    backend: str = "python-3.14",
    identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "gamma_eta": {
            "per_agent": {
                tq.agent_id: {
                    "gamma": tq.gamma,
                    "eta": tq.eta,
                    "delta": tq.delta,
                }
            }
        },
        "thermal": {
            "temperature": tq.temperature,
            "is_dreaming": tq.is_dreaming,
            "temperature_idle": tq.temperature_idle,
            "temperature_task": tq.temperature_task,
            "last_updated": tq.timestamp,
        },
        "melt": {
            "melt_pressure": tq.melt_pressure,
            "max_crystallization_rate": tq.max_crystallization_rate,
            "deterministic": tq.deterministic,
            "molt_count": tq.molt_count,
            "capability": tq.capability,
            "last_validation": tq.last_validation,
            "time_since_validation_seconds": tq.time_since_validation_seconds,
            "molt_phase": tq.molt_phase,
            "temp_rise_rate": tq.temp_rise_rate,
        },
        "creative": {
            "semantic_distance": tq.semantic_distance,
            "creative_value": tq.creative_value,
            "kappa_delta": tq.kappa_delta,
        },
        "uncertainty": {
            "tau": tq.tau,
        },
        "identity": identity or _build_identity(role, model, backend),
    }
def emit_cns_pulse(
    agent_id: str,
    telemetry: TelemetryQuantum | dict[str, Any],
    *,
    intent: str = "CNS_PULSE_STATUS",
    priority: str = "NORMAL",
    role: str = "lucineer-agent",
    model: str = "lucineer",
    backend: str = "python-3.14",
    extensions: list[str] | None = None,
) -> str | None:
    if isinstance(telemetry, dict):
        telemetry = TelemetryQuantum(agent_id=agent_id, **telemetry)
    if not telemetry.timestamp:
        telemetry.timestamp = _to_iso()

    payload = build_v3_payload(
        telemetry,
        role=role,
        model=model,
        backend=backend,
    )
    packet = {
        "header": {
            "origin_id": agent_id,
            "timestamp": telemetry.timestamp,
            "priority": priority,
            "correlation_id": telemetry.timestamp,
            "destination_id": "hermes",
        },
        "body": {
            "intent": intent,
            "payload": payload,
        },
        "signature": {
            "type": "USCP-v3",
            "version": "3.0",
            "extensions": extensions or ["lucineer-cns-telemetry"],
        },
    }

    try:
        Path(CNS_INBOX).mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        path = Path(CNS_INBOX) / f"lucineer_{agent_id}_{ts}.json"
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(packet, indent=2), encoding="utf-8")
        os.replace(tmp, path)
        return str(path)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"emit_cns_pulse failed: {e}")
        return None
