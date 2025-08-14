from types import SimpleNamespace

import pytest

from mcp_proxy.logic.utils import parsing_utils


@pytest.mark.parametrize(
    "input_str, expected_type",
    [
        ("string", str),
        ("boolean", bool),
        ("integer", int),
        ("float", float),
        ("unknown", str),  # default fallback
        ("", str),
        (None, str)
    ]
)
def test_map_str_to_type(input_str, expected_type):
    # Act
    result = parsing_utils.map_str_to_type(input_str)

    # Assert
    assert result is expected_type


def test_extract_param_types_with_path_and_query_params():
    # Arrange
    endpoint = SimpleNamespace(
        path_params=[SimpleNamespace(field="user_id", type="integer")],
        query_params=[SimpleNamespace(field="active", type="boolean")]
    )

    # Act
    result = parsing_utils.extract_param_types(endpoint)

    # Assert
    assert result == {"user_id": int, "active": bool}


def test_extract_param_types_with_empty_params():
    # Arrange
    endpoint = SimpleNamespace(
        path_params=None,
        query_params=None
    )

    # Act
    result = parsing_utils.extract_param_types(endpoint)

    # Assert
    assert result == {}


def test_extract_param_types_with_unknown_type():
    # Arrange
    endpoint = SimpleNamespace(
        path_params=[SimpleNamespace(field="custom", type="custom_type")],
        query_params=[]
    )

    # Act
    result = parsing_utils.extract_param_types(endpoint)

    # Assert
    assert result == {"custom": str}  # defaults to str
