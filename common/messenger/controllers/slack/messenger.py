import getpass
import locale
import os
import pprint
import time
from time import strftime, gmtime
from slackclient import SlackClient
from python_bot.common.webhook.request import BotRequest
from python_bot.common.localization.base import t
from python_bot.common.messenger.controllers.base.messenger import BaseMessenger, UserInfo
from python_bot.common.messenger.elements.buttons import PostbackButton
from python_bot.common.utils.colorize import print_palette, PaletteStyle, centralize
from python_bot.common.utils.misc import lazy
from python_bot.common.webhook.message import BotButtonMessage, BotTextMessage, BotImageMessage, \
    BotPersistentMenuMessage, BotTypingMessage


class SlackMessenger(BaseMessenger):

    @lazy
    def raw_client(self):
        return SlackClient(token=self.access_token)

    def get_request(self, user_id, text, **kwargs):
        return BotRequest(messenger=self, user_id=user_id, text=text, **kwargs)

    def bind(self, **kwargs):
        if self.raw_client.rtm_connect():
            while True:
                info_from_server = self.raw_client.rtm_read()
                for block in info_from_server:
                    if block['type'] == 'message':
                        self.on_message(user_id=block['user'],
                                        text=block['text'],
                                        channel=block['channel'])
                time.sleep(1)

    def unbind(self):
        pass

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
    channel = "C1YSUDDBQ"
    user_id = "python-bot"
    a = SlackMessenger(access_token="xoxb-66919509936-ks52a9VQDoFp9KzxYZHTIHYQ", api_version=1)
    a.bind()

# ++++++++++++++++for the futer +++++++++++++++++++++++
#print(self.raw_client.api_call("api.test"))
#list_users = self.raw_client.api_call("users.list")['members']
#user_number = ""
#user_channel = ""
#for dict_user in list_users:
#    for key, value in dict_user.items():
#        if dict_user[key] == user_id:
#            user_number = dict_user['id']
#
#xxx = self.raw_client.api_call("im.open", user=user_number)
#
#pprint.pprint(xxx)
#user_channel = xxx['channel']
#user_channel_id = user_channel['id']
#print(self.raw_client.api_call("chat.postMessage",
#                               channel=user_channel_id,
#                               text="Privet Sergey",
#                               username='smert',
#                               icon_emoji=':robot_face:'))
#pprint.pprint(xxx)
#return xxx