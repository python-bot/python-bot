import functools
import re
from gettext import gettext as _

import dateutil.parser

from python_bot.common.messenger.elements.message import BotBaseMessage
from python_bot.common.storage import UserStorageAdapter

__all__ = ["BotRequest"]


class BotRequest:
    def __init__(self, messenger, message: BotBaseMessage, raw_response: str, extra):
        self.message = message
        if isinstance(raw_response, bytes):
            raw_response = raw_response.decode()

        self.raw_response = raw_response
        self.extra = extra
        self.messenger = messenger
        self.text = message.text if hasattr(message, "text") else None

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4)

    @property
    @functools.lru_cache()
    def user_storage(self) -> UserStorageAdapter:
        """Cached Property for persistence storage
        Returns:
            UserStorageAdapter can be any kind of storage."""
        if self.messenger.bot.storage:
            params = {"user_id": self.message.user.user_id, "database_name": self.messenger.__class__.__name__}
            return self.messenger.bot.storage.create_user_storage(**params)

    def is_positive(self):
        if not self.text:
            return False
        return any(filter(lambda x: x in self.text.lower().split(),
                          [_("yes"), _("sure"), _("true"), _("of course"), _("certainly"), _("clearly")]))

    def is_negative(self):
        return not self.is_positive()

    def get_number(self):
        if not self.text:
            return

        m = re.search("[-+]?\d+[.,]?\d*", self.text)
        if not m:
            return
        string_value = m.group(0).replace(",", ".")
        try:
            return int(string_value)
        except ValueError:
            return float(string_value)

    def get_date(self):
        if not self.text:
            return

        found = re.findall(r"\b([0-9]{1,2})[-/:]([0-9]{1,2})[-/:]([0-9]{4})\b", self.text)
        if not found:
            return

        return dateutil.parser.parse("/".join(found[0]))
