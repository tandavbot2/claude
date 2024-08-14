# Auto Approve Telegram Bot

This Telegram bot automatically approves join requests for groups and channels, manages user subscriptions to required channels, and provides admin utilities.

## Features

- Auto-approve join requests for groups and channels
- Force users to subscribe to specified channels before joining
- Remove users who leave required channels
- Broadcast messages to all users
- Ban and unban users
- User and group statistics
- Configurable via environment variables

## Requirements

- Python 3.10+
- MongoDB database
- Telegram Bot API token

## Installation

1. Clone the repository: https://github.com/tandavbot2/claude
2. Install the required packages:
3. Set up environment variables:
Create a `.env` file in the root directory and add the following variables:
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
MONGO_URI=your_mongodb_uri
CHID=your_force_subscribe_channel_id
FSUB=your_force_subscribe_channel_username
SUDO=comma_separated_admin_user_ids
REQUIRED_CHANNELS=comma_separated_required_channel_usernames
BOT_NAME=YourBotName
BOT_USERNAME=YourBotUsername

## Usage

To run the bot locally: python bot.py

## Deployment

### Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/tandavbot2/claude)

### Docker

1. Build the Docker image: docker build -t auto-approve-bot
2. Run the container: docker run -d --env-file .env auto-approve-bot

### Okteto

1. Install Okteto CLI and login to your Okteto account.
2. Run the following command in the project directory: okteto deploy

## Commands

- `/start` - Start the bot and check if user is subscribed to required channels
- `/users` - Get the count of users and groups (admin only)
- `/bcast` - Broadcast a message to all users (admin only)
- `/fcast` - Forward a message to all users (admin only)
- `/ban` - Ban a user from the group (admin only)
- `/unban` - Unban a user from the group (admin only)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Pyrogram](https://docs.pyrogram.org/) - MTProto API Python framework
- [MongoDB](https://www.mongodb.com/) - Database
- [Flask](https://flask.palletsprojects.com/) - Web framework for keeping the bot alive

## Support

For support, join our [Telegram support group](https://t.me/TandavBots_Support).

## Disclaimer

This bot is provided as-is, without any warranty. Use at your own risk. The developers are not responsible for any misuse or damage caused by this bot.
