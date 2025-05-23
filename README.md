# CorahBot - Improved Bot for Corah IDLE RPG

An enhanced Python bot for automating gameplay in Corah IDLE RPG, featuring improved error handling, logging, and remote control capabilities.

## Features

- Robust error handling and retry mechanisms
- Comprehensive logging system with rotating file logs
- Modular architecture for easy maintenance and extensions
- REST API for remote control and monitoring
- Configurable settings and thresholds
- Graceful shutdown handling

## Requirements

- Python 3.7 or higher
- ADB (Android Debug Bridge)
- Waydroid container running Corah IDLE RPG

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd corahbot
```

2. Install the package:
```bash
pip install -e .
```

## Configuration

The bot's behavior can be configured by modifying `corahbot/config.py`. Key settings include:

- `DEVICE`: ADB device identifier
- `THRESH_DEFAULT/THRESH_ATTACK`: Template matching thresholds
- `RETRY_LIMIT`: Maximum retry attempts for actions
- `DEBUG_MODE`: Enable/disable debug logging
- `API_HOST/API_PORT`: REST API settings

## Usage

### Running the Bot

Start the bot directly:
```bash
corahbot
```

Or run with the API server:
```bash
corahbot-api
```

### API Endpoints

The REST API provides the following endpoints:

- `GET /status` - Get current bot status
- `POST /command` - Send control commands (start/stop)
- `GET /health` - API health check

Example API usage:
```bash
# Get bot status
curl http://localhost:8000/status

# Start the bot
curl -X POST http://localhost:8000/command -H "Content-Type: application/json" -d '{"command": "start"}'

# Stop the bot
curl -X POST http://localhost:8000/command -H "Content-Type: application/json" -d '{"command": "stop"}'
```

## Directory Structure

```
corahbot/
├── __init__.py      # Package initialization
├── config.py        # Configuration settings
├── logger.py        # Logging setup
├── templates.py     # Template management
├── actions.py       # Bot actions
├── main.py         # Main bot logic
└── api.py          # REST API
```

## Logging

Logs are stored in the configured `LOG_DIR` with daily rotation:
- Console output shows basic information
- Detailed logs are saved to files with format: `corahbot_YYYYMMDD.log`

## Error Handling

The bot includes several layers of error handling:
- Template verification before starting
- Action retry mechanisms
- Exception catching and logging
- Graceful shutdown on interruption

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original Corah IDLE RPG game developers
- Airtest framework developers
- FastAPI framework developers

## Support

For issues and feature requests, please use the GitHub issue tracker.
