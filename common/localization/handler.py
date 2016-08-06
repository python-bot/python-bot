class LocalizationMixIn(object):
    @staticmethod
    def locale_make():
        from python_bot.common.localization.makemessages import LocaleMessages
        LocaleMessages().make_messages()

    @staticmethod
    def locale_compile():
        from python_bot.common.localization.makemessages import LocaleMessages
        LocaleMessages().compile_messages()
