import datetime
import functools

from python_bot.common import create_message
from python_bot.common.messenger.controllers.base.messenger import PollingMessenger
from python_bot.common.messenger.elements.base import UserInfo
from python_bot.common.webhook.message import BotButtonResponse, BotTextResponse, BotImageResponse, \
    BotPersistentMenuResponse, BotTypingResponse


class SlackMessenger(PollingMessenger):
    def receive_updates(self):
        info_from_server = self.raw_client.rtm_read()
        for block in info_from_server:
            if block['type'] == 'message':
                bot_message = create_message(
                    "text",
                    user=UserInfo(block["user"]),
                    date=datetime.datetime.fromtimestamp(float(block['ts'])),
                    text=block['text'],
                    message_id=block['channel']
                )
                self.on_message(bot_message, extra=block)

    @property
    @functools.lru_cache()
    def raw_client(self):
        from slackclient import SlackClient
        return SlackClient(token=self.access_token)

    def __init__(self, access_token=None, api_version=None, on_message_callback=None, bot=None):
        super().__init__(access_token, api_version, on_message_callback, bot)
        self.raw_client.rtm_connect()

    def send_button(self, message: BotButtonResponse):
        raise NotImplemented()

    def send_text_message(self, message: BotTextResponse):
        self.raw_client.api_call("chat.postMessage", channel=message.request_message_id,
                                 text=message.text, as_user=False)

    def send_typing(self, message: BotTypingResponse):
        raise NotImplemented()

    def set_persistent_menu(self, message: BotPersistentMenuResponse):
        raise NotImplemented()

    def get_user_info(self, user_id) -> UserInfo:
        raise NotImplemented()

    def send_image(self, message: BotImageResponse):
        raise NotImplemented()
