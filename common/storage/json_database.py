from jsondb import Database

from python_bot.common.storage.base import StorageAdapter, UserStorageAdapter


class JsonDatabaseAdapter(StorageAdapter):
    """
    The JsonDatabaseAdapter is an interface that allows ChatterBot
    to store the conversation as a Json-encoded file.
    """

    def __init__(self, **kwargs):
        super(JsonDatabaseAdapter, self).__init__(**kwargs)

        database_path = self.kwargs.get("database", "database.db")
        self.database = Database(database_path)

    def _keys(self, filter_func=None):
        keys = self.database[0].keys()
        return list(filter(filter_func, keys) if callable(filter_func) else keys)

    def count(self, filter_func=None):
        return len(self._keys(filter_func))

    def find(self, statement_text):
        values = self.database.data(key=statement_text)

        if not values:
            return None

        return values

    def remove(self, statement_text):
        self.database.delete(statement_text)

    def _all_kwargs_match_values(self, kwarguments, values):
        for kwarg in kwarguments:

            if "__" in kwarg:
                kwarg_parts = kwarg.split("__")

                key = kwarg_parts[0]
                identifier = kwarg_parts[1]

                if identifier == "contains":
                    text_values = []
                    for val in values[key]:
                        text_values.append(val["text"])

                    if (kwarguments[kwarg] not in text_values) and (
                                kwarguments[kwarg] not in values[key]):
                        return False

            if kwarg in values:
                if values[kwarg] != kwarguments[kwarg]:
                    return False

        return True

    def filter(self, filter_func=None, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        results = []

        for key in self._keys(filter_func):
            values = self.database.data(key=key)

            if self._all_kwargs_match_values(kwargs, values):
                results.append(values)

        if not results:
            return None

        return results

    def update(self, key, value):
        # Do not alter the database unless writing is enabled
        if not self.read_only:
            self.database.data(key=key, value=value)
            return True
        return False

    def get_random(self, key):
        from random import choice

        if self.count() < 1:
            raise self.EmptyDatabaseException()

        statement = choice(self._keys())
        return self.find(statement)

    def drop(self):
        """
        Remove the json file database completely.
        """
        import os

        if os.path.exists(self.database.path):
            os.remove(self.database.path)


class UserJsonDatabaseAdapter(UserStorageAdapter, JsonDatabaseAdapter):
    pass
