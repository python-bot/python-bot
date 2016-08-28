from python_bot.bot import PythonBot
from python_bot.common.storage.json_database import UserJsonDatabaseAdapter
from python_bot.common.webhook.message import BotTextMessage
from python_bot.common.webhook.request import BotRequest


def echo_middleware(get_message):

    def middleware(request: BotRequest):
        messages = get_message(request)
        pre_message = request.user_storage.get("prev_message", "Previous message now found. Say hello")

        messages.append(BotTextMessage(request, pre_message))
        request.user_storage.update("prev_message", "Previous message was: %s" % request.text)

        return messages

    return middleware


# Adding example middleware which send message to bot with previous message
with PythonBot(
        middleware=[echo_middleware],
        messengers=[],
        user_storage=[UserJsonDatabaseAdapter, {"database_path": "./user.db"}]
) as bot:
    bot.converse()
