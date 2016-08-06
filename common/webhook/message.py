class BotMessage:
    def __init__(self, request):
        self.request = request
        self.messenger = request.messenger

    def to_json(self):
        pass


class BotButtonMessage(BotMessage):
    def __init__(self, request, text, buttons=None):
        super().__init__(request)
        if not buttons:
            buttons = []
        self.buttons = buttons
        self.text = text


class BotTextMessage(BotMessage):
    def __init__(self, request, text, quick_replies=None):
        super().__init__(request)
        if not quick_replies:
            quick_replies = []
        self.quick_replies = quick_replies
        self.text = text


class BotImageMessage(BotMessage):
    def __init__(self, request, url=None, path=None):
        super().__init__(request)
        self.url = url
        self.path = path


class BotPersistentMenuMessage(BotMessage):
    def __init__(self, request, call_to_actions=None):
        super().__init__(request)
        if not call_to_actions:
            call_to_actions = []
        self.call_to_actions = call_to_actions


class BotTypingMessage(BotMessage):
    def __init__(self, request, on=True):
        super().__init__(request)
        self.on = on
