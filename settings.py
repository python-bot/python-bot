import os

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

BOT_SETTINGS = {
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
        "python_bot.tests.common.middleware.EchoMiddleware": {}
    },
    "tokenizer": {
        "python_bot.common.tokenizer.elasticsearch.ElasticSearchTokenizer": {
            "server": "pressandgetdb.westeurope.cloudapp.azure.com",
            "index": "ka4me_actions",
            "field": "name.exact_name",
        }
    }
}


def main():
    pass
    # t = load_module(**BOT_SETTINGS["tokenizer"])


    # print(t.analyze_token("собака бывает кусачей"))
    # emoji_postprocessor()
    # LocaleMessages().make_messages()
    # LocaleMessages().compile_messages()


if __name__ == '__main__':
    main()
