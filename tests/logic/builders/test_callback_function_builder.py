from unittest.mock import MagicMock, patch

import pytest

from mcp_proxy.logic.builders.callback_function_builder import EndpointHttpCaller


@pytest.fixture
def fake_endpoint():
    """Creates a fake endpoint object with the attributes the class needs."""
    endpoint = MagicMock()
    endpoint.url = "http://api/users/{user_id}"
    endpoint.method.name = "GET"
    endpoint.path_params = [MagicMock(field="user_id")]
    endpoint.query_params = [MagicMock(field="active")]
    return endpoint


def test_successful_get_request(fake_endpoint):
    # Arrange
    caller = EndpointHttpCaller(fake_endpoint)
    mock_response = MagicMock()
    mock_response.text = "OK"
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response) as mock_get:
        # Act
        result = caller(user_id=123, active=True)

        # Assert
        mock_get.assert_called_once_with(
            "http://api/users/123", params={"active": True}
        )
        mock_response.raise_for_status.assert_called_once()
        assert result == "OK"


def test_missing_path_param(fake_endpoint):
    # Arrange
    caller = EndpointHttpCaller(fake_endpoint)
    fake_endpoint.path_params = [MagicMock(field="missing_id")]

    mock_response = MagicMock()
    mock_response.text = "OK"
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response) as mock_get:
        # Act
        result = caller(user_id=123, active=True)

        # Assert
        mock_get.assert_called_once_with(
            "http://api/users/{user_id}", params={"active": True}
        )
        assert result == "OK"


def test_unsupported_http_method(fake_endpoint):
    # Arrange
    fake_endpoint.method.name = "POST"
    caller = EndpointHttpCaller(fake_endpoint)

    # Act / Assert
    with pytest.raises(ValueError, match="Unsupported HTTP method: POST"):
        caller(user_id=1)


def test_build_url_with_path_params(fake_endpoint):
    # Arrange
    caller = EndpointHttpCaller(fake_endpoint)

    # Act
    result = caller._build_url_with_path_params({"user_id": 42})

    # Assert
    assert result == "http://api/users/42"


def test_extract_query_params(fake_endpoint):
    # Arrange
    caller = EndpointHttpCaller(fake_endpoint)

    # Act
    result = caller._extract_query_params({"active": True, "ignored": "x"})

    # Assert
    assert result == {"active": True}
