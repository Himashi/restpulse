import time
import asyncio
import httpx
from typing import Callable, Awaitable

class RateLimitError(Exception):
    """Raised when rate limit is exceeded and max retries are reached."""
    pass

class RateLimitMiddleware:
    def __init__(
        self,
        max_requests: int = 10,
        period: float = 1.0,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
    ):
        self.max_requests = max_requests
        self.period = period
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timestamps: list[float] = []

    async def __call__(
        self,
        request: httpx.Request,
        call_next: Callable[[httpx.Request], Awaitable[httpx.Response]]
    ) -> httpx.Response:
        retries = 0
        while retries <= self.max_retries:
            self._enforce_rate_limit()

            response = await call_next(request)

            if response.status_code == 429:
                if retries >= self.max_retries:
                    return response
                
                retry_after = response.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    sleep_time = float(retry_after)
                else:
                    sleep_time = self.backoff_factor * (2 ** retries)

                await asyncio.sleep(sleep_time)
                retries += 1
                continue

            return response

        raise RateLimitError("Rate limit exceeded and maximum retries reached.")

    def _enforce_rate_limit(self):
        now = time.time()
        # Remove timestamps outside the sliding window
        self.timestamps = [t for t in self.timestamps if now - t < self.period]
        
        if len(self.timestamps) >= self.max_requests:
            sleep_time = self.period - (now - self.timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.timestamps.append(time.time())