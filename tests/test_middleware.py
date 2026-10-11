from unittest.mock import MagicMock, patch
import pytest
from restpulse import RestPulseClient
from restpulse.models import APIResponse

@patch("restpulse.client.httpx.Client")
def test_before_request_and_after_response_hooks(mock_httpx_client_cls):
    # 1. Setup mock httpx response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_response.headers = {"content-type": "application/json"}
    
    mock_client_instance = mock_httpx_client_cls.return_value.__enter__.return_value
    mock_client_instance.get.return_value = mock_response

    # 2. Initialize client
    client = RestPulseClient(base_url="https://api.test")

    # 3. Track hook executions
    execution_order = []

    @client.before_request
    def add_auth_header(req):
        execution_order.append("before")
        req["headers"]["Authorization"] = "Bearer secret-123"
        return req

    @client.after_response
    def log_response(res):
        execution_order.append("after")
        return res

    # 4. Make request
    response = client.get("/data", params={"filter": "active"})

    # 5. Assertions
    assert execution_order == ["before", "after"]
    assert isinstance(response, APIResponse)
    assert response.status_code == 200
    assert response.data == {"status": "ok"}

    # Verify httpx received the header injected by the hook
    mock_client_instance.get.assert_called_once_with(
        "https://api.test/data",
        params={"filter": "active"},
        headers={"Authorization": "Bearer secret-123"}
    )