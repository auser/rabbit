import asyncio
import os

import asyncclick as click
from dotenv import load_dotenv

from rabbit.logging import logger
from rabbit.rabbitmq import RabbitMQ

load_dotenv()

pass_rabbitmq = click.make_pass_decorator(RabbitMQ, ensure=True)

@click.group()
@click.option("--env-file", "-e", type=str, required=False, multiple=True, help="Environment file")
@click.option("--verbose", '-v', count=True, required=False, default=0, help="Verbose mode")
@click.option("--from-host", "-f", type=str, required=False, help="Host to download from")
@click.option("--from-port", "-p", type=int, required=False, default=15672, help="Port to download from")
@click.option("--to-host", "-t", type=str, required=False, default="localhost", help="Host to upload to")
@click.option("--to-port", "-p", type=int, required=False, default=5672, help="Port to upload to")
@click.pass_context
def cli(ctx, env_file, verbose, from_host, from_port, to_host, to_port):
    rmq = RabbitMQ(env_file, verbose)
    rmq.from_host = from_host if from_host is not None else os.getenv("RABBITMQ_FROM_HOST", "localhost")
    rmq.from_port = from_port if from_port is not None else os.getenv("RABBITMQ_FROM_PORT", 15672)
    rmq.to_host = to_host if to_host is not None else os.getenv("RABBITMQ_TO_HOST", "localhost")
    rmq.to_port = to_port if to_port is not None else os.getenv("RABBITMQ_TO_PORT", 5672)
    rmq.input = os.getenv("RABBITMQ_INPUT", "source_rabbitmq.json")
    ctx.obj = rmq

@cli.command(help="Download script for setting up rabbitmq")
@click.option("--output", "-o", type=str, required=False, default="source_rabbitmq.json", help="Output file")
@click.pass_obj
async def download(rmq, output):
    logger.info(f"Downloading rabbitmq configuration from {rmq.from_host}:{rmq.from_port}")
    await rmq.download(output)

@cli.command(help="Upload script for setting up rabbitmq")
@click.option("--input", "-i", type=str, required=False, default="source_rabbitmq.json", help="Input file")
@click.pass_obj
async def upload(rmq, input):
    logger.info("Uploading rabbitmq configuration")
    await rmq.upload(input)

@cli.command(help="Upload script for setting up rabbitmq")
@click.pass_obj
async def clone(rmq):
    logger.info("Cloning rabbitmq configuration")
    await rmq.clone()


if __name__ == "__main__":
    asyncio.run(cli(auto_envvar_prefix="RABBITMQ"))
