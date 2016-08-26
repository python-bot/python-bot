import requests
import telebot
from telebot import types

from python_bot.common.messenger.controllers.base.messenger import UserInfo, WebHookMessenger
from python_bot.common.webhook.handlers.base import WebHookRequestHandler
from python_bot.common.webhook.message import BotButtonMessage, BotTextMessage, BotImageMessage, \
    BotTypingMessage, BotPersistentMenuMessage


class TelegramMessenger(WebHookMessenger):
    def set_web_hook_url(self, web_hook_url):
        self.messenger.set_webhook(web_hook_url, self.default_handler.settings.ssl_cert)

    @property
    def get_handlers(self):
        return [WebHookRequestHandler(self.__process)]

    def __init__(self, access_token=None, api_version=None, on_message_callback=None, bot=None):
        super().__init__(access_token, api_version, on_message_callback, bot)
        self.messenger = telebot.TeleBot(access_token)

    def send_text_message(self, message: BotTextMessage):
        self.messenger.send_message(message.request.user_id, message.text)

    def send_button(self, message: BotButtonMessage):
        markup = types.ReplyKeyboardMarkup()
        for button in message.buttons:
            markup.add(button.title)

        return self.messenger.send_message(message, message.text, reply_markup=markup, **message.kwargs)

    def send_image(self, message: BotImageMessage):
        if message.url:
            stream = requests.get(message.url, stream=True).raw
        else:
            stream = open(message.path, "rb")

        try:
            return self.messenger.send_photo(message.request.user_id, stream, **message.kwargs)
        finally:
            stream.close()

    def set_persistent_menu(self, message: BotPersistentMenuMessage):
        raise NotImplemented()

    def send_typing(self, message: BotTypingMessage):
        return self.messenger.send_chat_action(message.request.user_id, 'typing')

    def get_user_info(self, user_id) -> UserInfo:
        raise NotImplemented()
        # self.messenger.get_user_profile_photos()
        # user = UserInfo()
        # user.is_male = user_details.get("gender") == "male"
        # user.first_name = user_details.get("first_name")
        # user.last_name = user_details.get("last_name")
        # user.locale = user_details.get("locale")
        # user.timezone = user_details.get("timezone")
        # user.profile_pic = "https://graph.facebook.com/%s/picture" % user_id
        # return user

    def __process(self, data=None):
        self.on_message(data["user_id"], data["text"])
