import base64
from typing import Any


def decode_file_payload(payload: dict[str, Any], key: str) -> bytes:
    data = payload.get("data") or payload
    encoded = data.get(key)
    if isinstance(encoded, str) and encoded:
        return base64.b64decode(encoded)

    binary_url = data.get("url")
    if binary_url:
        raise ValueError("Binary URL mode is not implemented in this scaffold")

    raise ValueError(f"Unsupported download payload format for key '{key}'")
