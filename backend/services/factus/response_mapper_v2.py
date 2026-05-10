from typing import Any


INTERNAL_STATUS_MAP = {
    "validated": "ACEPTADA",
    "accepted": "ACEPTADA",
    "accepted_with_warnings": "ACEPTADA_CON_OBSERVACIONES",
    "rejected": "RECHAZADA",
    "pending": "PENDIENTE_REINTENTO",
    "error": "ERROR_INTEGRACION",
}


def map_factus_status(raw_status: str | None) -> str:
    if not raw_status:
        return "PENDIENTE_REINTENTO"
    return INTERNAL_STATUS_MAP.get(raw_status.lower(), "PENDIENTE_REINTENTO")


def extract_document_data(payload: dict[str, Any]) -> dict[str, Any]:
    data = payload.get("data") or {}
    return data.get("bill") or data.get("credit_note") or data
