from python_bot.bot import PythonBot
from python_bot.common import JsonDatabaseAdapter
from python_bot.common import MiddlewareMixin, BotRequest, BotTextResponse
from python_bot.common import PrintHelper
from python_bot.common.messenger.controllers.console import ConsoleMessenger
from python_bot.common.middleware.state import StateMiddleware

# Adding echo middleware which send message to bot the same as request
from python_bot.common.storage.state.base import StateView

helper = PrintHelper()

INDEX_KEY = "index"


class RootStateView(StateView):
    def did_hide(self, request: BotRequest, messages: list, removed=True):
        helper.header("RootStateView did_hide removed %s" % removed)

    def did_show(self, request: BotRequest, messages: list, added=True):
        helper.header("RootStateView did_show added %s" % added)

    def will_hide(self, request: BotRequest, removed=True):
        helper.header("RootStateView will_hide removed %s" % removed)

    def will_show(self, request: BotRequest, added=True):
        helper.header("RootStateView will_show added %s" % added)

    def process_message(self, request: BotRequest, messages):
        messages.append(BotTextResponse(request, "Hello!"))
        helper.header("Root view controller end")
        return messages

    def process_request(self, request: BotRequest):
        if request.text.lower() == "next":
            request.state_controller.push(PageStateView)
            request.user_storage.update(INDEX_KEY, 1)
        else:
            request.user_storage.update(INDEX_KEY, 0)

        helper.header("Root view controller")
        print(request)


class PageStateView(StateView):
    def will_show(self, request: BotRequest, added=True):
        helper.header("PageStateView will_show added %s" % added)

    def will_hide(self, request: BotRequest, removed=True):
        helper.header("PageStateView will_hide removed %s" % removed)

    def did_show(self, request, messages, added=True):
        helper.header("PageStateView did_show added %s" % added)

    def did_hide(self, request, messages, removed=True):
        helper.header("PageStateView did_hide removed %s" % removed)

    def process_message(self, request: BotRequest, messages):
        messages.append(BotTextResponse(request, "PageView Controller %s!" % request.user_storage.get(INDEX_KEY)))
        helper.header("Page view controller end")
        return messages

    def process_request(self, request: BotRequest):
        if request.text.lower() == "prev":
            request.state_controller.pop()
            request.user_storage.update(INDEX_KEY, request.user_storage.get(INDEX_KEY) - 1)

        if request.text.lower() == "next":
            request.state_controller.push(PageStateView)
            request.user_storage.update(INDEX_KEY, request.user_storage.get(INDEX_KEY) + 1)

        helper.header("Page view controller %s" % request.user_storage.get(INDEX_KEY))
        print(request)


with PythonBot(middleware=[(StateMiddleware, {"root": RootStateView})],
               storage=[JsonDatabaseAdapter, {"database_path": "./user.db"}]) as bot:
    bot.add_messenger(ConsoleMessenger)
    # Simulate on message event
    bot.converse(quit="quit")
