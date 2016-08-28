import os
from collections import OrderedDict

from python_bot.common.utils.misc import lazy

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")


class WebHookSettings:
    host = '<ip/host where the bot is running>'
    port = 8000  # 443, 80, 88 or 8000 (port need to be 'open')
    listen = '0.0.0.0'  # In some VPS you may need to put here the IP addr
    # Quick'n'dirty SSL certificate generation:
    #
    # openssl genrsa -out webhook_pkey.pem 2048
    # openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
    #
    # When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
    # with the same value in you put in WEBHOOK_HOST
    ssl_cert = ''  # './webhook_cert.pem'  # Path to the ssl certificate
    ssl_private = ''  # './webhook_pkey.pem'  # Path to the ssl private key

    @lazy
    def url_base(self):
        schema = "http"
        if self.ssl_cert:
            schema += "s"
        return "%s://%s:%s" % (schema, self.host, self.port)

    def __init__(self, host, port=8000, listen='0.0.0.0', ssl_cert='', ssl_private=''):
        self.host = host
        self.port = port
        self.listen = listen
        self.ssl_cert = ssl_cert
        self.ssl_private = ssl_private


DEFAULT_BOT_SETTINGS = {
    "messengers": [],
    "storage": None,
    "user_storage": None,
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
    "web_hook": None,
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
