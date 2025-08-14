from unittest.mock import mock_open, patch, MagicMock

import pytest

from mcp_proxy.logic.deserializers.config_deserializer import ConfigurationDeserializer


@pytest.fixture
def config_path():
    return "/fake/path/config.json"


def test_file_not_exists(config_path):
    # Arrange
    with patch("os.path.exists", return_value=False):
        deserializer = ConfigurationDeserializer(config_path)

        # Act
        result = deserializer.deserialize_json_config()

        # Assert
        assert result is None


def test_file_exists_and_loads_successfully(config_path):
    # Arrange
    fake_json = '{"version": "1.0"}'
    mock_api_config = MagicMock()
    with patch("os.path.exists", return_value=True), \
            patch("builtins.open", mock_open(read_data=fake_json)), \
            patch("mcp_proxy.models.mcp_endpoints_schema.ApiConfig.from_json",
                  return_value=mock_api_config) as mock_from_json:
        deserializer = ConfigurationDeserializer(config_path)

        # Act
        result = deserializer.deserialize_json_config()

        # Assert
        mock_from_json.assert_called_once_with(fake_json)
        assert result == mock_api_config


def test_file_exists_and_raises_valueerror(config_path):
    # Arrange
    fake_json = '{"bad": "data"}'
    with patch("os.path.exists", return_value=True), \
            patch("builtins.open", mock_open(read_data=fake_json)), \
            patch("mcp_proxy.models.mcp_endpoints_schema.ApiConfig.from_json", side_effect=ValueError("Invalid JSON")):
        deserializer = ConfigurationDeserializer(config_path)

        # Act
        result = deserializer.deserialize_json_config()

        # Assert
        assert result is None
