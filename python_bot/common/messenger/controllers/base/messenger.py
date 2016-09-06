import abc
import urllib.parse

from python_bot.common.messenger.elements.base import UserInfo
from python_bot.common.messenger.elements.message import BotBaseMessage
from python_bot.common.webhook.handlers.base import BaseWebHookHandler
from python_bot.common.webhook.message import BotButtonResponse, BotTextResponse, BotImageResponse, \
    BotTypingResponse, BotPersistentMenuResponse
from python_bot.common.webhook.request import BotRequest

__all__ = ["BaseMessenger", "PollingMessenger", "WebHookMessenger"]


class BaseMessenger(metaclass=abc.ABCMeta):
    def __init__(self, access_token=None, api_version=None, on_message_callback=None, bot=None):
        self.api_version = api_version
        self.access_token = access_token
        self._on_message_callback = on_message_callback
        self.bot = bot

    @abc.abstractmethod
    def send_text_message(self, message: BotTextResponse):
        pass

    @property
    @abc.abstractmethod
    def raw_client(self):
        pass

    # @abc.abstractmethod
    # def send_generic_message(self, message: BotGenericMessage):
    #     pass

    @abc.abstractmethod
    def send_button(self, message: BotButtonResponse):
        pass

    @abc.abstractmethod
    def send_image(self, message: BotImageResponse):
        pass

    @abc.abstractmethod
    def set_persistent_menu(self, message: BotPersistentMenuResponse):
        pass

    @abc.abstractmethod
    def send_typing(self, message: BotTypingResponse):
        pass

    @abc.abstractmethod
    def get_user_info(self, user_id) -> UserInfo:
        pass

    def on_message(self, message: BotBaseMessage, raw_response=None, extra=None):
        request = self.get_request(message, raw_response, extra)
        if callable(self._on_message_callback):
            return self._on_message_callback(request)

    def get_request(self, message, raw_response=None, extra=None):
        return BotRequest(messenger=self, message=message, raw_response=raw_response, extra=extra)

    def handle(self, messages: list):
        for message in messages:
            if isinstance(message, BotTextResponse):
                self.send_text_message(message)
            elif isinstance(message, BotButtonResponse):
                self.send_button(message)
            elif isinstance(message, BotImageResponse):
                self.send_image(message)
            elif isinstance(message, BotPersistentMenuResponse):
                self.set_persistent_menu(message)
            elif isinstance(message, BotTypingResponse):
                self.send_typing(message)
            else:
                raise ValueError("Message handler not found for message: [%s]" % message)


class PollingMessenger(BaseMessenger, metaclass=abc.ABCMeta):
    @property
    def polling_interval(self):
        """
        :return number: Amount of seconds to wait until next polling. Should be positive float number or zero
        """
        return 1

    @abc.abstractmethod
    def receive_updates(self):
        """
        With method called every polling interval at separate thread. So this should be blocking check
        of new update from socket of something like.
        :return:
        """
        pass


class WebHookMessenger(BaseMessenger, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def get_handlers(self):
        """Get list of all bounded handlers

        Returns:
            List of WebHookRequestHandler"""
        pass

    @abc.abstractmethod
    def set_web_hook_url(self, web_hook_url):
        pass

    def __init__(self, access_token=None, api_version=None, on_message_callback=None, bot=None, base_path=None):
        super().__init__(access_token, api_version, on_message_callback, bot)
        self._default_handler = None
        self.base_path = base_path

    @property
    def base_url(self):
        if not self._default_handler:
            return None

        return urllib.parse.urljoin(self._default_handler.settings.url_base, self.base_path)

    @property
    def default_handler(self) -> BaseWebHookHandler:
        return self._default_handler

    def bind_default_handler(self):
        from python_bot.bot.bot import bot_logger
        self._default_handler, self.base_path = self.bot.bind_web_hook_handler(self.get_handlers, self.base_path)
        bot_logger.debug("Web hook for %s bounded to %s" % (self.__class__.__name__, self.base_url))
        self._default_handler.start()
        self.set_web_hook_url(self.base_url)
