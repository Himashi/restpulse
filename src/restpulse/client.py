from typing import Any, Dict, Optional
import httpx
from restpulse.models import APIResponse
from restpulse.exceptions import APIError, AuthenticationError, NotFoundError

class RestPulseClient:
    """Client for making type-safe REST API requests."""

    def __init__(self, base_url: str = "", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _build_url(self, endpoint: str) -> str:
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}" if self.base_url else endpoint

    def _handle_error(self, error: httpx.HTTPStatusError) -> None:
        """Translate httpx status errors into custom exceptions."""
        status_code = error.response.status_code
        message = f"API request failed with status {status_code}: {error.request.url}"
        body = error.response.text

        if status_code == 401:
            raise AuthenticationError(message, status_code, body)
        elif status_code == 404:
            raise NotFoundError(message, status_code, body)
        else:
            raise APIError(message, status_code, body)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Perform a synchronous GET request."""
        url = self._build_url(endpoint)
        with httpx.Client(timeout=self.timeout) as client:
            try:
                response = client.get(url, params=params)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                self._handle_error(e)
            
            return APIResponse(
                status_code=response.status_code,
                data=response.json(),
                headers=dict(response.headers),
            )

    async def get_async(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Perform an asynchronous GET request."""
        url = self._build_url(endpoint)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                self._handle_error(e)
            
            return APIResponse(
                status_code=response.status_code,
                data=response.json(),
                headers=dict(response.headers),
            )