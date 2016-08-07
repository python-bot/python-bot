import getpass
import locale
import os
from time import strftime, gmtime

from python_bot.common.localization.base import t
from python_bot.common.messenger.controllers.base.messenger import BaseMessenger, UserInfo
from python_bot.common.messenger.elements.buttons import PostbackButton
from python_bot.common.utils.colorize import print_palette, PaletteStyle, centralize
from python_bot.common.webhook.message import BotButtonMessage, BotTextMessage, BotImageMessage, \
    BotPersistentMenuMessage, BotTypingMessage


class ConsoleMessenger(BaseMessenger):
    def unbind(self):
        pass

    def bind(self, **kwargs):
        pass

    def on_message(self, user_id, text):
        self._print_caption(t("On message"))
        print_palette(t("Recipient: %s, Text: %s") % (user_id, text), PaletteStyle.text)
        return super().on_message(user_id, text)

    def send_button(self, message: BotButtonMessage):
        self._print_caption(t("Send button:"))
        print_palette(t("Recipient: %s, Text: %s \nButtons:") % (message.request.user_id, message.text),
                      PaletteStyle.text)
        print_palette(message.buttons, PaletteStyle.button)

    def send_text_message(self, message: BotTextMessage):
        self._print_caption(t("Send text message:"))
        print_palette(t("Recipient: %s, Message: %s") % (message.request.user_id, message.text), PaletteStyle.text)
        print_palette(t("Quick replies: %s") % message.quick_replies, PaletteStyle.quick_reply)

    def send_typing(self, message: BotTypingMessage):
        self._print_caption(t("Typing:"))
        print_palette(t("Typing is set to %s") % (t("on") if message.on else t("off")), PaletteStyle.typing)

    def set_persistent_menu(self, message: BotPersistentMenuMessage):
        self._print_caption(t("Set persistent menu: "))
        print_palette(message.call_to_actions, PaletteStyle.text)

    # def send_generic_message(self, user_id, elements):
    #     self._print_caption(t("Send generic message:"))
    #     print_palette(t("Recipient: %s, Message: %s") % (user_id, elements), PaletteStyle.text)

    def get_user_info(self, user_id) -> UserInfo:
        result = UserInfo()
        result.user_id = user_id
        result.first_name = getpass.getuser()
        result.locale = locale.getlocale()[0]
        result.timezone = strftime("%z", gmtime())

        self._print_caption(t("User info:"))
        print_palette(result, PaletteStyle.text)

        return result

    def send_image(self, message: BotImageMessage):
        self._print_caption(t("Send image:"))
        print_palette(t("Recipient: %s, Url: %s, Path: %s") % (message.request.user_id, message.url, message.path),
                      PaletteStyle.text)

    @staticmethod
    def _print_caption(text):
        print_palette(os.linesep + centralize(text) + os.linesep, PaletteStyle.caption)


if __name__ == "__main__":
    a = ConsoleMessenger(access_token="1", api_version=1)
    a.send_text_message(1, "Test Message", ["132", "123"])
    a.get_user_info(1)
    a.send_typing(1, False)
    a.send_button(1, "Test", [PostbackButton("Test button", "1")])
