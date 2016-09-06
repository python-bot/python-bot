import abc


class BaseModule(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def name(self):
        pass
