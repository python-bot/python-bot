import os
from collections import OrderedDict

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

DEFAULT_BOT_SETTINGS = {
    "messenger": [],
    "storage": {
        "python_bot.common.storage.json_database.JsonDatabaseAdapter": {}
    },
    "user_storage": {
        "python_bot.common.storage.json_database.UserJsonDatabaseAdapter": {}
    },
    "middleware": [
        ("python_bot.common.middleware.emoji.EmojiMiddleware", {
            "use_aliases": True,
            "message_only": True
        }),
    ],
    "tokenizer": OrderedDict(),
    "locale": {
        "lang": "en",
        "path": LOCALE_DIR
    },
    "logging": {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(name)s %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            }
        },

        "loggers": {
            # "telegram": {
            #     "level": "INFO",
            #     "handlers": [],
            #     "propagate": "no"
            # },
        },

        "root": {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    }
}
