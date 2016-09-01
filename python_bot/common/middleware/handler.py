import functools

from python_bot.common.utils.path import load_module

__all__ = ["MiddlewareHandlerMixIn"]


class MiddlewareHandlerMixIn(object):
    def __init__(self):
        self._middleware_chain = None
        super().__init__()

    @property
    @functools.lru_cache()
    def middleware(self):
        if self._middleware_chain:
            return self._middleware_chain

        handler = self._get_message
        for middleware in self.settings["middleware"]:
            params = {"get_message": handler}
            if isinstance(middleware, (list, tuple)):
                params.update(middleware[1])
                middleware = middleware[0]

            if callable(middleware):
                # simple middleware case
                handler = middleware(**params)
            elif isinstance(middleware, str):
                handler = load_module({"entry": middleware, "params": params})
            else:
                raise ValueError("Wrong middleware type")

        # We only assign to this when initialization is complete as it is used
        # as a flag for initialization being complete.
        self._middleware_chain = handler
        return self._middleware_chain

    def get_message(self, request):
        message = self.middleware(request)
        return message

    def _get_message(self, request):
        return []
