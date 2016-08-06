import re

import dateutil.parser

from python_bot.common.localization.base import t
from python_bot.common.storage.base import UserStorageAdapter
from python_bot.common.utils.path import load_module
from python_bot.settings import BOT_SETTINGS


class BotRequest:
    def __init__(self, messenger, user_id, text: str, analyzed_text: str = None):
        self.text = str(text)
        self.analyze_text = analyzed_text
        self.user_id = user_id
        self.messenger = messenger

    def user_storage(self) -> UserStorageAdapter:
        params = BOT_SETTINGS["user_storage"].get("params", {})
        params["user_id"] = self.user_id
        if BOT_SETTINGS["user_storage"]:
            first_item = next(iter(BOT_SETTINGS["user_storage"].items()))
            return load_module({"entry": first_item[0], "params": first_item[1]})

    def is_positive(self):
        return any(filter(lambda x: x in self.text.lower().split(),
                          [t("yes"), t("sure"), t("true"), t("of course"), t("certainly"), t("clearly")]))

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
