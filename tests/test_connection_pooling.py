import pytest
import httpx
import respx
from restpulse import RestPulseClient, ConnectionPoolConfig

@pytest.mark.anyio
@respx.mock
async def test_connection_pool_configuration():
    respx.get("https://api.example.com/pool").mock(
        return_value=httpx.Response(200, json={"pooled": True})
    )

    config = ConnectionPoolConfig(
        max_connections=50,
        max_keepalive_connections=10,
        keepalive_expiry=2.0
    )

    client = RestPulseClient(base_url="https://api.example.com", pool_config=config)
    response = await client.get_async("/pool")
    
    assert response.status_code == 200
    assert response.data == {"pooled": True}