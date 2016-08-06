import os

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

DEFAULT_BOT_SETTINGS = {
    "messenger": {
        "python_bot.common.messenger.controllers.console.ConsoleMessenger": {}
    }
    ,
    "storage": {
        "python_bot.common.storage.json_database.JsonDatabaseAdapter": {}
    },
    "user_storage": {
        "python_bot.common.storage.json_database.UserJsonDatabaseAdapter": {}
    },
    "middleware": {
        "python_bot.common.middleware.emoji.EmojiMiddleware": {
            "use_aliases": True,
            "message_only": True
        },
    },
    "tokenizer": {
        "python_bot.common.tokenizer.elasticsearch.ElasticSearchTokenizer": {
            "server": "pressandgetdb.westeurope.cloudapp.azure.com",
            "index": "ka4me_actions",
            "field": "name.exact_name",
        }
    }
}

_user_settings = {}
_user_settings_changed = True

_settings = {}


def set_bot_settings(messenger=None, storage=None, user_storage=None, middleware=None, tokenizer=None):
    global _user_settings, _user_settings_changed
    _user_settings.update({
        "messenger": messenger or {},
        "storage": storage or {},
        "user_storage": user_storage or {},
        "middleware": middleware or {},
        "tokenizer": tokenizer or {}
    })
    _user_settings_changed = True


def get_bot_settings():
    global _settings, _user_settings_changed
    if _user_settings_changed:
        _settings = DEFAULT_BOT_SETTINGS.copy()
        for k in _settings.keys():
            _settings[k].update(_user_settings.get(k, {}))
            _user_settings_changed = False
    return _settings
