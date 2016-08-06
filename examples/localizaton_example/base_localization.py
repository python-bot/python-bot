from python_bot.bot import PythonBot

bot = PythonBot()

# make and compile message
# bot.locale_make(locale=["ru"])
# bot.locale_compile(locale=["ru"])

bot.switch_locale("ru")

print(bot.localize_message("Yes"))
