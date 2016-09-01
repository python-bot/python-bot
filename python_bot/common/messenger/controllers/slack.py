import functools

from python_bot.common.messenger.controllers.base.messenger import UserInfo, PollingMessenger
from python_bot.common.webhook.message import BotButtonMessage, BotTextMessage, BotImageMessage, \
    BotPersistentMenuMessage, BotTypingMessage
from python_bot.common.webhook.request import BotRequest


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
        raise NotImplemented()

    def send_text_message(self, message: BotTextMessage):
        raise NotImplemented()

    def send_typing(self, message: BotTypingMessage):
        raise NotImplemented()

    def set_persistent_menu(self, message: BotPersistentMenuMessage):
        raise NotImplemented()

    def get_user_info(self, user_id) -> UserInfo:
        raise NotImplemented()

    def send_image(self, message: BotImageMessage):
        raise NotImplemented()
