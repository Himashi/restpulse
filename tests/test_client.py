import pytest
import respx
from httpx import Response
from restpulse.client import RestPulseClient
from restpulse.exceptions import NotFoundError, AuthenticationError


def test_sync_get_not_found():
    """Test that a 404 response raises NotFoundError."""
    client = RestPulseClient(base_url="https://api.example.com")
    
    with respx.mock:
        respx.get("https://api.example.com/missing").mock(
            return_value=Response(404, json={"error": "Not Found"})
        )
        
        with pytest.raises(NotFoundError) as exc_info:
            client.get("/missing")
        
        assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_async_get_unauthorized():
    """Test that a 401 response raises AuthenticationError."""
    client = RestPulseClient(base_url="https://api.example.com")
    
    with respx.mock:
        respx.get("https://api.example.com/secret").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        
        with pytest.raises(AuthenticationError) as exc_info:
            await client.get_async("/secret")
        
        assert exc_info.value.status_code == 401