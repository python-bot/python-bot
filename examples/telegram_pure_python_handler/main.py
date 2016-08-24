from python_bot.bot import PythonBot
from python_bot.common.messenger.controllers.telegram import TelegramMessenger
from python_bot.common.webhook.handlers.python_handler import PurePythonHandler
from python_bot.settings import WebHookSettings
from python_bot.tests.common.middleware import EchoMiddleware

with PythonBot(
        middleware=[EchoMiddleware],
        messenger=[TelegramMessenger],
        web_hook=[PurePythonHandler, {"settings": WebHookSettings('127.0.0.1')}]
) as bot:
    bot.wait()
