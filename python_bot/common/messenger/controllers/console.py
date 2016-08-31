import getpass
import locale
import os
from functools import lru_cache
from gettext import gettext as _
from time import strftime, gmtime

from python_bot.common.messenger.controllers.base.messenger import BaseMessenger, UserInfo
from python_bot.common.utils.colorize import PrintHelper
from python_bot.common.webhook.message import BotButtonMessage, BotTextMessage, BotImageMessage, \
    BotPersistentMenuMessage, BotTypingMessage


class ConsoleMessenger(BaseMessenger):
    @property
    @lru_cache()
    def raw_client(self)->PrintHelper:
        return PrintHelper()

    def stop(self):
        pass

    def start(self, **kwargs):
        pass

    def on_message(self, user_id, text):
        
        self.raw_client.header(_("On message"))
        self.raw_client.text(_("Recipient: %s, Text: %s") % (user_id, text))
        return super().on_message(user_id, text)

    def send_button(self, message: BotButtonMessage):
        self.raw_client.header(_("Send button:"))
        self.raw_client.text(_("Recipient: %s, Text: %s \nButtons:") % (message.request.user_id, message.text))
        self.raw_client.button(message.buttons)

    def send_text_message(self, message: BotTextMessage):
        self.raw_client.header(_("Send text message:"))
        self.raw_client.text(_("Recipient: %s, Message: %s") % (message.request.user_id, message.text))
        self.raw_client.quick_reply(_("Quick replies: %s") % message.quick_replies)

    def send_typing(self, message: BotTypingMessage):
        self.raw_client.header(_("Typing:"))
        self.raw_client.typing(_("Typing is set to %s") % (_("on") if message.on else _("off")))

    def set_persistent_menu(self, message: BotPersistentMenuMessage):
        self.raw_client.header(_("Set persistent menu: "))
        self.raw_client.text(message.call_to_actions)

    # def send_generic_message(self, user_id, elements):
    #     self.raw_client.header(_("Send generic message:"))
    #     self.raw_client.text(_("Recipient: %s, Message: %s") % (user_id, elements), PaletteStyle.text)

    def get_user_info(self, user_id) -> UserInfo:
        result = UserInfo()
        result.user_id = user_id
        result.first_name = getpass.getuser()
        result.locale = locale.getlocale()[0]
        result.timezone = int(strftime("%z", gmtime())) / 100

        self.raw_client.header(_("User info:"))
        self.raw_client.text(result)

        return result

    def send_image(self, message: BotImageMessage):
        self.raw_client.header(_("Send image:"))
        self.raw_client.text(_("Recipient: %s, Url: %s, Path: %s") % (message.request.user_id, message.url, message.path))
