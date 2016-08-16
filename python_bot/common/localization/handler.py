from python_bot.common.localization.base import init_localization


class LocalizationMixIn:
    def __init__(self):
        self._trans = None
        super().__init__()

    def locale_make(self, **kwargs):
        from python_bot.common.localization.makemessages import LocaleMessages
        self._update_kwargs(kwargs)
        LocaleMessages(**kwargs).make_messages()

    def locale_compile(self, **kwargs):
        from python_bot.common.localization.makemessages import LocaleMessages
        self._update_kwargs(kwargs)
        LocaleMessages(**kwargs).compile_messages()

    def switch_locale(self, locale=None):
        self.settings["locale"]["lang"] = locale
        self._trans = init_localization(locale, path=self.settings["locale"].get("path"))
        return self._trans

    def localize_message(self, message: str):
        if not self._trans:
            self._trans = init_localization(self.settings["locale"]["lang"], path=self.settings["locale"].get("path"))
        return self._trans.gettext(message)

    def _update_kwargs(self, kwargs):
        locale = kwargs.pop("locale", [])
        lang = self.settings["locale"].get("lang")
        if lang:
            locale.append(lang)

        locale_paths = kwargs.pop("locale_paths", [])
        path = self.settings["locale"].get("path")
        if path:
            locale_paths.append(path)

        kwargs["locale_paths"] = locale_paths
        kwargs["locale"] = locale
