from inspect import Signature
from unittest.mock import MagicMock

import pytest

from mcp_proxy.logic.builders.mcp_function_builder import MCPFunctionBuilder


@pytest.fixture
def fake_mcp():
    """Fake FastMCP instance with a mock tool decorator."""
    mcp = MagicMock()
    mcp.tool.return_value = lambda func: func  # passthrough decorator
    return mcp


@pytest.fixture
def fake_params():
    """Fake FunctionParams object."""
    params = MagicMock()
    params.name = "test_func"
    params.doc = "This is a test function."
    params.return_type = str
    params.param_types = {
        "x": int,
        "y": str
    }
    params.callback = MagicMock(return_value="OK")
    return params


def test_build_creates_function_with_correct_metadata(fake_mcp, fake_params):
    # Arrange
    builder = MCPFunctionBuilder(fake_mcp)

    # Act
    built_func = builder.build(fake_params)

    # Assert
    assert callable(built_func)
    assert built_func.__name__ == "test_func"
    assert built_func.__doc__ == "This is a test function."
    assert built_func.__annotations__ == {
        "x": int,
        "y": str,
        "return": str
    }


def test_built_function_calls_callback(fake_mcp, fake_params):
    # Arrange
    builder = MCPFunctionBuilder(fake_mcp)
    built_func = builder.build(fake_params)

    # Act
    result = built_func(x=42, y="hello")

    # Assert
    fake_params.callback.assert_called_once_with(x=42, y="hello")
    assert result == "OK"


def test_signature_is_correct(fake_mcp, fake_params):
    # Arrange
    builder = MCPFunctionBuilder(fake_mcp)

    # Act
    built_func = builder.build(fake_params)
    sig = Signature.from_callable(built_func)

    # Assert
    param_names = list(sig.parameters.keys())
    assert param_names == ["x", "y"]
    assert sig.parameters["x"].annotation is int
    assert sig.parameters["y"].annotation is str
