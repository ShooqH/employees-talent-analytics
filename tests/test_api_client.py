from unittest.mock import patch, MagicMock
from src.APIclient import HRApiClient
import requests

def test_failed_request_returns_none():
    # ARRANGE
    client = HRApiClient(base_url="https://fake-url.com")
    network_error = requests.exceptions.ConnectionError("Network down")

    # Intercept session.get and make it raise an error
    with patch.object(client.session, 'get', 
                      side_effect=network_error):
        # ACT
        result = client._make_request("some-endpoint")

    # ASSERT
    assert result is None
def test_retry_logic_attempts_twice():
    #ARRANGE
    client = HRApiClient(base_url="https://fake-url.com")
    network_error = requests.exceptions.ConnectionError("Network down")

    # Intercept session.get and make it raise an error
    with patch.object(client.session, 'get', side_effect=[network_error, network_error]) as mock_get:
        
        # ACT 
        result = client._make_request("some-endpoint")

    # ASSERT
    assert result is None
    assert mock_get.call_count ==2

def test_successful_request_returns_dict():
    # ARRANGE
    client = HRApiClient(base_url="https://fake-url.com")
    
    # generate 200 response 
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}

    # Intercept session.get
    with patch.object(client.session, 'get', return_value=mock_response):
        # ACT
        result = client._make_request("some-endpoint")

    # ASSERT
    assert result == {"status": "success"}
    assert isinstance(result, dict)