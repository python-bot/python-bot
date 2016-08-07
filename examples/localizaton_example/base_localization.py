import os

from python_bot.bot import PythonBot

# In this example we will work with localization our messages
# to make and compile messages use
# bot.locale_make()
# bot.locale_compile()

locale_path = os.path.join(os.path.dirname(__file__), "locale")
bot = PythonBot(locale={"path": locale_path})

assert bot.localize_message("Test") == "Test"
bot.switch_locale("ru")

assert bot.localize_message("Test") == "Тест"
