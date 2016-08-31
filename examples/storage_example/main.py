from python_bot.bot import PythonBot
from python_bot.common.storage.json_database import UserJsonDatabaseAdapter
from python_bot.common.webhook.message import BotTextMessage
from python_bot.common.webhook.request import BotRequest


def echo_middleware(get_message):

    def middleware(request: BotRequest):
        messages = get_message(request)

        # Get previous saved message for current user. User storage is persistent storage for each user.
        pre_message = request.user_storage.get("prev_message")

        message = "Previous message was: %s" % pre_message if pre_message else "Say hello"
        messages.append(BotTextMessage(request, message))

        request.user_storage.update("prev_message", request.text)

        return messages

    return middleware


# Adding example middleware which send message to bot with previous message
with PythonBot(
        middleware=[echo_middleware],
        messengers=[],
        user_storage=[UserJsonDatabaseAdapter, {"database_path": "./user.db"}]
) as bot:
    bot.converse()
