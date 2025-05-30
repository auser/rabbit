import json

import httpx

from rabbit.logging import logger
from rabbit.utils import get_definitions_url


async def upload(args):
    try:
        with open(args["input"], "r") as f:
            data = f.read()

        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json"
            }
            async with httpx.AsyncClient() as client:
                url = get_definitions_url(args["to_host"], args["to_port"])
                response = await client.post(
                    url,
                    auth=(args["username"], args["password"]),
                    headers=headers,
                    json=json.loads(data)
                )
                logger.debug(f"Uploaded rabbitmq configuration to {args['to_host']}:{args['to_port']}")
                logger.debug(response.text)
    except FileNotFoundError:
        print(f"File {args.input} not found")
        return