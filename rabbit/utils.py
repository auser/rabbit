import json

from rabbit.logging import logger


def get_url(host, port):
    return f"http://{host}:{port}"

def get_definitions_url(host, port):
    url = f"{get_url(host, port)}/api/definitions"
    logger.debug(f"definitions url: {url}")
    return url

def debug_json_response(response):
  from pygments import highlight
  from pygments.formatters import TerminalFormatter
  from pygments.lexers import JsonLexer

  json_str = json.dumps(response.json(), indent=4, sort_keys=True)
  print(highlight(json_str, JsonLexer(), TerminalFormatter()))
  return json_str