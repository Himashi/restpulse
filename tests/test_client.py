import pytest
import respx
from httpx import Response
from restpulse.client import RestPulseClient
from restpulse.models import APIResponse


def test_sync_get_retry_success():
    """Test that client retries on 500 error and succeeds on subsequent attempt."""
    client = RestPulseClient(base_url="https://api.example.com", retries=3, backoff_factor=0.01)
    
    with respx.mock:
        route = respx.get("https://api.example.com/flakey")
        route.side_effect = [
            Response(500, json={"error": "Server Error"}),
            Response(200, json={"success": True})
        ]
        
        response = client.get("/flakey")
        
        assert response.status_code == 200
        assert response.data == {"success": True}
        assert route.call_count == 2