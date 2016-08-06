from python_bot.common.localization.base import init_localization, system_trans


class LocalizationMixIn(object):
    def __init__(self):
        self._trans = system_trans

    @staticmethod
    def locale_make(**kwargs):
        from python_bot.common.localization.makemessages import LocaleMessages
        LocaleMessages(**kwargs).make_messages()

    @staticmethod
    def locale_compile(**kwargs):
        from python_bot.common.localization.makemessages import LocaleMessages
        LocaleMessages(**kwargs).compile_messages()

    def switch_locale(self, locale=None):
        self._trans = init_localization(locale)
        return self._trans

    def localize_message(self, message: str):
        return self._trans.gettext(message)
