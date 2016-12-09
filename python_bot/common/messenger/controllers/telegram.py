import json

import requests
from requests.utils import guess_json_utf
from gettext import gettext as _
from python_bot.common.messenger.controllers.base.messenger import WebHookMessenger
from python_bot.common.messenger.elements.base import UserInfo
from python_bot.common.messenger.elements.message import create_message
from python_bot.common.webhook.handlers.base import WebHookRequestHandler
from python_bot.common.webhook.message import BotButtonResponse, BotTextResponse, BotImageResponse, \
    BotTypingResponse, BotPersistentMenuResponse, BotResponse


class TelegramMessenger(WebHookMessenger):
    @property
    def raw_client(self):
        return self._messenger

    def set_web_hook_url(self, web_hook_url):
        self.raw_client.set_webhook(web_hook_url, open(self.default_handler.settings.ssl_cert))

    @property
    def get_handlers(self):
        return [WebHookRequestHandler(self.__process)]

    def __init__(self, access_token=None, api_version=None, on_message_callback=None, bot=None, base_path=None):
        if not access_token:
            raise ValueError(_("You need to specify access_token."))

        super().__init__(access_token, api_version, on_message_callback, bot, base_path)
        import telebot
        self._messenger = telebot.TeleBot(access_token)

    def send_text_message(self, message: BotTextResponse):
        self.raw_client.send_message(message.request_user_id, message.text, **self.__get_extra_kwargs(message))

    def send_button(self, message: BotButtonResponse):
        import telebot
        markup = telebot.types.ReplyKeyboardMarkup()
        for button in message.buttons:
            markup.add(button.title)

        return self.raw_client.send_message(
            message,
            message.text,
            reply_markup=markup,
            **self.__get_extra_kwargs(message)
        )

    def send_image(self, message: BotImageResponse):
        if message.url:
            stream = requests.get(message.url, stream=True).raw
        else:
            stream = open(message.path, "rb")

        try:
            return self.raw_client.send_photo(
                message.request_user_id,
                stream,
                **self.__get_extra_kwargs(message)
            )
        finally:
            stream.close()

    def set_persistent_menu(self, message: BotPersistentMenuResponse):
        raise NotImplemented()

    def send_typing(self, message: BotTypingResponse):
        return self.raw_client.send_chat_action(message.request_user_id, 'typing')

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

    def __get_extra_kwargs(self, message: BotResponse):
        keys = {
            "caption",  # photo message
            "disable_web_page_preview",  # text message
            "reply_to_message_id",
            "parse_mode",
            "disable_notification"
        }
        return {key: message.kwargs[key] for key in message.kwargs if key in keys}

    def __process(self, data=None):
        if not data:
            return

        import telebot
        json_data = json.loads(data.decode(), encoding=guess_json_utf(data))
        update = telebot.types.Update.de_json(json_data)
        telegram_message = update.message

        from python_bot.bot.bot import bot_logger
        bot_logger.debug("Received message: %s" % telegram_message)
        user = telegram_message.from_user

        message = create_message(telegram_message.content_type,
                                 user=UserInfo(user.id, user.first_name, user.last_name, user.username),
                                 date=telegram_message.date,
                                 text=telegram_message.text,
                                 message_id=user.id)

        if not message:
            bot_logger.debug("Failed to initiate message data for content type [%s]" % message.content_Type)
            return

        self.on_message(message, data, extra=telegram_message)
