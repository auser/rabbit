import json
import os
import tempfile
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv

from rabbit.logging import logger, setup_logging
from rabbit.utils import debug_json_response, get_definitions_url

load_dotenv() # Initial load


class RabbitMQ(object):
    env_files: list[str] = []
    verbose: bool = False
    from_host: str = "localhost"
    from_port: int = 15672
    from_username: str = os.getenv("RABBITMQ_FROM_USERNAME")
    from_password: str = os.getenv("RABBITMQ_FROM_PASSWORD")
    output: str | Path = "source_rabbitmq.json"
    to_host: str = "localhost"
    to_port: int = 5672
    to_username: str = os.getenv("RABBITMQ_TO_USERNAME")
    to_password: str = os.getenv("RABBITMQ_TO_PASSWORD")
    input: str | Path = "source_rabbitmq.json"

    def __init__(self, env_files: Optional[list[str]] = None, debug: bool = False):
        self.env_files = env_files
        self.debug = debug
        setup_logging(debug)
        load_env_files(self.env_files)

    async def download(self, output: Optional[str | Path] = None):
        """Download the rabbitmq configuration from the source host"""
        response = await self._make_request("get", (self.from_username, self.from_password), None)
        json_str = debug_json_response(response)

        if output is not None:
            with open(output, "w") as f:
                f.write(json_str)

    async def upload(self, input: Optional[str | Path] = None):
        """Upload the rabbitmq configuration to the target host"""
        if input is None:
            raise ValueError("Input file is required")

        with open(input, "r") as f:
            data = json.load(f)
        await self._make_request("put", (self.to_username, self.to_password), data)
        logger.info("Uploaded rabbitmq configuration")

    async def clone(self):
        """Clone the rabbitmq configuration from the source host to the target host"""
        logger.info("Downloading rabbitmq configuration from source host")
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        await self.download(temp_file.name)
        logger.info("Uploading rabbitmq configuration to target host")
        await self.upload(temp_file.name)
        logger.info("Cloned rabbitmq configuration")

    async def _make_request(self, method: str, auth: tuple[str, str], data: dict = None):
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json"
            }
            url = get_definitions_url(self.from_host, self.from_port)
            method_func = getattr(client, method.lower())
            kwargs = {"auth": auth, "headers": headers}
            if data is not None:
                kwargs["json"] = data
            response = await method_func(url, **kwargs)
            return response


# Helpers
def load_env_files(env_files):
    load_dotenv() # Default .env
    for env_file in env_files:
        load_dotenv(env_file)