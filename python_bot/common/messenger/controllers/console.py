import getpass
import locale
import os
from functools import lru_cache
from gettext import gettext as _
from time import strftime, gmtime

from python_bot.common.messenger.controllers.base.messenger import BaseMessenger
from python_bot.common.messenger.elements.base import UserInfo
from python_bot.common.utils.colorize import PrintHelper
from python_bot.common.webhook.message import BotButtonResponse, BotTextResponse, BotImageResponse, \
    BotPersistentMenuResponse, BotTypingResponse


class ConsoleMessenger(BaseMessenger):
    @property
    @lru_cache()
    def raw_client(self)->PrintHelper:
        return PrintHelper()

    def stop(self):
        pass

    def start(self, **kwargs):
        pass

    def on_message(self, message, raw_response=None, extra=None):
        self.raw_client.header(_("On message"))
        self.raw_client.text(_("Recipient: %s, Text: %s") % (message.user.user_id, message.text))
        return super().on_message(message, raw_response=raw_response, extra=extra)

    def send_button(self, message: BotButtonResponse):
        self.raw_client.header(_("Send button:"))
        self.raw_client.text(_("Recipient: %s, Text: %s \nButtons:") % (message.request_user_id, message.text))
        self.raw_client.button(message.buttons)

    def send_text_message(self, message: BotTextResponse):
        self.raw_client.header(_("Send text message:"))
        self.raw_client.text(_("Recipient: %s, Message: %s") % (message.request_user_id, message.text))
        self.raw_client.quick_reply(_("Quick replies: %s") % message.quick_replies)

    def send_typing(self, message: BotTypingResponse):
        self.raw_client.header(_("Typing:"))
        self.raw_client.typing(_("Typing is set to %s") % (_("on") if message.on else _("off")))

    def set_persistent_menu(self, message: BotPersistentMenuResponse):
        self.raw_client.header(_("Set persistent menu: "))
        self.raw_client.text(message.call_to_actions)

    # def send_generic_message(self, user_id, elements):
    #     self.raw_client.header(_("Send generic message:"))
    #     self.raw_client.text(_("Recipient: %s, Message: %s") % (user_id, elements), PaletteStyle.text)

    def get_user_info(self, user_id) -> UserInfo:
        result = UserInfo(user_id)
        result.first_name = getpass.getuser()
        result.locale = locale.getlocale()[0]
        result.timezone = int(strftime("%z", gmtime())) / 100

        self.raw_client.header(_("User info:"))
        self.raw_client.text(result)

        return result

    def send_image(self, message: BotImageResponse):
        self.raw_client.header(_("Send image:"))
        self.raw_client.text(_("Recipient: %s, Url: %s, Path: %s") % (message.request_user_id, message.url, message.path))
