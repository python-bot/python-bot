import abc
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


class PrintEventStateView(StateView, metaclass=abc.ABCMeta):
    def will_show(self, request: BotRequest, added=True):
        helper.header("%s will_show added %s" % (self._get_title(request), added))

    def will_hide(self, request: BotRequest, removed=True):
        helper.header("%s will_hide removed %s" % (self._get_title(request), removed))

    def did_show(self, request, messages, added=True):
        helper.header("%s did_show added %s" % (self._get_title(request), added))

    def did_hide(self, request, messages, removed=True):
        helper.header("%s did_hide removed %s" % (self._get_title(request), removed))

    @abc.abstractmethod
    def _get_title(self, request):
        pass


class RootStateView(PrintEventStateView):
    def _get_title(self, request):
        return "RootStateView"

    def process_message(self, request: BotRequest, messages):
        messages.append(BotTextResponse(request, "Hello! Use 'next' or 'prev' to navigate between pages."))
        helper.header("Root view controller end")
        return messages

    def process_request(self, request: BotRequest):
        if request.text.lower() == "next":
            request.state_controller.push(PageStateView(index=1))

        helper.header("Root view controller")
        print(request)


class PageStateView(PrintEventStateView):
    def __init__(self, index=0):
        self.index = index

    def process_message(self, request: BotRequest, messages):
        messages.append(BotTextResponse(request, self._get_title(request)))
        helper.header("Page view controller end")
        return messages

    def process_request(self, request: BotRequest):
        if request.text.lower() == "prev":
            request.state_controller.pop()

        if request.text.lower() == "next":
            request.state_controller.push(PageStateView(index=self.index + 1))

        helper.header("Page view controller %s" % self.index)
        print(request)

    def _get_title(self, request):
        return "PageView Controller %s!" % self.index


with PythonBot(middleware=[(StateMiddleware, {"root": RootStateView()})],
               storage=[JsonDatabaseAdapter, {"database_path": "./user.db"}]) as bot:
    bot.add_messenger(ConsoleMessenger)
    # Simulate on message event
    bot.converse(quit="quit")
