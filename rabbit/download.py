
import httpx

from rabbit.utils import debug_json_response, get_definitions_url


async def download(args):
    async with httpx.AsyncClient() as client:
        headers = {
            "Content-Type": "application/json"
        }
        url = get_definitions_url(args["from_host"], args["from_port"])
        response = await client.get(url, auth=(args["username"], args["password"]), headers=headers)
        json_str = debug_json_response(response)
        
        if args["output"]:
            with open(args["output"], "w") as f:
                f.write(json_str)
