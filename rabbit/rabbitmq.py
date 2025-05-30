import json
import os
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
    from_username: str = os.getenv("RABBITMQ_USERNAME")
    from_password: str = os.getenv("RABBITMQ_PASSWORD")
    output: str | Path = "source_rabbitmq.json"
    to_host: str = "localhost"
    to_port: int = 5672
    to_username: str = os.getenv("RABBITMQ_USERNAME")
    to_password: str = os.getenv("RABBITMQ_PASSWORD")
    input: str | Path = "source_rabbitmq.json"

    def __init__(self, env_files: Optional[list[str]] = None, debug: bool = False):
        self.env_files = env_files
        self.debug = debug
        setup_logging(debug)

        for env_file in self.env_files:
            load_dotenv(env_file)

    def get_env_files(self):
        return self.env_files

    async def download(self, output: Optional[str | Path] = None):
        response = await self.make_request("get", (self.from_username, self.from_password), None)
        json_str = debug_json_response(response)

        if output is not None:
            with open(output, "w") as f:
                f.write(json_str)


    async def upload(self, input: Optional[str | Path] = None):
        if input is None:
            raise ValueError("Input file is required")

        with open(input, "r") as f:
            data = json.load(f)
        await self.make_request("put", (self.to_username, self.to_password), data)
        logger.info("Uploaded rabbitmq configuration")

    async def make_request(self, method: str, auth: tuple[str, str], data: dict = None):
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

