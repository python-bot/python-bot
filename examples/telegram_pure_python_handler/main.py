import logging

from python_bot.bot import PythonBot
from python_bot.bot.bot import bot_logger
from python_bot.common.messenger.controllers.telegram import TelegramMessenger
from python_bot.common.webhook.handlers.python_handler import PurePythonHandler
from python_bot.settings import WebHookSettings
from python_bot.tests.common.middleware import EchoMiddleware

ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
bot_logger.setLevel(logging.DEBUG)
with PythonBot(
        middleware=[EchoMiddleware],
        messenger=[
            (TelegramMessenger, {"access_token": ACCESS_TOKEN})
        ],
        web_hook=[PurePythonHandler, {"settings": WebHookSettings('127.0.0.1')}]
) as bot:
    bot.wait()
