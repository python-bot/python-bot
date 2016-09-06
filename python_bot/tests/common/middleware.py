from python_bot.common.middleware.base import MiddlewareMixin
from python_bot.common.webhook.message import BotTextResponse
from python_bot.common.webhook.request import BotRequest


class EchoMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_message(self, request: BotRequest, messages):
        messages.append(BotTextResponse(request, request.text))
        return messages

    def process_request(self, request: BotRequest):
        pass
