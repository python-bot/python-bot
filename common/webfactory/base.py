import abc

from python_bot.common.messenger.controllers.base.messenger import BaseMessenger


class BaseAdapter(metaclass=abc.ABCMeta):
    def __init__(self, messenger: BaseMessenger):
        self.messenger = messenger

    @abc.abstractmethod
    def create_view(self):
        pass

    @abc.abstractmethod
    def bind(self):
        pass

    @abc.abstractmethod
    def unbind(self):
        pass
