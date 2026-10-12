from __future__ import annotations

import time
import asyncio
from typing import Any, Callable, Dict, List, Optional
import httpx
from restpulse.models import APIResponse
from restpulse.exceptions import APIError, AuthenticationError, NotFoundError
from restpulse.config import ConnectionPoolConfig

class RestPulseClient:
    """Client for making type-safe REST API requests with automatic retries, connection pooling, and middleware hooks."""

    def __init__(
        self,
        base_url: str = "",
        timeout: float = 10.0,
        retries: int = 3,
        backoff_factor: float = 0.5,
        pool_config: ConnectionPoolConfig | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = max(1, retries)
        self.backoff_factor = backoff_factor
        self.pool_config = pool_config or ConnectionPoolConfig()

        # Hook registries for middleware
        self.request_hooks: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = []
        self.response_hooks: List[Callable[[httpx.Response], httpx.Response]] = []

    def before_request(self, hook: Callable[[Dict[str, Any]], Dict[str, Any]]):
        """Register a hook to modify or inspect requests before execution."""
        self.request_hooks.append(hook)
        return hook

    def after_response(self, hook: Callable[[httpx.Response], httpx.Response]):
        """Register a hook to process responses globally."""
        self.response_hooks.append(hook)
        return hook

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

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Perform a synchronous GET request with retry logic and middleware hooks."""
        url = self._build_url(endpoint)
        
        req_context = {
            "method": "GET",
            "url": url,
            "params": params or {},
            "headers": headers or {}
        }

        for hook in self.request_hooks:
            req_context = hook(req_context)

        url = req_context["url"]
        params = req_context["params"]
        req_headers = req_context["headers"]

        response = None
        start_time = time.time()

        limits = self.pool_config.to_limits()
        timeout_config = self.pool_config.to_timeout()

        with httpx.Client(timeout=timeout_config, limits=limits) as client:
            for attempt in range(1, self.retries + 1):
                try:
                    response = client.get(url, params=params, headers=req_headers)
                    
                    if response.status_code >= 500 and attempt < self.retries:
                        time.sleep(self.backoff_factor * (2 ** (attempt - 1)))
                        continue
                    
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

        response.elapsed_time = time.time() - start_time

        for hook in self.response_hooks:
            response = hook(response)

        return APIResponse(
            status_code=response.status_code,
            data=response.json(),
            headers=dict(response.headers),
        )

    async def get_async(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Perform an asynchronous GET request with retry logic and middleware hooks."""
        url = self._build_url(endpoint)
        
        req_context = {
            "method": "GET",
            "url": url,
            "params": params or {},
            "headers": headers or {}
        }

        for hook in self.request_hooks:
            req_context = hook(req_context)

        url = req_context["url"]
        params = req_context["params"]
        req_headers = req_context["headers"]

        response = None
        start_time = time.time()

        limits = self.pool_config.to_limits()
        timeout_config = self.pool_config.to_timeout()

        async with httpx.AsyncClient(timeout=timeout_config, limits=limits) as client:
            for attempt in range(1, self.retries + 1):
                try:
                    response = await client.get(url, params=params, headers=req_headers)
                    
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

        response.elapsed_time = time.time() - start_time

        for hook in self.response_hooks:
            response = hook(response)

        return APIResponse(
            status_code=response.status_code,
            data=response.json(),
            headers=dict(response.headers),
        )