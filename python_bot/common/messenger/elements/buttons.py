import abc
import json

from gettext import gettext as _

__all__ = ["Button", "PhoneNumberButton", "QuickReply"]


class Button(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def button_type(self):
        pass

    def __init__(self, title):
        if len(title) > 20:
            raise ValueError(_('Button title limit is 20 characters'))
        self.title = title

    def to_dict(self):
        serialised = {
            'type': self.button_type,
            'title': self.title
        }
        if self.button_type == 'web_url':
            serialised['url'] = self.url
        elif self.button_type == 'postback':
            serialised['payload'] = self.payload
        return serialised

    def to_json(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return self.to_json()


class PhoneNumberButton(Button):
    button_type = 'postback'

    def __init__(self, title, phone_number):
        if not phone_number or phone_number[0] != "+":
            raise ValueError(_('Phone_number payload format mush be ‘+’ prefix followed by the country code, '
                               'area code and local number'))
        super().__init__(title=title)


class WebUrlButton(Button):
    button_type = 'web_url'

    def __init__(self, title, url):
        self.url = url
        super().__init__(title=title)


class PostbackButton(Button):
    button_type = 'postback'

    def __init__(self, title, payload):
        self.payload = payload
        super().__init__(title=title)


class QuickReply(object):
    def __init__(self, title, payload):
        if len(title) > 20:
            raise ValueError('Button title limit is 20 characters')
        self.title = title
        self.payload = payload

    def to_dict(self):
        serialised = {
            'content_type': "text",
            'title': self.title,
            'payload': self.payload
        }

        return serialised

    def to_json(self):
        return json.dumps(self.to_dict())


YES_BUTTON = QuickReply(_("Yes"), "yes")
NO_BUTTON = QuickReply(_("No"), "no")

MALE_BUTTON = QuickReply(_("Male"), "male")
FEMALE_BUTTON = QuickReply(_("Female"), "female")

YES_NO_BUTTONS = [YES_BUTTON, NO_BUTTON]

GENDER_BUTTONS = [MALE_BUTTON, FEMALE_BUTTON]
