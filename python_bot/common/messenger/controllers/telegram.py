import json

import requests
import telebot
from requests.utils import guess_json_utf
from telebot import types
from gettext import gettext as _
from python_bot.common.messenger.controllers.base.messenger import UserInfo, WebHookMessenger
from python_bot.common.webhook.handlers.base import WebHookRequestHandler
from python_bot.common.webhook.message import BotButtonMessage, BotTextMessage, BotImageMessage, \
    BotTypingMessage, BotPersistentMenuMessage


class TelegramMessenger(WebHookMessenger):
    @property
    def raw_client(self):
        return self._messenger

    def set_web_hook_url(self, web_hook_url):
        self.raw_client.set_webhook(web_hook_url, self.default_handler.settings.ssl_cert)

    @property
    def get_handlers(self):
        return [WebHookRequestHandler(self.__process)]

    def __init__(self, access_token=None, api_version=None, on_message_callback=None, bot=None, base_path=None):
        if not access_token:
            raise ValueError(_("You need to specify access_token."))

        super().__init__(access_token, api_version, on_message_callback, bot, base_path)
        self._messenger = telebot.TeleBot(access_token)

    def send_text_message(self, message: BotTextMessage):
        self.raw_client.send_message(message.request.user_id, message.text)

    def send_button(self, message: BotButtonMessage):
        markup = types.ReplyKeyboardMarkup()
        for button in message.buttons:
            markup.add(button.title)

        return self.raw_client.send_message(message, message.text, reply_markup=markup, **message.kwargs)

    def send_image(self, message: BotImageMessage):
        if message.url:
            stream = requests.get(message.url, stream=True).raw
        else:
            stream = open(message.path, "rb")

        try:
            return self.raw_client.send_photo(message.request.user_id, stream, **message.kwargs)
        finally:
            stream.close()

    def set_persistent_menu(self, message: BotPersistentMenuMessage):
        raise NotImplemented()

    def send_typing(self, message: BotTypingMessage):
        return self.raw_client.send_chat_action(message.request.user_id, 'typing')

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
        if not data:
            return

        json_data = json.loads(data.decode(), encoding=guess_json_utf(data))
        update = telebot.types.Update.de_json(json_data)
        message = update.message

        from python_bot.bot.bot import bot_logger
        bot_logger.debug("Received message: %s" % message)
        self.on_message(message.from_user.id, message.text, data, message)
