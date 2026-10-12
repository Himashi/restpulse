import pytest
import httpx
import json
import respx
from restpulse.middleware.data_masking import DataMaskingMiddleware

@pytest.mark.anyio
@respx.mock
async def test_data_masking_headers_and_body():
    respx.post("https://api.example.com/login").mock(
        return_value=httpx.Response(200, json={"status": "authenticated"})
    )

    middleware = DataMaskingMiddleware()

    async def call_next(request: httpx.Request):
        assert request.headers["Authorization"] == "***MASKED***"
        body = json.loads(request.content.decode("utf-8"))
        assert body["password"] == "***MASKED***"
        assert body["user"] == "john_doe"
        
        client = httpx.AsyncClient()
        return await client.send(request)

    request = httpx.Request(
        "POST",
        "https://api.example.com/login",
        headers={"Authorization": "Bearer secret_token_123"},
        json={"user": "john_doe", "password": "supersecretpassword"}
    )

    response = await middleware(request, call_next)
    assert response.status_code == 200