import functools

from python_bot.common.messenger.controllers.base.messenger import PollingMessenger
from python_bot.common.messenger.elements.base import UserInfo
from python_bot.common.webhook.message import BotButtonResponse, BotTextResponse, BotImageResponse, \
    BotPersistentMenuResponse, BotTypingResponse


class SlackMessenger(PollingMessenger):
    def receive_updates(self):
        info_from_server = self.raw_client.rtm_read()
        for block in info_from_server:
            if block['type'] == 'message':
                self.on_message(user_id=block['user'],
                                text=block['text'],
                                channel=block['channel'])

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
        raise NotImplemented()

    def send_typing(self, message: BotTypingResponse):
        raise NotImplemented()

    def set_persistent_menu(self, message: BotPersistentMenuResponse):
        raise NotImplemented()

    def get_user_info(self, user_id) -> UserInfo:
        raise NotImplemented()

    def send_image(self, message: BotImageResponse):
        raise NotImplemented()
