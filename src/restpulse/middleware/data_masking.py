import re
import json
import httpx
from typing import Callable, Awaitable, Any

DEFAULT_SENSITIVE_KEYS = {
    "password", "secret", "token", "authorization", "api_key",
    "apikey", "access_token", "ssn", "credit_card", "card_number"
}

CARD_PATTERN = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

class DataMaskingMiddleware:
    def __init__(
        self,
        mask_pattern: str = "***MASKED***",
        extra_sensitive_keys: set[str] | None = None,
    ):
        self.mask_pattern = mask_pattern
        self.sensitive_keys = DEFAULT_SENSITIVE_KEYS.union(extra_sensitive_keys or set())

    async def __call__(
        self,
        request: httpx.Request,
        call_next: Callable[[httpx.Request], Awaitable[httpx.Response]]
    ) -> httpx.Response:
        # Sanitize headers
        for key in list(request.headers.keys()):
            if key.lower() in self.sensitive_keys:
                request.headers[key] = self.mask_pattern

        # Sanitize body if JSON
        if request.content:
            try:
                body_str = request.content.decode("utf-8")
                body_data = json.loads(body_str)
                sanitized_data = self._mask_dict(body_data)
                request.stream = httpx.ByteStream(json.dumps(sanitized_data).encode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        return await call_next(request)

    def _mask_dict(self, data: Any) -> Any:
        if isinstance(data, dict):
            masked = {}
            for k, v in data.items():
                if k.lower() in self.sensitive_keys:
                    masked[k] = self.mask_pattern
                else:
                    masked[k] = self._mask_dict(v)
            return masked
        elif isinstance(data, list):
            return [self._mask_dict(item) for item in data]
        elif isinstance(data, str):
            data = CARD_PATTERN.sub(self.mask_pattern, data)
            data = SSN_PATTERN.sub(self.mask_pattern, data)
            return data
        return data