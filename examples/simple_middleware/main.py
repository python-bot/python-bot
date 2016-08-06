from python_bot.bot import PythonBot
from python_bot.common.messenger.controllers.console import ConsoleMessenger
from python_bot.common.webhook.message import BotTextMessage
from python_bot.settings import set_bot_settings


def echo_middleware(get_message):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        messages = get_message(request)
        messages.append(BotTextMessage(request, request.text))
        # Code to be executed for each request/response after
        # the view is called.

        return messages

    return middleware

# Adding echo middleware which send message to bot the same as request
set_bot_settings(middleware={"echo_middleware": echo_middleware},
                 messenger={"python_bot.common.messenger.controllers.console.ConsoleMessenger": {}})

bot = PythonBot()
console_messenger_request = ConsoleMessenger().get_request(user_id=1, text="test")

# Simulate on message event
bot.on_message(console_messenger_request)
