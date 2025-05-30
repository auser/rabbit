# RabbitMQ Cloner

You should use an `.env` file to set the environment variables.

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
