import emoji

from python_bot.common.middleware.base import MiddlewareMixin
from python_bot.common.webhook.request import BotRequest


class EmojiMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        self.use_aliases = kwargs.pop("use_aliases", False)
        super().__init__(*args, **kwargs)

    def process_message(self, _: BotRequest, messages):
        for message in messages:
            if hasattr(message, "text"):
                message.text = emoji.emojize(message.text, use_aliases=self.use_aliases)

        return messages

    def process_request(self, request: BotRequest):
        request.text = emoji.emojize(request.text, use_aliases=self.use_aliases)
