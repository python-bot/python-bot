from python_bot.bot import PythonBot
from python_bot.common.messenger.controllers.console import ConsoleMessenger

# Adding echo middleware which send message to bot the same as request
bot = PythonBot(middleware={"python_bot.tests.common.middleware.EchoMiddleware": {}},
                messenger={"python_bot.common.messenger.controllers.console.ConsoleMessenger": {}})
console_messenger_request = ConsoleMessenger().get_request(user_id=1, text="test")

# Simulate on message event
bot.on_message(console_messenger_request)
