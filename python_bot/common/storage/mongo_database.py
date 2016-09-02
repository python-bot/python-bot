from python_bot.common.storage.base import StorageAdapter, UserStorageAdapter


# Not working
class MongoDatabaseAdapter(StorageAdapter):
    """
    The MongoDatabaseAdapter is an interface that allows ChatterBot
    to store the conversation as a MongoDB database.
    """

    def create_user_storage(self, **kwargs):
        _kwargs = self.kwargs.copy()
        _kwargs.update(kwargs)
        return UserMongoDatabaseAdapter(**_kwargs)

    def __init__(self, **kwargs):
        super(MongoDatabaseAdapter, self).__init__(**kwargs)

        self.database_name = self.kwargs.get(
            "database", "python-bot-database"
        )
        self.database_uri = self.kwargs.get(
            "database_uri", "mongodb://localhost:27017/"
        )

        # Use the default host and port
        from pymongo import MongoClient
        self.client = MongoClient(self.database_uri)

        # Specify the name of the database
        self.database = self.client[self.database_name]

        # Set a requirement for the text attribute to be unique
        self.statements.create_index('text', unique=True)

    def _keys(self, filter_func=None):
        keys = self.database.keys()
        return list(filter(filter_func, keys) if callable(filter_func) else keys)

    def count(self, filter_func=None):
        return len(self._keys(filter_func))

    def get(self, statement_text):
        values = self.database.find_one({'key': statement_text})

        if not values:
            return None

        return values

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        filter_parameters = kwargs.copy()
        contains_parameters = {}

        # Convert Message objects to data
        if "in_message_to" in filter_parameters:
            message_objects = filter_parameters["in_message_to"]
            serialized_messages = []
            for message in message_objects:
                serialized_messages.append(message.serialize())

            filter_parameters["in_message_to"] = serialized_messages

        # Exclude special arguments from the kwargs
        for parameter in kwargs:

            if "__" in parameter:
                del (filter_parameters[parameter])

                kwarg_parts = parameter.split("__")

                if kwarg_parts[1] == "contains":
                    key = kwarg_parts[0]
                    value = kwargs[parameter]

                    contains_parameters[key] = {
                        '$elemMatch': {
                            'text': value
                        }
                    }

        filter_parameters.update(contains_parameters)

        matches = self.statements.get(filter_parameters)
        matches = list(matches)

        results = []

        for match in matches:
            statement_text = match['text']
            del (match['text'])

            message_list = self.deserialize_messages(match["in_message_to"])
            match["in_message_to"] = message_list

            results.append(statement_text)

        return results

    def update(self, statement):
        from pymongo import UpdateOne, ReplaceOne

        # Do not alter the database unless writing is enabled
        if not self.read_only:
            data = statement.serialize()

            operations = []

            update_operation = ReplaceOne(
                {'text': statement.text}, data, True
            )
            operations.append(update_operation)

            # Make sure that an entry for each message is saved
            for message in statement.in_message_to:
                # $setOnInsert does nothing if the document is not created
                update_operation = UpdateOne(
                    {'text': message.text},
                    {'$setOnInsert': {'in_message_to': []}},
                    upsert=True
                )
                operations.append(update_operation)

            self.statements.bulk_write(operations, ordered=False)

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from random import randint

        count = self.count()

        random_integer = randint(0, count - 1)

        if self.count() < 1:
            raise self.EmptyDatabaseException()

        statement = self.statements.get().limit(1).skip(random_integer)

        values = list(statement)[0]
        statement_text = values['text']

        del (values['text'])
        return statement_text

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any messages from statements if the message text matches the
        input text.
        """
        for statement in self.filter(in_message_to__contains=statement_text):
            statement.remove_message(statement_text)
            self.update(statement)

        self.database.delete_one({'text': statement_text})

    def drop(self):
        """
        Remove the database.
        """
        self.client.drop_database(self.database_name)


class UserMongoDatabaseAdapter(UserStorageAdapter, MongoDatabaseAdapter):
    pass
