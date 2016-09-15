from python_bot.common.middleware.base import MiddlewareMixin
from python_bot.common.storage.state.base import StateController


class StateMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        self.root = kwargs.pop("root", None)
        super().__init__(*args, **kwargs)

    def __call__(self, request):
        request.state_controller = request.state_controller if request.state_controller else StateController(request)

        state = request.state_controller.get_state()

        if not state:
            if self.root:
                state = request.state_controller.push(self.root)
            else:
                from python_bot.bot import bot_logger
                bot_logger.info("Process_message. No current state found")
                raise ValueError("No current state found")

        state.process_request(request)

        if request.state_controller.changed:
            request.state_controller.trigger_change_events(request, is_will=True)

        message = self.get_message(request)

        if request.state_controller.changed:
            request.state_controller.trigger_change_events(request, messages=message, is_will=False)
            request.state_controller.invalidate_state()

        return state.process_message(request, message)
