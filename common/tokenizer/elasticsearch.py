import urllib.parse

import requests

from python_bot.common.tokenizer.base import BaseTokenizer


class ElasticSearchTokenizer(BaseTokenizer):
    def __init__(self, server: str = None, port: str = "9020", schema: str = "http", index: str = None,
                 field: str = None):
        super().__init__()
        if not server:
            raise ValueError("ElasticSearch server not found")

        if not index:
            raise ValueError("ElasticSearch analyzer index not found")

        if not field:
            raise ValueError("ElasticSearch analyzer field not found")

        self.server = server
        self.port = port
        self.index = index
        self.field = field
        self.base_url = "%s://%s:%s" % (schema, self.server, self.port)
        self.analyzer_url = '%s/%s/_analyze?field=%s&text=' % (self.base_url, self.index, self.field)

    @property
    def name(self):
        return "ElasticSearch Tokenizer"

    def analyze_token(self, text: str):
        message = requests.get(self.analyzer_url + urllib.parse.quote(
            text))
        return [i["token"] for i in message.json()["tokens"]]
