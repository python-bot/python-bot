import logging

from python_bot.bot import PythonBot
from python_bot.bot.bot import bot_logger
from python_bot.common.messenger.controllers.telegram import TelegramMessenger
from python_bot.common.webhook.handlers.python_handler import PurePythonHandler
from python_bot.settings import WebHookSettings
from python_bot.tests.common.middleware import EchoMiddleware

# Getting Your Token
# From your Telegram client - connect to BotFather
# and basically follow the instructions on the Telegram website:
# https://core.telegram.org/bots#3-how-do-i-create-a-bot

ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

# For development purposes, we will use Ngrok that sets up secure tunnels to our localhost i.e.
# Ngrok gives web accessible URLs and tunnels all traffic from that URL to our localhost!
# Go to Ngrok's download page https://ngrok.com/download, download the zip file, unzip and simply run the command
# ./ngrok http 8000
# Now any outside computer can reach your localhost server at https://{unique_id}.ngrok.io
# Copy this unique_id to NGROK_URL

NGROK_URL = 'https://{unique_id}.ngrok.io'


# Now we need to ovveride web hook url to our NGROK_URL
class MyTelegramMessenger(TelegramMessenger):
    def set_web_hook_url(self, web_hook_url):
        super().set_web_hook_url(NGROK_URL)


bot_logger.setLevel(logging.DEBUG)


with PythonBot(
        middleware=[EchoMiddleware],
        messengers=[
            (
                    MyTelegramMessenger,
                    {
                        "access_token": ACCESS_TOKEN,
                        # also due to NGROK, we need to override base server path
                        "base_path": '/'
                    }
            )
        ],
        web_hook=[PurePythonHandler, {
            "settings":
                WebHookSettings(
                    '127.0.0.1'
                )
        }]
) as bot:
    bot.wait()
