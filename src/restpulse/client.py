import time
import asyncio
from typing import Any, Dict, Optional
import httpx
from restpulse.models import APIResponse
from restpulse.exceptions import APIError, AuthenticationError, NotFoundError

class RestPulseClient:
    """Client for making type-safe REST API requests with automatic retries."""

    def __init__(self, base_url: str = "", timeout: float = 10.0, retries: int = 3, backoff_factor: float = 0.5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = max(1, retries)
        self.backoff_factor = backoff_factor

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
        """Perform a synchronous GET request with retry logic for 5xx errors and network issues."""
        url = self._build_url(endpoint)
        response = None

        with httpx.Client(timeout=self.timeout) as client:
            for attempt in range(1, self.retries + 1):
                try:
                    response = client.get(url, params=params)
                    
                    # If server error (5xx) and we have retries left, retry
                    if response.status_code >= 500 and attempt < self.retries:
                        time.sleep(self.backoff_factor * (2 ** (attempt - 1)))
                        continue
                    
                    # Will raise HTTPStatusError for 4xx/5xx if not retried
                    response.raise_for_status()
                    break
                    
                except (httpx.TransportError, httpx.TimeoutException):
                    if attempt == self.retries:
                        raise
                    time.sleep(self.backoff_factor * (2 ** (attempt - 1)))
                except httpx.HTTPStatusError as e:
                    if e.response.status_code >= 500 and attempt < self.retries:
                        time.sleep(self.backoff_factor * (2 ** (attempt - 1)))
                        continue
                    self._handle_error(e)

        return APIResponse(
            status_code=response.status_code,
            data=response.json(),
            headers=dict(response.headers),
        )

    async def get_async(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Perform an asynchronous GET request with retry logic for 5xx errors and network issues."""
        url = self._build_url(endpoint)
        response = None

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(1, self.retries + 1):
                try:
                    response = await client.get(url, params=params)
                    
                    # If server error (5xx) and we have retries left, retry
                    if response.status_code >= 500 and attempt < self.retries:
                        await asyncio.sleep(self.backoff_factor * (2 ** (attempt - 1)))
                        continue
                        
                    response.raise_for_status()
                    break
                    
                except (httpx.TransportError, httpx.TimeoutException):
                    if attempt == self.retries:
                        raise
                    await asyncio.sleep(self.backoff_factor * (2 ** (attempt - 1)))
                except httpx.HTTPStatusError as e:
                    if e.response.status_code >= 500 and attempt < self.retries:
                        await asyncio.sleep(self.backoff_factor * (2 ** (attempt - 1)))
                        continue
                    self._handle_error(e)

        return APIResponse(
            status_code=response.status_code,
            data=response.json(),
            headers=dict(response.headers),
        )