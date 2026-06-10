from __future__ import annotations

from typing import Any, Dict

from ir.runtime_payload import SerializedIRPayload


def payload_to_runtime_dict(payload: SerializedIRPayload) -> Dict[str, Any]:
    data = payload.to_dict()
    if not data.get("version"):
        raise ValueError("SerializedIRPayload.version is required")
    if not data.get("generated_at"):
        raise ValueError("SerializedIRPayload.generated_at is required")
    if not data.get("source_hash"):
        raise ValueError("SerializedIRPayload.source_hash is required")
    return data
