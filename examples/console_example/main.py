from python_bot.bot import PythonBot
from python_bot.tests.common.middleware import EchoMiddleware
from python_bot.common.messenger.controllers.console import ConsoleMessenger

# Adding echo middleware which send message to bot the same as request

with PythonBot(middleware=[EchoMiddleware], messenger=[ConsoleMessenger]) as bot:
    # Simulate on message event
    bot.converse(quit="quit")
