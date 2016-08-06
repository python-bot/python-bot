from python_bot.bot import PythonBot
from python_bot.common.messenger.controllers.console import ConsoleMessenger
from python_bot.settings import set_bot_settings

# Adding echo middleware which send message to bot the same as request
set_bot_settings(middleware={"python_bot.tests.common.middleware.EchoMiddleware": {}},
                 messenger={"python_bot.common.messenger.controllers.console.ConsoleMessenger": {}})

bot = PythonBot()
console_messenger_request = ConsoleMessenger().get_request(user_id=1, text="test")

# Simulate on message event
bot.on_message(console_messenger_request)
