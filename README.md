# RabbitMQ Cloner

You should use an `.env` file to set the environment variables.

## Installation

This project uses [uv](https://docs.astral.sh/uv/) to install the dependencies. First install uv with `pip install uv`. Then install the dependencies with `uv sync`.

```bash
uv sync
```

And activate the venv with `uv venv`.

```bash
source .venv/bin/activate
```

**Important**: Copy the `.env.example` file to `.env` and set the environment variables.

```bash
cp .env.example .env
```

## Usage

### Download from a source host

```bash
python main.py download --from-host <host> --from-port <port> --from-username <username> --from-password <password>
```

### Upload to a target host

```bash
python main.py upload --to-host <host> --to-port <port> --to-username <username> --to-password <password>
```

### Clone from a source host to a target host

```bash
python main.py clone
```

## Environment Variables

The following environment variables are supported:

- `RABBITMQ_FROM_HOST`: The host of the source RabbitMQ server.
- `RABBITMQ_FROM_PORT`: The port of the source RabbitMQ server.
- `RABBITMQ_FROM_USERNAME`: The username of the source RabbitMQ server.
- `RABBITMQ_FROM_PASSWORD`: The password of the source RabbitMQ server.
