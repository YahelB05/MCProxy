import logging
import os
from typing import Optional

from mcp_proxy.models import mcp_endpoints_schema


class ConfigurationDeserializer:
    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path

    def deserialize_json_config(self) -> Optional[mcp_endpoints_schema.ApiConfig]:
        if not os.path.exists(self.config_file_path):
            logging.warning(f"Path [{self.config_file_path}] does not exist.")
            return None

        try:
            logging.debug(f"Loading configuration: {self.config_file_path}")
            with open(self.config_file_path, 'r') as f:
                content = f.read()
                return mcp_endpoints_schema.ApiConfig.from_json(content)
        except ValueError as e:
            logging.warning(e)
            return None
