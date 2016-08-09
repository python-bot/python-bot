from collections import OrderedDict

import time

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
        for entry in self.settings["messenger"]:
            if isinstance(entry, (list, tuple)):
                params = entry[1]
                entry = entry[0]
            else:
                params = {}

            if "on_message_callback" in params:
                params["on_message_callback"] = self.on_message
            params["bot"] = self

            mod = None
            if isinstance(entry, str):
                mod = load_module({"entry": entry, "params": params})
            elif callable(entry):
                mod = entry(**params)

            if mod:
                result.append(mod)
        return result

    def bind(self):
        for messenger in self.messengers:
            messenger.bind()

    def unbind(self):
        for messenger in self.messengers:
            messenger.unbind()

    def wait(self):
        while True:
            time.sleep(0.3)

    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                from python_bot.common.messenger.controllers.console import ConsoleMessenger
                request = ConsoleMessenger().get_request(1, user_input)
                self.on_message(request)

    def on_message(self, request: BotRequest):
        message = self.get_message(request)
        return request.messenger.handle(message)


class PythonBot(LocalizationMixIn, MiddlewareHandlerMixIn, BotHandlerMixIn):
    def __init__(self,
                 messenger=None, storage=None, user_storage=None,
                 middleware=None, tokenizer=None, locale=None):
        self._user_settings = {
            "messenger": messenger or OrderedDict(),
            "storage": storage or OrderedDict(),
            "user_storage": user_storage or OrderedDict(),
            "middleware": middleware or OrderedDict(),
            "tokenizer": tokenizer or OrderedDict(),
            "locale": locale or OrderedDict()
        }
        super().__init__()

    @lazy
    def settings(self):
        _settings = DEFAULT_BOT_SETTINGS.copy()
        for k in _settings.keys():
            if isinstance(_settings[k], (dict, OrderedDict)):
                _settings[k].update(self._user_settings.get(k, {}))
            elif isinstance(_settings[k], list):
                _settings[k] += self._user_settings.get(k, [])
            else:
                _settings[k] = self._user_settings.get(k, None)
        return _settings

    @lazy
    def storage(self) -> StorageAdapter:
        if self.settings["storage"]:
            first_item = next(iter(self.settings["storage"].items()))
            return load_module({"entry": first_item[0], "params": first_item[1]})

    @lazy
    def tokenizer(self) -> BaseTokenizer:
        if self.settings["tokenizer"]:
            first_item = next(iter(self.settings["tokenizer"].items()))
            return load_module({"entry": first_item[0], "params": first_item[1]})

    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unbind()


if __name__ == "__main__":
    a = PythonBot()
    from python_bot.common.messenger.controllers.console import ConsoleMessenger

    r = ConsoleMessenger().get_request(1, "test")
    d = a.on_message(r)
