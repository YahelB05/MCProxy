from inspect import Signature, Parameter
from typing import Any

import makefun
from mcp.server.fastmcp import FastMCP

from mcp_proxy.models import function_params


class MCPFunctionBuilder:
    def __init__(self, mcp_instance: FastMCP[Any]):
        self.mcp = mcp_instance

    def build(self, params: function_params.FunctionParams):
        # This is the function that will actually be called
        def callback_template(**kwargs: Any):
                return params.callback(**kwargs)

        # Build Signature from param_types
        sig = Signature(parameters=[
            Parameter(name, kind=Parameter.POSITIONAL_OR_KEYWORD, annotation=typ)
            for name, typ in params.param_types.items()
        ])

        # Create the function with explicit named params
        func = makefun.create_function(
            sig,
            callback_template
        )

        # Set metadata
        func.__name__ = params.name
        func.__doc__ = params.doc
        func.__annotations__ = {**params.param_types, 'return': params.return_type}

        return self.mcp.tool()(func)
