from python_bot.common.utils.misc import lazy
from python_bot.common.utils.path import load_module
from python_bot.common.webhook.message import BotMessage
from python_bot.settings import BOT_SETTINGS


class MiddlewareHandlerMixIn(object):
    def __init__(self):
        self._middleware_chain = None

    @lazy
    def middleware(self):
        if self._middleware_chain:
            return self._middleware_chain

        handler = self._get_message
        for middleware in reversed(list(BOT_SETTINGS["middleware"].keys())):
            params = BOT_SETTINGS["middleware"][middleware]
            params["get_message"] = handler

            handler = load_module({"entry": middleware, "params": params})

        # We only assign to this when initialization is complete as it is used
        # as a flag for initialization being complete.
        self._middleware_chain = handler
        return self._middleware_chain

    def get_message(self, request):
        message = self.middleware(request)
        return message

    def _get_message(self, request):
        return []
