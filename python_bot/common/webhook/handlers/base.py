import abc

from python_bot.settings import WebHookSettings


class WebHookRequestHandler:
    def __init__(self, process=None, can_process=None, request_type="POST"):
        self._process = process
        self._can_process = can_process
        self._request_type = request_type

    def can_process(self, request_type, path, headers):
        if self._request_type == request_type:
            if callable(self._can_process):
                return bool(self._can_process(request_type=request_type, path=path, headers=headers))
        return False

    def process(self, data):
        if callable(self._process):
            self._process(data=data)


class BaseWebHookHandler(metaclass=abc.ABCMeta):
    """
    :param handlers: List of WebHookRequestHandler
    """

    def __init__(self, settings: WebHookSettings):
        self.settings = settings
        self.handlers = {}

    def set_handlers(self, handlers: list, base_path: str):
        self.handlers[base_path] = handlers

    def get_request_handler(self, request_type, path, headers) -> WebHookRequestHandler:
        base_path = path.split("/")[0]
        handlers = self.handlers.get(base_path)

        if not handlers:
            raise ValueError("Handlers can not be empty")

        for handler in handlers:
            if handler.can_process(request_type, path, headers):
                return handler

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass
