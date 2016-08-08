from python_bot.bot import PythonBot

# Adding echo middleware which send message to bot the same as request

with PythonBot(middleware={"python_bot.tests.common.middleware.EchoMiddleware": {}},
               messenger={"python_bot.common.messenger.controllers.console.ConsoleMessenger": {}}) as bot:
    # Simulate on message event
    bot.converse(quit="quit")
