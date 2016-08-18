import json
import os

import requests
from requests_toolbelt import MultipartEncoder
from gettext import gettext as _

from python_bot.common.messenger.controllers.base.messenger import UserInfo, BaseMessenger
from python_bot.common.webhook.message import BotButtonMessage, BotTextMessage, BotImageMessage, \
    BotTypingMessage, BotPersistentMenuMessage


class FacebookMessenger(BaseMessenger):
    def unbind(self):
        pass

    def bind(self, **kwargs):
        pass

    def __init__(self, access_token=None, api_version=None, on_message_callback=None):

        super().__init__(access_token, api_version, on_message_callback)
        self.base_url = (
            "https://graph.facebook.com"
            "/v{0}/me/messages?access_token={1}"
        ).format(self.api_version, access_token)

        self.thread_settings_url = (
            "https://graph.facebook.com/v{0}/me/thread_settings?access_token={1}"
        ).format(self.api_version, access_token)

    def send_text_message(self, message: BotTextMessage):
        payload = {
            'recipient': {
                'id': message.request.user_id
            },
            'message': {
                'text': message,
            }
        }

        if message.quick_replies:
            payload["message"]["quick_replies"] = list(map(lambda r: r.to_json(), message.quick_replies))

    # @abc.abstractmethod
    # def send_generic_message(self, message: BotGenericMessage):
    #     pass

    def send_button(self, message: BotButtonMessage):
        payload = {
            'recipient': {
                'id': message.request.user_id
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": message.text,
                        "buttons": list(map(lambda b: b.to_json(), message.buttons))
                    }
                }
            }
        }
        return self._send_payload(payload)

    def send_image(self, message: BotImageMessage):
        """
          This sends an image to the specified recipient.
          Image must be PNG or JPEG or GIF.
        """
        if message.path:
            if not os.path.exists(message.path):
                raise ValueError(_("Image on path [%s] does not exists") % message.path)

            payload = {
                'recipient': json.dumps(
                    {
                        'id': message.request.user_id
                    }
                ),
                'message': json.dumps(
                    {
                        'attachment': {
                            'type': 'image',
                            'payload': {}
                        }
                    }
                ),
                'filedata': (message.path, open(message.path, 'rb'))
            }
            multipart_data = MultipartEncoder(payload)
            multipart_header = {
                'Content-Type': multipart_data.content_type
            }
            return requests.post(self.base_url, data=multipart_data, headers=multipart_header).json()
        elif message.url:
            payload = {
                "recipient": {
                    "id": message.request.user_id
                },
                "message": {
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": message.url
                        }
                    }
                }
            }

            self._send_payload(payload)
        else:
            ValueError(_("Image url either image path should be set"))

    def set_persistent_menu(self, message: BotPersistentMenuMessage):
        data = {
            "setting_type": "call_to_actions",
            "thread_state": "existing_thread",
            "call_to_actions": list(map(lambda b: b.to_json(), message.call_to_actions))
        }
        return self._send_thread_settings(data)

    def send_typing(self, message: BotTypingMessage):
        payload = {
            'recipient': json.dumps(
                {
                    'id': message.request.user_id
                }
            ),
            'sender_action': 'typing_' + ("on" if message.on else "off")

        }
        return self._send_payload(payload)

    def get_user_info(self, user_id) -> UserInfo:
        user_details_url = "https://graph.facebook.com/v2.7/%s" % user_id
        user_details_params = {'fields': 'first_name,last_name,gender,locale,timezone',
                               'access_token': self.access_token}
        user_details = requests.get(user_details_url, user_details_params).json()
        user = UserInfo()
        user.is_male = user_details.get("gender") == "male"
        user.first_name = user_details.get("first_name")
        user.last_name = user_details.get("last_name")
        user.locale = user_details.get("locale")
        user.timezone = user_details.get("timezone")
        user.profile_pic = "https://graph.facebook.com/%s/picture" % user_id
        return user

    def _send_generic_message(self, user_id, elements):
        payload = {
            'recipient': {
                'id': user_id
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": list(map(lambda el: el.to_json(), elements))
                    }
                }
            }
        }
        return self._send_payload(payload)

    def _send_thread_settings(self, payload):
        result = requests.post(self.thread_settings_url, json=payload).json()
        return result

    def _send_payload(self, payload):
        result = requests.post(self.base_url, json=payload).json()
        return result
