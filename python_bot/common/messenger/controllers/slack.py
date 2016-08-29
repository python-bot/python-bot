import getpass
import locale
import os
from time import strftime, gmtime

import functools
from slackclient import SlackClient

from gettext import gettext as _
from python_bot.common.messenger.controllers.base.messenger import UserInfo, PollingMessenger
from python_bot.common.utils.colorize import print_palette, PaletteStyle, centralize
from python_bot.common.webhook.message import BotButtonMessage, BotTextMessage, BotImageMessage, \
    BotPersistentMenuMessage, BotTypingMessage
from python_bot.common.webhook.request import BotRequest


class SlackMessenger(PollingMessenger):

    def receive_updates(self):
        while True:
            info_from_server = self.raw_client.rtm_read()
            for block in info_from_server:
                if block['type'] == 'message':
                    self.on_message(user_id=block['user'],
                                    text=block['text'],
                                    channel=block['channel'])

    @property
    @functools.lru_cache()
    def raw_client(self):
        return SlackClient(token=self.access_token)

    def get_request(self, user_id, text, **kwargs):
        return BotRequest(messenger=self, user_id=user_id, text=text, **kwargs)

    def __init__(self, access_token=None, api_version=None, on_message_callback=None, bot=None):
        super().__init__(access_token, api_version, on_message_callback, bot)
        self.raw_client.rtm_connect()

    def on_message(self, user_id, text, **kwargs):
        request = self.get_request(user_id, text, **kwargs)
        if callable(self._on_message_callback):
            return self._on_message_callback(request)

    def send_button(self, message: BotButtonMessage):
        pass

    def send_text_message(self, message: BotTextMessage):
        pass

    def send_typing(self, message: BotTypingMessage):
        pass

    def set_persistent_menu(self, message: BotPersistentMenuMessage):
        pass

    def get_user_info(self, user_id) -> UserInfo:
        result = UserInfo()
        result.user_id = user_id
        result.first_name = getpass.getuser()
        result.locale = locale.getlocale()[0]
        result.timezone = strftime("%z", gmtime())

        self._print_caption(_("User info:"))
        print_palette(result, PaletteStyle.text)

        return result

    def send_image(self, message: BotImageMessage):
        self._print_caption(_("Send image:"))
        print_palette(_("Recipient: %s, Url: %s, Path: %s") % (message.request.user_id, message.url, message.path),
                      PaletteStyle.text)

    @staticmethod
    def _print_caption(text):
        print_palette(os.linesep + centralize(text) + os.linesep, PaletteStyle.caption)


if __name__ == "__main__":
    channel = "C1YSUDDBQ"
    user_id = "python-bot"
    a = SlackMessenger(access_token="xoxb-66919509936-ks52a9VQDoFp9KzxYZHTIHYQ", api_version=1)
    a.start()
