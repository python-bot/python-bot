__all__ = ["MiddlewareMixin"]


class MiddlewareMixin(object):
    def __init__(self, get_message=None, request_only=False, message_only=False):
        self.get_message = get_message
        self.request_only = request_only
        self.message_only = message_only
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        message = None
        if hasattr(self, 'process_request') and not self.message_only:
            message = self.process_request(request)

        if not message:
            message = self.get_message(request)

        if hasattr(self, 'process_message') and not self.request_only:
            message = self.process_message(request, message)

        return message
