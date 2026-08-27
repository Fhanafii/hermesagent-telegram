# Hermes Agent Telegram

A Python-based Telegram bot implementation powered by Hermes Agent, providing intelligent conversational capabilities through Telegram messaging platform.

## 🚀 Features

- **Telegram Integration**: Seamless integration with Telegram Bot API
- **AI-Powered Responses**: Leverages Hermes Agent for intelligent message processing
- **Asynchronous Operation**: Built with async/await for efficient message handling
- **Easy Configuration**: Simple setup and configuration process
- **Extensible Architecture**: Easily add custom handlers and features

## 📋 Prerequisites

- Python 3.8 or higher
- Telegram Bot API Token (from [@BotFather](https://t.me/botfather))
- Hermes Agent dependencies

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Fhanafii/hermesagent-telegram.git
cd hermesagent-telegram
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Setting Up Your Telegram Bot

1. Open Telegram and chat with [@BotFather](https://t.me/botfather)
2. Create a new bot using `/newbot` command
3. Copy your Bot API Token

### Environment Variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
HERMES_API_KEY=your_hermes_api_key_here
LOG_LEVEL=INFO
```

## 🎯 Usage

### Starting the Bot

```bash
python main.py
```

### Command Examples

Once the bot is running, you can interact with it through Telegram:

- `/start` - Start the bot and receive welcome message
- `/help` - Get help and available commands
- `/info` - Get information about the bot

Send any message for the bot to process and respond intelligently using Hermes Agent.

## 📁 Project Structure

```
hermesagent-telegram/
├── main.py                 # Entry point of the application
├── config.py              # Configuration settings
├── handlers/              # Message handlers and command processors
│   ├── __init__.py
│   ├── message_handler.py # Main message processing
│   └── command_handler.py # Command handling
├── agents/                # Hermes Agent integration
│   ├── __init__.py
│   └── hermes_agent.py    # Agent logic
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── logger.py          # Logging configuration
│   └── helpers.py         # Helper functions
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # This file
```

## 🔌 Dependencies

Key dependencies include:

- **python-telegram-bot**: Telegram Bot API wrapper
- **python-dotenv**: Environment variable management
- **aiohttp**: Asynchronous HTTP client
- **pydantic**: Data validation using Python type annotations

For complete list, see `requirements.txt`

## 💬 Message Processing

The bot processes messages in the following pipeline:

1. **Receive**: Message arrives from Telegram
2. **Parse**: Extract content and metadata
3. **Agent Processing**: Hermes Agent analyzes and processes the message
4. **Response Generation**: Generate appropriate response
5. **Send**: Reply back to the user on Telegram

## 🛠️ Development

### Adding Custom Handlers

Create new handler files in the `handlers/` directory:

```python
async def handle_custom_command(update, context):
    """Custom command handler"""
    message = update.message.text
    # Process message
    await update.message.reply_text("Response")
```

### Extending the Agent

Modify `agents/hermes_agent.py` to customize agent behavior:

```python
class CustomHermesAgent(HermesAgent):
    async def process_message(self, message):
        # Custom processing logic
        return await super().process_message(message)
```

## 📝 Logging

The application includes comprehensive logging. Configure logging level in `.env`:

```env
LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

Logs are output to both console and log file (if configured).

## 🚨 Error Handling

The bot includes robust error handling for:

- Network failures
- Invalid messages
- API timeouts
- Malformed requests

Errors are logged and gracefully handled without crashing the bot.

## 🔐 Security

- **Token Security**: Never commit `.env` file with actual tokens
- **Input Validation**: All user inputs are validated
- **Rate Limiting**: Implements rate limiting to prevent abuse
- **Error Messages**: Safe error messages that don't expose sensitive info

## 📦 Building & Deployment

### Local Testing

```bash
python main.py
```

### Deployment Options

- **Local Server**: Run on your machine
- **VPS/Cloud Server**: Deploy to AWS, Heroku, or similar services
- **Docker**: Containerize the application for easy deployment

#### Docker Deployment (Optional)

```bash
docker build -t hermesagent-telegram .
docker run -d --env-file .env hermesagent-telegram
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License - see the LICENSE file for details.

## 📞 Support & Contact

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/Fhanafii/hermesagent-telegram/issues)
- **Author**: [Fhanafii](https://github.com/Fhanafii)
- **Repository**: [hermesagent-telegram](https://github.com/Fhanafii/hermesagent-telegram)

## 🗺️ Roadmap

- [ ] Advanced message filtering
- [ ] User authentication system
- [ ] Message history storage
- [ ] Database integration
- [ ] Web dashboard
- [ ] Multi-language support
- [ ] Performance optimizations

## 📚 Additional Resources

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

---

**Last Updated**: August 2026

**Status**: Active Development

Feel free to reach out with questions or suggestions!
