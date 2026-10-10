import pytest
import respx
from httpx import Response
from restpulse.client import RestPulseClient
from restpulse.models import APIResponse


def test_sync_get_success():
    """Test standard synchronous GET request with mocked response."""
    client = RestPulseClient(base_url="https://api.example.com")
    
    with respx.mock:
        respx.get("https://api.example.com/users").mock(
            return_value=Response(200, json={"id": 1, "name": "Alice"})
        )
        
        response = client.get("/users")
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data == {"id": 1, "name": "Alice"}


@pytest.mark.asyncio
async def test_async_get_success():
    """Test asynchronous GET request with mocked response."""
    client = RestPulseClient(base_url="https://api.example.com")
    
    with respx.mock:
        respx.get("https://api.example.com/status").mock(
            return_value=Response(200, json={"status": "ok"})
        )
        
        response = await client.get_async("/status")
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data["status"] == "ok"