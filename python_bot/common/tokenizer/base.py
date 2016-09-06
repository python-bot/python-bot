import abc

from python_bot.common.models import BaseModule

__all__ = ["BaseTokenizer"]


class BaseTokenizer(BaseModule):
    @abc.abstractmethod
    def analyze_token(self, text: str):
        pass
