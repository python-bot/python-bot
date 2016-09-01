import logging.config
import time
import uuid
from collections import OrderedDict

import sys

import functools

from python_bot.common.localization.handler import LocalizationMixIn
from python_bot.common.messenger.controllers.base.messenger import WebHookMessenger, PollingMessenger
from python_bot.common.middleware.handler import MiddlewareHandlerMixIn
from python_bot.common.storage.base import StorageAdapter
from python_bot.common.tokenizer.base import BaseTokenizer
from python_bot.common.utils.path import load_module
from python_bot.common.utils.polling import start_polling, stop_polling
from python_bot.common.webhook.handlers.base import BaseWebHookHandler
from python_bot.common.webhook.request import BotRequest
from python_bot.settings import DEFAULT_BOT_SETTINGS

__all__ = ["bot_logger", "PythonBot", "BotHandlerMixIn"]

bot_logger = logging.getLogger('PythonBot')
_formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
)

console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(_formatter)
bot_logger.addHandler(console_output_handler)

bot_logger.setLevel(logging.ERROR)


class BotHandlerMixIn:
    request_class = BotRequest

    @property
    @functools.lru_cache()
    def messengers(self) -> list:
        """Lazy Property list of messenger

        Returns:
            List of BaseMessenger objects corresponding to user settings."""
        result = []
        for entry in self.settings["messengers"]:
            params = {"on_message_callback": self.on_message, "bot": self}

            mod = PythonBot.load_module(entry, params)
            if mod:
                result.append(mod)
        return result

    @staticmethod
    def wait():
        """Wait until break event.
        """
        # todo log debug information.
        while True:
            time.sleep(0.3)

    def start(self):
        """Starts webhook server and long polling threads.
        """
        web_hooks = filter(lambda x: isinstance(x, WebHookMessenger), self.messengers)
        for messenger in web_hooks:
            messenger.bind_default_handler()

        polling = filter(lambda x: isinstance(x, PollingMessenger), self.messengers)

        polling_methods = [messenger.receive_updates for messenger in polling]
        if polling_methods:
            start_polling(polling_methods, True, 1)

    def stop(self):
        """Stops webhook server and long polling threads.
        """
        web_hooks = filter(lambda x: isinstance(x, WebHookMessenger), self.messengers)
        for messenger in web_hooks:
            messenger.default_handler.stop()
        stop_polling()

    def converse(self, quit="quit"):
        """Simple console converse method.

        Useful to test your middleware and talk with bot directly from your console.
        Args:
            quit: Name of exit keyword. Bot will proceed user messages until this keyword would be given.

        """
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                from python_bot.common.messenger.controllers.console import ConsoleMessenger
                ConsoleMessenger(on_message_callback=self.on_message, bot=self).on_message(1, user_input)

    def on_message(self, request: BotRequest):
        """Callback method received from messenger.

        Executes all found middleware, then return response back to messenger.
        """
        message = self.get_message(request)
        return request.messenger.handle(message)

    def _validate_messengers(self):
        for messenger in self.messengers:
            pass


class PythonBot(LocalizationMixIn, MiddlewareHandlerMixIn, BotHandlerMixIn):
    def __init__(self,
                 messengers=None, storage=None, user_storage=None,
                 middleware=None, tokenizer=None, locale=None, web_hook=None):
        self._user_settings = {
            "messengers": messengers or (),
            "storage": storage,
            "user_storage": user_storage,
            "middleware": middleware or (),
            "tokenizer": tokenizer or OrderedDict(),
            "locale": locale or OrderedDict(),
            "web_hook": web_hook
        }

        self._validate_messengers()
        super().__init__()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @property
    @functools.lru_cache()
    def settings(self):
        """Lazy property User settings

        Merge user settings with default properties

        Returns:
            Dictionary of user settings."""

        _settings = DEFAULT_BOT_SETTINGS.copy()
        for k in _settings.keys():
            if isinstance(_settings[k], (dict, OrderedDict)):
                _settings[k].update(self._user_settings.get(k, {}))
            elif isinstance(_settings[k], list):
                _settings[k] += self._user_settings.get(k, [])
            else:
                _settings[k] = self._user_settings.get(k, None)
        return _settings

    @property
    @functools.lru_cache()
    def storage(self) -> StorageAdapter:
        """Lazy property for storage adapter

        Load preferred storage adapter from settings

        Returns:
            Instance of StorageAdapter."""
        if self.settings["storage"]:
            first_item = next(iter(self.settings["storage"].items()))
            return load_module({"entry": first_item[0], "params": first_item[1]})

    @property
    @functools.lru_cache()
    def tokenizer(self) -> BaseTokenizer:
        """Lazy property for tokenizer

        Load preferred tokenizer from settings

        Returns:
            Instance of BaseTokenizer."""
        if self.settings["tokenizer"]:
            first_item = next(iter(self.settings["tokenizer"].items()))
            return load_module({"entry": first_item[0], "params": first_item[1]})

    @property
    @functools.lru_cache()
    def web_hook_handler(self) -> BaseWebHookHandler:
        if self.settings["web_hook"]:
            return PythonBot.load_module(self.settings["web_hook"])

    def on_exception(self, exc, request: BotRequest):
        bot_logger.error(exc)

    @staticmethod
    def setup_logging(**kwargs):
        config = DEFAULT_BOT_SETTINGS["logging"]
        config.update(kwargs)
        logging.config.dictConfig(config)

    @staticmethod
    def load_module(entry, extra_params=None):
        if isinstance(entry, (list, tuple)):
            params = entry[1]
            entry = entry[0]
        else:
            params = {}

        if extra_params:
            params.update(extra_params)

        mod = None
        if isinstance(entry, str):
            mod = load_module({"entry": entry, "params": params})
        elif callable(entry):
            mod = entry(**params)

        return mod

    def bind_web_hook_handler(self, handlers, base_path=None) -> BaseWebHookHandler:
        if self.settings["web_hook"]:
            if not base_path:
                base_path = str(uuid.uuid4()).replace("-", "")

            self.web_hook_handler.set_handlers(handlers, base_path)
            return self.web_hook_handler, base_path
