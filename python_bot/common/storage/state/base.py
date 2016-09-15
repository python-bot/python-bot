import abc

import jsonpickle

from python_bot.common import BotRequest


class StateView(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def will_show(self, request: BotRequest, added=True):
        pass

    @abc.abstractmethod
    def will_hide(self, request: BotRequest, removed=True):
        pass

    @abc.abstractmethod
    def did_show(self, request: BotRequest, messages: list, added=True):
        pass

    @abc.abstractmethod
    def did_hide(self, request: BotRequest, messages: list, removed=True):
        pass

    @abc.abstractmethod
    def process_request(self, request: BotRequest):
        pass

    @abc.abstractmethod
    def process_message(self, request: BotRequest, messages: list):
        pass


class StateController:
    __controller_key = "__STATE_CONTROLLER__"

    def __init__(self, request: BotRequest):
        self.request = request
        if not request.user_storage:
            raise ValueError("Can't use controller without user storage")

        self.user_storage = request.user_storage
        self._default_options = {"state": []}
        self.current_state = None
        self.__removed = []
        self.__added = []
        self.__show = []
        self.__hide = []

        if not self.get_options():
            self.user_storage.update(self.__controller_key, self._default_options)

    @property
    def length(self):
        return len(self.get_options()["state"])

    @property
    def changed(self):
        return len(self.__removed or self.__added or self.__show) > 0

    def get_options(self):
        return self.user_storage.get(self.__controller_key)

    def pop(self) -> StateView:
        options = self.get_options()
        current_state = options["state"]
        if not current_state:
            return

        last = current_state.pop()
        options["state"] = current_state
        self.user_storage.update(self.__controller_key, options)

        import jsonpickle
        self.current_state = self.get_state()
        removed = jsonpickle.decode(last)()
        self.__removed.append(removed)
        self.__show.append(self.current_state)
        return removed

    def push(self, controller) -> StateView:
        options = self.get_options()
        self.__validate(controller)

        import jsonpickle
        options["state"].append(jsonpickle.encode(controller))

        self.user_storage.update(self.__controller_key, options)
        if self.current_state:
            self.__hide.append(self.current_state)

        self.current_state = controller()
        self.__added.append(self.current_state)
        self.__show.append(self.current_state)

        return self.current_state

    def pop_to_root(self) -> StateView:
        options = self.get_options()
        current_state = options["state"]
        if not current_state:
            return

        for state in current_state[1:]:
            self.__removed.append(state())

        last = current_state[0]
        options["state"] = []
        self.__show.append(last)
        self.user_storage.update(self.__controller_key, options)

        import jsonpickle
        self.current_state = jsonpickle.decode(last)()
        return self.current_state

    def get_state(self, index=None) -> StateView:
        options = self.get_options()
        current_state = options["state"]
        if not current_state:
            return

        if index is None:
            index = -1

        self.current_state = jsonpickle.decode(current_state[index])()
        return self.current_state

    def invalidate_state(self):
        self.__removed = []
        self.__added = []
        self.__show = []
        self.__hide = []

    def trigger_change_events(self, request: BotRequest, messages: list = None, is_will=False):
        for removed in self.__removed:
            self.__call_event(removed, request, messages, is_will, is_hide=True, added_or_removed=True)

        for hidden in self.__hide:
            self.__call_event(hidden, request, messages, is_will, is_hide=True, added_or_removed=False)

        for added in self.__added:
            self.__call_event(added, request, messages, is_will, is_hide=False, added_or_removed=True)

        for shown in self.__show:
            self.__call_event(shown, request, messages, is_will, is_hide=False, added_or_removed=False)

    def __call_event(self, state: StateView, request, messages, is_will, is_hide, added_or_removed=True):
        if is_will:
            if is_hide:
                state.will_hide(request, removed=added_or_removed)
            else:
                state.will_show(request, added=added_or_removed)
        else:
            if is_hide:
                state.did_hide(request, messages, removed=added_or_removed)
            else:
                state.did_show(request, messages, added=added_or_removed)

    def __validate(self, controller):
        if not issubclass(controller, StateView):
            raise ValueError("Controller %r should be subclass of StateView" % controller)
