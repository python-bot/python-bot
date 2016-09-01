from python_bot.common.webhook.request import BotRequest

__all__ = [
    "BotButtonMessage", "BotImageMessage", "BotMessage",
    "BotPersistentMenuMessage", "BotTextMessage", "BotTypingMessage"
]


class BotMessage:
    def __init__(self, request: BotRequest, **kwargs):
        self.request = request
        self.messenger = request.messenger
        self.kwargs = kwargs

    def to_json(self):
        pass


class BotButtonMessage(BotMessage):
    def __init__(self, request: BotRequest, text, buttons=None, **kwargs):
        super().__init__(request, **kwargs)
        if not buttons:
            buttons = []
        self.buttons = buttons
        self.text = text


class BotTextMessage(BotMessage):
    def __init__(self, request: BotRequest, text, quick_replies=None, **kwargs):
        super().__init__(request, **kwargs)
        if not quick_replies:
            quick_replies = []
        self.quick_replies = quick_replies
        self.text = text


class BotImageMessage(BotMessage):
    def __init__(self, request: BotRequest, url=None, path=None, **kwargs):
        super().__init__(request, **kwargs)
        self.url = url
        self.path = path


class BotPersistentMenuMessage(BotMessage):
    def __init__(self, request: BotRequest, call_to_actions=None, **kwargs):
        super().__init__(request)
        if not call_to_actions:
            call_to_actions = []
        self.call_to_actions = call_to_actions


class BotTypingMessage(BotMessage):
    def __init__(self, request, on=True, **kwargs):
        super().__init__(request, **kwargs)
        self.on = on
