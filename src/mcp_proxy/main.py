import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

from mcp_proxy.logic.builders.callback_function_builder import EndpointHttpCaller
from mcp_proxy.logic.builders.mcp_function_builder import MCPFunctionBuilder
from mcp_proxy.logic.deserializers.config_deserializer import ConfigurationDeserializer
from mcp_proxy.logic.utils import parsing_utils
from mcp_proxy.models import function_params

DEFAULT_CONFIG_FILE_PATH = "config.json"

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
mcp = FastMCP("PROXY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.debug("Starting application lifespan setup...")

    config_deserializer = ConfigurationDeserializer(
        os.environ.get("CONFIG_FILE") or DEFAULT_CONFIG_FILE_PATH
    )
    config = config_deserializer.deserialize_json_config()

    if not config:
        raise ValueError("Configuration Error.")
    logging.debug(f"Loaded configuration successfully. Configuration version: {config.version}")

    mcp_functions = []
    for endpoint in config.endpoints:
        logging.debug(f"[{endpoint.url}] Creating MCP proxy")
        params = function_params.FunctionParams(
            name=endpoint.name,
            doc=endpoint.description,
            param_types=parsing_utils.extract_param_types(endpoint),
            return_type=str,
            callback=EndpointHttpCaller(endpoint)
        )
        logging.debug(f"[{endpoint.url}] Function parameters: {params}")

        builder = MCPFunctionBuilder(mcp)
        mcp_function = builder.build(params)
        mcp_functions.append(mcp_function)
        logging.debug(f"[{endpoint.url}] Created MCP function")

    # run the MCP session manager asynchronously
    # mcp.session_manager.run() returns an async context manager
    async with mcp.session_manager.run():
        logging.debug("MCP session manager running.")
        yield  # App runs here

    logging.debug("Application shutting down.")


app = FastAPI(title="MCP-PROXY-API", lifespan=lifespan)
app.mount("/", mcp.streamable_http_app())
