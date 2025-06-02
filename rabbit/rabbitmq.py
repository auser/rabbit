import json
import tempfile
from pathlib import Path
from typing import Optional

import httpx
from dotenv import dotenv_values, load_dotenv

from rabbit.logging import logger, setup_logging
from rabbit.utils import get_definitions_url

load_dotenv() # Initial load

values = dotenv_values()

class RabbitMQ(object):
    env_files: list[str] = []
    verbose: bool = False
    from_host: str = "localhost"
    from_port: int = 15672
    from_username: str = values.get("RABBITMQ_FROM_USERNAME", "guest")
    from_password: str = values.get("RABBITMQ_FROM_PASSWORD", "guest")
    output: str | Path = "source_rabbitmq.json"
    to_host: str = "localhost"
    to_port: int = 5672
    to_username: str = values.get("RABBITMQ_TO_USERNAME", "guest")
    to_password: str = values.get("RABBITMQ_TO_PASSWORD", "guest")
    input: str | Path = "source_rabbitmq.json"

    def __init__(self, env_files: Optional[list[str]] = None, debug: bool = False):
        self.env_files = env_files
        self.debug = debug
        print(debug)
        setup_logging(debug)
        load_env_files(self.env_files)

    async def download(self, output: Optional[str | Path] = None):
        """Download the rabbitmq configuration from the source host"""
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json"
            }
            url = get_definitions_url(self.from_host, self.from_port)
            logger.info(f"Downloading rabbitmq configuration from {url}")
            kwargs = {"auth": (self.from_username, self.from_password), "headers": headers}
            response = await client.get(url, **kwargs)
            json_str = response.text

        if output is not None:
            with open(output, "w") as f:
                f.write(json_str)

    async def upload(self, input: Optional[str | Path] = None):
        """Upload the rabbitmq configuration to the target host"""
        if input is None:
            raise ValueError("Input file is required")

        with open(input, "r") as f:
            data = json.load(f)

        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json"
            }
            url = get_definitions_url(self.to_host, self.to_port)
            logger.info(f"Uploading rabbitmq configuration to {url}")
            kwargs = {"auth": (self.to_username, self.to_password), "headers": headers}
            response = await client.post(url, json=data, **kwargs)
            print(response.text)
        # await self._make_request("post", (self.to_username, self.to_password), data, input)
        logger.info("Uploaded rabbitmq configuration")

    async def clone(self):
        """Clone the rabbitmq configuration from the source host to the target host"""
        logger.info("Downloading rabbitmq configuration from source host")
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        await self.download(temp_file.name)
        logger.info("Uploading rabbitmq configuration to target host")
        await self.upload(temp_file.name)
        logger.info("Cloned rabbitmq configuration")

# Helpers
def load_env_files(env_files):
    load_dotenv() # Default .env
    for env_file in env_files:
        load_dotenv(env_file)