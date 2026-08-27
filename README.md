# Hermes Sysadmin Agent

A small Python sysadmin service for managing a server through Telegram and MCP. It is designed to be used as a tool provider for Hermes Agent, with Docker and host observability tools behind a security gate.

## Project status

This project is in active development.

The Telegram path can ask an authorized user to confirm high-risk Docker operations with inline buttons. The MCP path can correctly detect and refuse unconfirmed destructive operations, but the current Hermes MCP integration does not provide a way to route that confirmation request back through Telegram and resume the pending tool call. As a result, destructive MCP calls remain blocked until that integration issue is resolved.

Read-only MCP tools are usable directly.

## What it provides

- Server status: CPU, memory, disk, and uptime
- Memory and swap usage
- Disk usage
- Running Docker containers
- Recent Docker container logs
- Server or ESP32CAM error log output
- Docker container start, stop, and restart operations
- Telegram user allowlisting with `ALLOWED_USER_IDS`
- Risk-based tool policies and confirmation tokens

## Architecture

```text
Telegram -> bot.py -> ToolExecutor -> SecurityGate -> host / Docker

Hermes Agent -> MCP stdio server -> ToolExecutor -> SecurityGate -> host / Docker
                                      |
                                      +-- low risk: execute
                                      +-- high risk: confirmation_required
```

The shared `ToolExecutor` and `SecurityGate` ensure that tools are not executed merely because they are exposed through MCP. Every registered tool must also have a security policy.

## Requirements

- Python 3.12 or newer
- A Linux server is recommended for the host metrics and Docker workflow
- Docker, when using Docker tools
- A Telegram bot token, when using the Telegram bot
- The MCP server/runtime expected by the Hermes installation, when using MCP

Runtime dependencies are currently not declared in `pyproject.toml`. Install the packages required by the selected entry point in your virtual environment, for example:

```powershell
python -m pip install python-dotenv psutil python-telegram-bot pytest
```

Install the MCP package/version supported by your Hermes setup separately. The MCP API used by this project is `MCPServer` with `run_stdio_async()`.

## Installation

```powershell
git clone https://github.com/Fhanafii/hermesagent-telegram.git
Set-Location hermesagent-telegram

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install python-dotenv psutil python-telegram-bot pytest
```

On Linux or macOS, activate the environment with:

```bash
source .venv/bin/activate
```

## Configuration

Create a `.env` file in the project root. Do not commit it.

```env
TELEGRAM_BOT_TOKEN=replace_with_your_bot_token
ALLOWED_USER_IDS=123456789,987654321
```

`ALLOWED_USER_IDS` is a comma-separated list of Telegram numeric user IDs. Users not in this list cannot use the Telegram bot. `HERMES_API_KEY` and `LOG_LEVEL` are not read by the current implementation.

## Running the project

### Telegram bot

The Telegram bot provides read-only commands and a confirmation flow for `/restart`:

```powershell
python bot.py
```

Available commands:

| Command | Purpose |
| --- | --- |
| `/start` | Show server status |
| `/status` | Show CPU, memory, disk, and uptime |
| `/memory` | Show RAM and swap usage |
| `/disk` | Show disk usage |
| `/docker` | List Docker containers |
| `/logs <container>` | Show recent container logs |
| `/restart <container>` | Request confirmation, then restart a container |

### MCP server

The MCP server communicates over stdio and is intended to be launched by an MCP client such as Hermes Agent:

```powershell
python -m mcp.server
```

Configure the MCP client to launch that command from the repository directory. The exact configuration format depends on the Hermes version and MCP client being used.

## Tool inventory

| Tool | Risk | Confirmation |
| --- | --- | --- |
| `get_server_status` | Low | No |
| `get_memory` | Low | No |
| `get_disk` | Low | No |
| `get_docker_containers` | Low | No |
| `get_container_logs` | Low | No |
| `get_error_log` | Low | No |
| `start_container` | High | Yes |
| `stop_container` | High | Yes |
| `restart_container` | High | Yes |

Unknown tools and tools without a policy are rejected. Tool failures are returned as structured error results instead of being allowed to crash the server.

## Confirmation and security model

1. A tool call is looked up in the registry.
2. The tool must have a matching policy.
3. Low-risk tools execute immediately.
4. High-risk tools return `confirmation_required` unless `confirmed=True`.
5. The Telegram bot creates a short-lived, user-bound confirmation token and displays Confirm and Cancel buttons.
6. A confirmation token expires after 120 seconds and can only be consumed by the Telegram user who created it.

The confirmation layer is an application-level safeguard, not a replacement for least-privilege OS permissions, Docker permissions, firewalling, backups, or server access controls.

## Project structure

```text
hermesagent-telegram/
├── bot.py                 # Telegram entry point and confirmation callbacks
├── agent/executor.py      # Shared tool execution and result statuses
├── mcp/server.py          # MCP stdio tool server
├── security/
│   ├── auth.py            # Telegram user allowlist
│   ├── confirmation.py   # Expiring Telegram confirmation tokens
│   ├── gate.py            # Tool and policy enforcement
│   └── policy.py          # Risk levels and confirmation policies
├── tools/
│   ├── docker.py          # Docker operations
│   ├── log.py             # Error log reader
│   ├── registry.py        # Tool registration and dispatch
│   ├── schema.py          # Tool schemas
│   └── system.py          # Host metrics
├── tests/test_tools.py    # Registry, policy, and validation tests
├── docs.MD                # Architecture notes
└── pyproject.toml         # Package metadata
```

## Testing

Run the current test suite with:

```powershell
python -m pytest
```

The tests cover registration, schemas, confirmation policies, unknown tools, and invalid container access. Docker integration tests are not currently included.
