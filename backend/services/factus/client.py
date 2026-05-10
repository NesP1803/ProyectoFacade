from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib import request, error
import json
import time

from .endpoints import FactusEndpointRegistry


@dataclass
class FactusApiError(Exception):
    message: str
    status_code: int
    payload: dict[str, Any] | None = None


class FactusClient:
    def __init__(self, base_url: str, token: str, endpoints: FactusEndpointRegistry, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.endpoints = endpoints
        self.timeout = timeout

    def request(self, logical_endpoint: str, method: str = "GET", body: dict[str, Any] | None = None, retries_429: int = 2, **path_params: str) -> dict[str, Any]:
        path = self.endpoints.resolve(logical_endpoint, **path_params)
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        if body is not None:
            headers["Content-Type"] = "application/json"

        for attempt in range(retries_429 + 1):
            req = request.Request(url=url, method=method.upper(), data=data, headers=headers)
            try:
                with request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except error.HTTPError as exc:
                response_payload = self._read_error_payload(exc)
                if exc.code == 429 and attempt < retries_429:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise FactusApiError(
                    message=self._extract_error_message(response_payload, exc.code),
                    status_code=exc.code,
                    payload=response_payload,
                )

        raise FactusApiError("Rate limit retries exhausted", 429)

    @staticmethod
    def _read_error_payload(exc: error.HTTPError) -> dict[str, Any] | None:
        try:
            raw = exc.read().decode("utf-8")
            return json.loads(raw) if raw else None
        except Exception:
            return None

    @staticmethod
    def _extract_error_message(payload: dict[str, Any] | None, status_code: int) -> str:
        if not payload:
            return f"Factus API request failed with HTTP {status_code}"
        if isinstance(payload.get("message"), str):
            return payload["message"]
        errors = payload.get("errors")
        if isinstance(errors, dict):
            return f"Factus validation error ({status_code}): {errors}"
        return f"Factus API request failed with HTTP {status_code}"
