import abc
import json
import os

from python_bot.common.localization.base import t
from python_bot.common.webhook.request import BotRequest
from python_bot.common.webhook.message import BotButtonMessage, BotTextMessage, BotImageMessage, \
    BotTypingMessage, BotPersistentMenuMessage, BotMessage


class UserInfo:
    user_id = 0
    first_name = ""
    last_name = ""
    profile_pic = ""
    locale = None
    timezone = None  # float (min: -24) (max: 24)
    is_male = True

    def __str__(self):
        out = "%s: %s %s " % (self.user_id, self.first_name, self.last_name)
        if self.locale:
            out += os.linesep + t("Locale: ") + self.locale
        if self.timezone:
            out += os.linesep + t("Timezone: ") + str(self.timezone)
        return out


class BaseMessenger(metaclass=abc.ABCMeta):
    def __init__(self, access_token=None, api_version=None, on_message_callback=None, bot=None):
        self.api_version = api_version
        self.access_token = access_token
        self._on_message_callback = on_message_callback
        self.bot = bot

    @abc.abstractmethod
    def send_text_message(self, message: BotTextMessage):
        pass

    # @abc.abstractmethod
    # def send_generic_message(self, message: BotGenericMessage):
    #     pass

    @abc.abstractmethod
    def bind(self, **kwargs):
        pass

    @abc.abstractmethod
    def unbind(self):
        pass

    @abc.abstractmethod
    def send_button(self, message: BotButtonMessage):
        pass

    @abc.abstractmethod
    def send_image(self, message: BotImageMessage):
        pass

    @abc.abstractmethod
    def set_persistent_menu(self, message: BotPersistentMenuMessage):
        pass

    @abc.abstractmethod
    def send_typing(self, message: BotTypingMessage):
        pass

    @abc.abstractmethod
    def get_user_info(self, user_id) -> UserInfo:
        pass

    def on_message(self, user_id, text):
        request = self.get_request(user_id, text)
        if callable(self._on_message_callback):
            return self._on_message_callback(request)

    def get_request(self, user_id, text):
        return BotRequest(messenger=self, user_id=user_id, text=text)

    def handle(self, messages: list):
        for message in messages:
            if isinstance(message, BotTextMessage):
                self.send_text_message(message)
            elif isinstance(message, BotButtonMessage):
                self.send_button(message)
            elif isinstance(message, BotImageMessage):
                self.send_image(message)
            elif isinstance(message, BotPersistentMenuMessage):
                self.set_persistent_menu(message)
            elif isinstance(message, BotTypingMessage):
                self.send_typing(message)
            else:
                raise ValueError("Message handler not found for message: [%s]" % message)
