import logging

from python_bot.bot import PythonBot, bot_logger
from python_bot.common import TelegramMessenger, MiddlewareMixin, PrintHelper, PurePythonHandler, \
    BotTextResponse, BotRequest
from python_bot.common.messenger.controllers.slack import SlackMessenger
from python_bot.settings import WebHookSettings

# Go to the Slack web API page
# https://api.slack.com/bot-users
# and sign up to create your own Slack team.
# You can also sign into an existing account where you have administrative privileges.

ACCESS_TOKEN = '{ACCESS_TOKEN}'

BOT_NAME = '{NOT_NAME}'
bot_logger.setLevel(logging.DEBUG)
with PythonBot() as bot:
    slack = bot.add_messenger(SlackMessenger, access_token=ACCESS_TOKEN)
    bot.start(wait=False)

    api_call = slack.raw_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)
