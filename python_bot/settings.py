import os
from collections import OrderedDict

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

DEFAULT_BOT_SETTINGS = {
    "messenger": OrderedDict(),
    "storage": OrderedDict({
        "python_bot.common.storage.json_database.JsonDatabaseAdapter": {}
    }),
    "user_storage": OrderedDict({
        "python_bot.common.storage.json_database.UserJsonDatabaseAdapter": {}
    }),
    "middleware": OrderedDict({
        "python_bot.common.middleware.emoji.EmojiMiddleware": {
            "use_aliases": True,
            "message_only": True
        },
    }),
    "tokenizer": OrderedDict(),
    "locale": {
        "lang": "en",
        "path": LOCALE_DIR
    }
}
