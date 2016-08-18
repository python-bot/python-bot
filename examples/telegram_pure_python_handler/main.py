from python_bot.common.webhook.handlers.python_handler import PurePythonHandler
from python_bot.bot import PythonBot
from python_bot.common.messenger.controllers.console import ConsoleMessenger
from python_bot.common.webhook.message import BotTextMessage
from python_bot.tests.common.middleware import EchoMiddleware


with PythonBot(
    middleware=[EchoMiddleware],
    messenger=[TelegramMessenger]
) as bot:
    console_messenger_request = ConsoleMessenger().get_request(user_id=1, text="test")

    # Simulate on message event
    bot.on_message(console_messenger_request)
