import os
from gettext import gettext as _

__all__ = ["UserInfo"]


class UserInfo:
    def __init__(self, user_id, first_name="", last_name="", username="",
                 profile_pic="", locale=None, timezone=None, is_male=True):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.profile_pic = profile_pic
        self.locale = locale
        self.timezone = timezone  # float (min: -24) (max: 24)
        self.is_male = is_male

    def __repr__(self):
        out = "%s: %s %s " % (self.user_id, self.first_name, self.last_name)
        if self.locale:
            out += os.linesep + _("Locale: ") + self.locale
        if self.timezone:
            out += os.linesep + _("Timezone: ") + str(self.timezone)
        return out
