import asyncio
from datetime import datetime

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
@click.option("--from-port", type=int, required=False, help="Port to download from")
@click.option("--to-host", "-t", type=str, required=False, help="Host to upload to")
@click.option("--to-port", type=int, required=False, help="Port to upload to")
@click.pass_context
def cli(ctx, env_file, verbose, from_host, from_port, to_host, to_port):
    # Create RabbitMQ instance with environment files and verbose level
    rmq = RabbitMQ(env_file, verbose)
    
    # Override with CLI arguments if provided (CLI takes precedence over env vars)
    if from_host is not None:
        rmq.from_host = from_host
    if from_port is not None:
        rmq.from_port = from_port
    if to_host is not None:
        rmq.to_host = to_host
    if to_port is not None:
        rmq.to_port = to_port
    
    ctx.obj = rmq

@cli.command(help="Download script for setting up rabbitmq")
@click.option("--output", "-o", type=str, required=False, help="Output file (defaults to env RABBITMQ_OUTPUT)")
@click.pass_obj
async def download(rmq, output):
    output_file = output or rmq.output
    logger.info(f"Downloading rabbitmq configuration from {rmq.from_host}:{rmq.from_port}")
    await rmq.download(output_file)

@cli.command(help="Upload script for setting up rabbitmq")
@click.option("--input", "-i", type=str, required=False, help="Input file (defaults to env RABBITMQ_INPUT)")
@click.pass_obj
async def upload(rmq, input):
    input_file = input or rmq.input
    logger.info("Uploading rabbitmq configuration")
    await rmq.upload(input_file)

@cli.command(help="Clone rabbitmq configuration from source to target")
@click.pass_obj
async def clone(rmq):
    logger.info("Cloning rabbitmq configuration")
    await rmq.clone()

@cli.command(help="Inspect RabbitMQ server and export detailed information")
@click.option("--host", type=str, required=False, help="RabbitMQ host to inspect (defaults to from-host)")
@click.option("--port", type=int, required=False, help="Management port (defaults to from-port)")
@click.option("--username", type=str, required=False, help="Username for authentication")
@click.option("--password", type=str, required=False, help="Password for authentication")
@click.option("--output", "-o", type=str, required=False, help="Output filename prefix (auto-generated if not provided)")
@click.option("--format", type=click.Choice(['excel', 'csv', 'json', 'all']), default='excel', help="Output format")
@click.option("--vhost", type=str, default='/', help="Virtual host to inspect")
@click.option("--ssl", is_flag=True, help="Use SSL connection")
@click.pass_obj
async def inspect(rmq, host, port, username, password, output, format, vhost, ssl):
    """Inspect a RabbitMQ server and export comprehensive information to spreadsheet"""
    
    # Use from_host/from_port as defaults if not specified
    inspect_host = host or rmq.from_host
    inspect_port = port or rmq.from_port
    inspect_username = username or rmq.from_username
    inspect_password = password or rmq.from_password
    
    logger.debug("CLI arguments received:")
    logger.debug(f"  host: {host} -> using: {inspect_host}")
    logger.debug(f"  port: {port} -> using: {inspect_port}")
    logger.debug(f"  username: {username} -> using: {inspect_username}")
    logger.debug(f"  format: {format}")
    logger.debug(f"  vhost: {vhost}")
    logger.debug(f"  ssl: {ssl}")
    
    # Generate default output filename if not provided
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        host_clean = inspect_host.replace('.', '_').replace(':', '_')
        output = f"rabbitmq_{host_clean}_{timestamp}"
    
    logger.info(f"Inspecting RabbitMQ server: {inspect_host}:{inspect_port}")
    logger.debug(f"Output will be saved as: {output}")
    
    try:
        await rmq.inspect_server(
            host=inspect_host,
            port=inspect_port,
            username=inspect_username,
            password=inspect_password,
            output=output,
            format=format,
            vhost=vhost,
            ssl=ssl
        )
        logger.info(f"✅ Inspection completed successfully! Output: {output}.*")
    except Exception as e:
        logger.error(f"❌ Inspection failed: {e}")
        if rmq.verbose > 0:  # Show traceback only in verbose mode
            import traceback
            logger.debug(traceback.format_exc())
        raise

@cli.command(help="Compare two RabbitMQ servers and show differences")
@click.option("--dev-host", type=str, required=False, help="Development RabbitMQ host (defaults to to-host)")
@click.option("--dev-port", type=int, required=False, help="Development management port (defaults to to-port)")
@click.option("--dev-username", type=str, required=False, help="Development username")
@click.option("--dev-password", type=str, required=False, help="Development password")
@click.option("--prod-host", type=str, required=False, help="Production RabbitMQ host (defaults to from-host)")
@click.option("--prod-port", type=int, required=False, help="Production management port (defaults to from-port)")
@click.option("--prod-username", type=str, required=False, help="Production username")
@click.option("--prod-password", type=str, required=False, help="Production password")
@click.option("--output", "-o", type=str, required=False, help="Output filename prefix")
@click.option("--format", type=click.Choice(['excel', 'csv', 'json', 'all']), default='excel', help="Output format")
@click.option("--ssl", is_flag=True, help="Use SSL for connections")
@click.pass_obj
async def compare(rmq, dev_host, dev_port, dev_username, dev_password, 
                 prod_host, prod_port, prod_username, prod_password, 
                 output, format, ssl):
    """Compare production and development RabbitMQ environments"""
    
    # Use configured hosts as defaults
    prod_host = prod_host or rmq.from_host
    prod_port = prod_port or rmq.from_port
    prod_username = prod_username or rmq.from_username
    prod_password = prod_password or rmq.from_password
    
    dev_host = dev_host or rmq.to_host
    dev_port = dev_port or rmq.to_port
    dev_username = dev_username or rmq.to_username
    dev_password = dev_password or rmq.to_password
    
    # Generate default output filename if not provided
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"rabbitmq_comparison_{timestamp}"
    
    logger.info("Comparing RabbitMQ environments:")
    logger.info(f"  Production:  {prod_host}:{prod_port}")
    logger.info(f"  Development: {dev_host}:{dev_port}")
    
    try:
        await rmq.compare_servers(
            prod_host=prod_host,
            prod_port=prod_port,
            prod_username=prod_username,
            prod_password=prod_password,
            dev_host=dev_host,
            dev_port=dev_port,
            dev_username=dev_username,
            dev_password=dev_password,
            output=output,
            format=format,
            ssl=ssl
        )
        logger.info(f"✅ Comparison completed successfully! Output: {output}.*")
    except Exception as e:
        logger.error(f"❌ Comparison failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(cli(auto_envvar_prefix="RABBITMQ"))