import functools
import re
from gettext import gettext as _

import dateutil.parser

from python_bot.common.storage.base import UserStorageAdapter


class BotRequest:
    def __init__(self, messenger, user_id, text: str, raw_response: str, extra):
        self.text = str(text)
        if isinstance(raw_response, bytes):
            raw_response = raw_response.decode()

        self.raw_response = raw_response
        self.extra = extra
        self.user_id = user_id
        self.messenger = messenger

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4)

    @property
    @functools.lru_cache()
    def user_storage(self) -> UserStorageAdapter:
        """Cached Property for persistence storage
        Returns:
            UserStorageAdapter can be any kind of storage."""
        if self.messenger.bot.settings["user_storage"]:
            params = {"user_id": self.user_id, "database_name": self.messenger.__class__.__name__}
            from python_bot.bot import PythonBot
            return PythonBot.load_module(self.messenger.bot.settings["user_storage"], params)

    def is_positive(self):
        return any(filter(lambda x: x in self.text.lower().split(),
                          [_("yes"), _("sure"), _("true"), _("of course"), _("certainly"), _("clearly")]))

    def is_negative(self):
        return not self.is_positive()

    def get_number(self):
        m = re.search("[-+]?\d+[.,]?\d*", self.text)
        if not m:
            return
        string_value = m.group(0).replace(",", ".")
        try:
            return int(string_value)
        except ValueError:
            return float(string_value)

    def get_date(self):
        found = re.findall(r"\b([0-9]{1,2})[-/:]([0-9]{1,2})[-/:]([0-9]{4})\b", self.text)
        if not found:
            return

        return dateutil.parser.parse("/".join(found[0]))
