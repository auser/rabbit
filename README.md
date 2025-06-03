# RabbitMQ Cloner & Inspector

A comprehensive tool for cloning RabbitMQ configurations and inspecting RabbitMQ environments. Supports downloading/uploading configurations, comparing environments, and exporting detailed server analysis to Excel/CSV.

You should use an `.env` file to set the environment variables.

## Installation

This project uses [uv](https://docs.astral.sh/uv/) to install the dependencies. First install uv with the instructions listed [here](https://docs.astral.sh/uv/getting-started/installation/#installation-methods). Then install the dependencies with `uv sync`.

If you do not have a `.venv` directory, you can create one with `uv venv`.

```bash
uv venv
```

And then we'll need to sync the dependencies.

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

### Configuration Management

#### Download from a source host

```bash
python main.py download --from-host <host> --from-port <port> --from-username <username> --from-password <password>
```

#### Upload to a target host

```bash
python main.py upload --to-host <host> --to-port <port> --to-username <username> --to-password <password>
```

#### Clone from a source host to a target host

```bash
python main.py clone
```

### Server Inspection & Analysis

#### Inspect a single RabbitMQ server

Export comprehensive server information to Excel, CSV, or JSON formats:

```bash
# Basic inspection using configured host
python main.py --from-host prod.rabbitmq.com inspect

# Custom inspection with specific settings
python main.py inspect --host prod.rabbitmq.com --username admin --password secret --ssl

# Export to all formats with custom output name
python main.py inspect --host prod.rabbitmq.com --format all --output production_analysis

# Verbose output for debugging
python main.py -vvv inspect --host prod.rabbitmq.com
```

#### Compare two RabbitMQ environments

Compare production and development environments to identify differences:

```bash
# Basic comparison using configured hosts
python main.py --from-host prod.rabbitmq.com --to-host dev.rabbitmq.com compare

# Custom comparison with specific hosts
python main.py compare \
  --prod-host prod.rabbitmq.com --prod-username admin --prod-password secret \
  --dev-host dev.rabbitmq.com --dev-username devuser --dev-password devpass

# Export comparison to all formats
python main.py compare --format all --output env_comparison_2024
```

### Output Formats

- **Excel** (`.xlsx`): Multi-sheet workbook with formatted data (recommended for analysis)
- **CSV**: Separate files for each data type (good for programmatic processing)
- **JSON**: Raw data export (for automation/scripting)

### Exported Data

The inspection commands export comprehensive information including:

- **Summary**: Server overview, versions, and totals
- **Queues**: Message counts, consumer counts, durability settings, states
- **Exchanges**: Types, routing statistics, configurations
- **Consumers**: Active consumers with connection details and queue associations
- **Bindings**: Routing relationships between exchanges and queues
- **Connections**: Active connections with client information

### Finding Missing Consumers

To identify which consumers are running in production but not in development:

1. **Use the compare command**:
   ```bash
   python main.py compare --prod-host prod.rabbitmq.com --dev-host dev.rabbitmq.com
   ```

2. **Check the console output** for "Queues with consumers (prod only)"

3. **Open the Excel file** and look at:
   - **Comparison Summary** sheet for high-level differences
   - **Prod Consumers** vs **Dev Consumers** sheets for detailed comparison
   - **Prod Queues** vs **Dev Queues** sheets to see consumer counts

## Command Options

### Global Options

- `--from-host, -f`: Source RabbitMQ host
- `--from-port`: Source management port (default: 15672)
- `--to-host, -t`: Target RabbitMQ host (default: localhost)
- `--to-port`: Target port (default: 5672)
- `--verbose, -v`: Verbose output (use `-vvv` for debug level)
- `--env-file, -e`: Additional environment files to load

### Inspection Options

- `--host`: RabbitMQ host to inspect (defaults to from-host)
- `--port`: Management port (defaults to from-port)
- `--username`: Username for authentication
- `--password`: Password for authentication
- `--output, -o`: Output filename prefix
- `--format`: Export format (`excel`, `csv`, `json`, `all`)
- `--vhost`: Virtual host to inspect (default: `/`)
- `--ssl`: Use SSL connection

### Comparison Options

- `--prod-host`: Production RabbitMQ host
- `--prod-port`: Production management port
- `--prod-username`: Production username
- `--prod-password`: Production password
- `--dev-host`: Development RabbitMQ host
- `--dev-port`: Development management port
- `--dev-username`: Development username
- `--dev-password`: Development password

## Environment Variables

The following environment variables are supported:

### Connection Settings
- `RABBITMQ_FROM_HOST`: The host of the source RabbitMQ server
- `RABBITMQ_FROM_PORT`: The port of the source RabbitMQ server (default: 15672)
- `RABBITMQ_FROM_USERNAME`: The username of the source RabbitMQ server (default: guest)
- `RABBITMQ_FROM_PASSWORD`: The password of the source RabbitMQ server (default: guest)

### Target Settings (for cloning)
- `RABBITMQ_TO_HOST`: The host of the target RabbitMQ server (default: localhost)
- `RABBITMQ_TO_PORT`: The port of the target RabbitMQ server (default: 5672)
- `RABBITMQ_TO_USERNAME`: The username of the target RabbitMQ server (default: guest)
- `RABBITMQ_TO_PASSWORD`: The password of the target RabbitMQ server (default: guest)

### File Settings
- `RABBITMQ_INPUT`: Input configuration file (default: source_rabbitmq.json)

## Examples

### Typical Workflow

1. **Inspect production environment**:
   ```bash
   python main.py --from-host prod.rabbitmq.com -v inspect --output prod_analysis
   ```

2. **Inspect development environment**:
   ```bash
   python main.py --from-host dev.rabbitmq.com -v inspect --output dev_analysis
   ```

3. **Compare environments directly**:
   ```bash
   python main.py compare \
     --prod-host prod.rabbitmq.com \
     --dev-host dev.rabbitmq.com \
     --output comparison_report
   ```

4. **Open Excel files** to analyze differences in queues, consumers, and configurations

### Troubleshooting

If you're not seeing output:

1. **Check RabbitMQ Management Plugin**: Ensure the management plugin is enabled
2. **Verify Connectivity**: Test if `http://your-host:15672` is accessible
3. **Use Verbose Mode**: Add `-vvv` for detailed debug output
4. **Check Authentication**: Verify username/password are correct
5. **Network Access**: Ensure port 15672 is accessible from your machine

## Dependencies

- `asyncclick`: Async Click command-line interface
- `httpx`: Async HTTP client for API requests
- `pandas`: Data manipulation and analysis
- `openpyxl`: Excel file creation and formatting
- `python-dotenv`: Environment variable management

## Output Files

When you run inspection commands, you'll get files like:

- `rabbitmq_prod_20241203_143022.xlsx` - Excel workbook with multiple sheets
- `rabbitmq_prod_20241203_143022_summary.csv` - Server summary
- `rabbitmq_prod_20241203_143022_queues.csv` - Queue details
- `rabbitmq_prod_20241203_143022_consumers.csv` - Consumer information
- (and additional CSV files for exchanges, bindings, connections)

The Excel format is recommended as it organizes all data in a single file with properly formatted sheets.