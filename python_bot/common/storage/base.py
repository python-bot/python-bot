import abc


class Adapter(metaclass=abc.ABCMeta):
    """
    An abstract superclass for all adapters
    """

    def __init__(self, **kwargs):
        self.context = None

    def set_context(self, context):
        self.context = context

    class AdapterMethodNotImplementedError(NotImplementedError):
        def __init__(self, message="This method must be overridden in a subclass method."):
            self.message = message

        def __str__(self):
            return self.message


class StorageAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all storage adapters should implement.
    """

    @staticmethod
    @abc.abstractmethod
    def create_user_storage(self, **kwargs):
        pass

    def __init__(self, **kwargs):
        super(StorageAdapter, self).__init__(**kwargs)

        self.kwargs = kwargs
        self.read_only = kwargs.get("read_only", False)

    @abc.abstractmethod
    def count(self, filter_func=None):
        """
        Return the number of entries in the database.
        """
        pass

    @abc.abstractmethod
    def get(self, statement_text, default=None):
        """
        Returns a object from the database if it exists
        """
        pass

    @abc.abstractmethod
    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any messages from statements where the message text matches
        the input text.
        """
        pass

    @abc.abstractmethod
    def filter(self, filter_func=None, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain
        all listed attributes and in which all values
        match for all listed attributes will be returned.
        """
        pass

    @abc.abstractmethod
    def update(self, key, value):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        pass

    @abc.abstractmethod
    def get_random(self, key):
        """
        Returns a random statement from the database
        """
        pass

    @abc.abstractmethod
    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        pass

    class EmptyDatabaseException(Exception):
        def __init__(self, value="The database currently contains no entries. At least one entry is expected."):
            self.value = value

        def __str__(self):
            return repr(self.value)


class UserStorageAdapter(StorageAdapter):
    PROPERTY_SEPARATOR = "__"

    def drop(self):
        super().drop()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "user_id" not in self.kwargs:
            raise ValueError("You need to specify user id")

        if "database_name" not in self.kwargs:
            raise ValueError("You need to specify database name")

        self.user_id = str(self.kwargs["user_id"])
        self.database_name = self.kwargs["database_name"]

        if not self.user_id:
            raise ValueError("user_id is not set")

    def _format_key(self, key):
        return self.PROPERTY_SEPARATOR.join((self.database_name, self.user_id, key))

    def _default_filter_func(self, key):
        return key.startswith(self.PROPERTY_SEPARATOR.join((self.database_name, self.user_id)))

    def update(self, key, value):
        return super().update(self._format_key(key), value)

    def remove(self, key):
        return super().remove(self._format_key(key))

    def filter(self, filter_func=None, **kwargs):
        if not filter_func:
            filter_func = self._default_filter_func
        return super().filter(filter_func, **kwargs)

    def count(self, filter_func=None):
        if not filter_func:
            filter_func = self._default_filter_func
        return super().count(filter_func)

    def get_random(self, key):
        return super().get_random(self._format_key(key))

    def get(self, key, default=None):
        return super().get(self._format_key(key), default=default)
