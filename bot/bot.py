from python_bot.common.localization.handler import LocalizationMixIn
from python_bot.common.middleware.handler import MiddlewareHandlerMixIn
from python_bot.common.storage.base import StorageAdapter
from python_bot.common.tokenizer.base import BaseTokenizer
from python_bot.common.utils.misc import lazy
from python_bot.common.utils.path import load_module
from python_bot.common.webhook.request import BotRequest
from python_bot.settings import BOT_SETTINGS


class BotHandlerMixIn:
    request_class = BotRequest

    @lazy
    def messengers(self):
        result = []
        for messenger in BOT_SETTINGS["messenger"]:
            params = messenger.get("params", {})
            params["on_message_callback"] = self.on_message
            mod = load_module({"entry": messenger["entry"], "params": params})
            result.append(mod)
        return result

    def bind(self):
        for messenger in self.messengers:
            messenger.bind()

    def unbind(self):
        for messenger in self.messengers:
            messenger.unbind()

    def on_message(self, request: BotRequest):
        message = self.get_message(request)
        return request.messenger.handle(message)


class PythonBot(LocalizationMixIn, MiddlewareHandlerMixIn, BotHandlerMixIn):
    @lazy
    def storage(self) -> StorageAdapter:
        if BOT_SETTINGS["storage"]:
            first_item = next(iter(BOT_SETTINGS["storage"].items()))
            return load_module({"entry": first_item[0], "params": first_item[1]})

    @lazy
    def tokenizer(self) -> BaseTokenizer:
        if BOT_SETTINGS["tokenizer"]:
            first_item = next(iter(BOT_SETTINGS["tokenizer"].items()))
            return load_module({"entry": first_item[0], "params": first_item[1]})


if __name__ == "__main__":
    a = PythonBot()
    from python_bot.common.messenger.controllers.console import ConsoleMessenger

    r = ConsoleMessenger().get_request(1, "test")
    d = a.on_message(r)
