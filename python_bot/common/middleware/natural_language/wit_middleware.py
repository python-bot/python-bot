from wit import Wit

from python_bot.common.middleware.base import MiddlewareMixin
from python_bot.common.webhook.request import BotRequest


class WitMiddleware(MiddlewareMixin):
    WIT_DATA_KEY = "_wit"
    WIT_CONTEXT_KEY = "_context"

    def __init__(self, *args, **kwargs):
        self.access_token = kwargs.pop("access_token", None)
        self.actions = kwargs.pop("actions", {})
        self.client = Wit(access_token=self.access_token, actions=self.actions)
        super().__init__(*args, **kwargs)

    def process_request(self, request: BotRequest):
        if request.text:
            user_data = request.user_storage().get(request.user_id)
            wit_data = user_data.get(self.WIT_DATA_KEY, {})
            context = wit_data.get(self.WIT_CONTEXT_KEY, {})

            result_context = self.client.run_actions(str(request.user_id), request.text, context)
            wit_data[self.WIT_CONTEXT_KEY] = result_context
