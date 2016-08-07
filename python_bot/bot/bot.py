from collections import OrderedDict

from python_bot.common.localization.handler import LocalizationMixIn
from python_bot.common.middleware.handler import MiddlewareHandlerMixIn
from python_bot.common.storage.base import StorageAdapter
from python_bot.common.tokenizer.base import BaseTokenizer
from python_bot.common.utils.misc import lazy
from python_bot.common.utils.path import load_module
from python_bot.common.webhook.request import BotRequest
from python_bot.settings import DEFAULT_BOT_SETTINGS


class BotHandlerMixIn:
    request_class = BotRequest

    @lazy
    def messengers(self):
        result = []
        for messenger in self.settings["messenger"]:
            params = messenger.get("params", {})
            params["on_message_callback"] = self.on_message
            params["bot"] = self
            mod = load_module({"entry": messenger["entry"], "params": params})
            result.append(mod)
        return result

    def bind(self):
        for messenger in self.messengers:
            messenger.bind(self)

    def unbind(self):
        for messenger in self.messengers:
            messenger.unbind(self)

    def on_message(self, request: BotRequest):
        message = self.get_message(request)
        return request.messenger.handle(message)


class PythonBot(LocalizationMixIn, MiddlewareHandlerMixIn, BotHandlerMixIn):
    def __init__(self, messenger=None, storage=None, user_storage=None, middleware=None, tokenizer=None):
        self._user_settings = {
            "messenger": messenger or OrderedDict(),
            "storage": storage or OrderedDict(),
            "user_storage": user_storage or OrderedDict(),
            "middleware": middleware or OrderedDict(),
            "tokenizer": tokenizer or OrderedDict()
        }
        super().__init__()

    @lazy
    def settings(self):
        _settings = DEFAULT_BOT_SETTINGS.copy()
        for k in _settings.keys():
            _settings[k].update(self._user_settings.get(k, {}))
        return _settings

    @lazy
    def storage(self) -> StorageAdapter:
        if get_bot_settings()["storage"]:
            first_item = next(iter(get_bot_settings()["storage"].items()))
            return load_module({"entry": first_item[0], "params": first_item[1]})

    @lazy
    def tokenizer(self) -> BaseTokenizer:
        if get_bot_settings()["tokenizer"]:
            first_item = next(iter(get_bot_settings()["tokenizer"].items()))
            return load_module({"entry": first_item[0], "params": first_item[1]})


if __name__ == "__main__":
    a = PythonBot()
    from python_bot.common.messenger.controllers.console import ConsoleMessenger

    r = ConsoleMessenger().get_request(1, "test")
    d = a.on_message(r)
