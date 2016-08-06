import abc

from python_bot.common.models import BaseModule


class BaseTokenizer(BaseModule):
    @abc.abstractmethod
    def analyze_token(self, text: str):
        pass