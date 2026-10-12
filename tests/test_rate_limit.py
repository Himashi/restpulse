import pytest
import httpx
import respx
from restpulse.middleware.rate_limit import RateLimitMiddleware

@pytest.mark.anyio
@respx.mock
async def test_rate_limit_success():
    respx.get("https://api.example.com/data").mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )

    middleware = RateLimitMiddleware(max_requests=5, period=1.0)
    
    async def call_next(request: httpx.Request):
        client = httpx.AsyncClient()
        return await client.send(request)

    request = httpx.Request("GET", "https://api.example.com/data")
    response = await middleware(request, call_next)
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.anyio
@respx.mock
async def test_rate_limit_retry_after():
    route = respx.get("https://api.example.com/rate-limited")
    route.side_effect = [
        httpx.Response(429, headers={"Retry-After": "0.1"}),
        httpx.Response(200, json={"success": True})
    ]

    middleware = RateLimitMiddleware(max_requests=5, period=1.0, max_retries=2)
    
    async def call_next(request: httpx.Request):
        client = httpx.AsyncClient()
        return await client.send(request)

    request = httpx.Request("GET", "https://api.example.com/rate-limited")
    response = await middleware(request, call_next)
    
    assert response.status_code == 200
    assert response.json() == {"success": True}