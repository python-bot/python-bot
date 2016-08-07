import codecs
import gettext
import locale
import logging
import os

from python_bot.settings import LOCALE_DIR


def has_bom(fn):
    with open(fn, 'rb') as f:
        sample = f.read(4)
    return sample.startswith((codecs.BOM_UTF8, codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE))


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception:
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()


def init_localization(user_locale=None, path=None):
    if not user_locale:
        locale.setlocale(locale.LC_ALL, '')  # use user's preferred locale
        # take first two characters of country code
        loc = locale.getlocale()
        user_locale = loc[0][:2]
    if not path:
        filename = os.path.join(LOCALE_DIR, user_locale, "LC_MESSAGES", "python_bot.mo")
    else:
        filename = os.path.join(path, user_locale, "LC_MESSAGES", "python_bot.mo")

    try:
        logging.debug("Opening message file %s for locale %s", filename, user_locale)
        trans = gettext.GNUTranslations(open(filename, "rb"))
    except IOError:
        logging.debug("Locale not found. Using default messages")
        trans = gettext.NullTranslations()

    trans.install()
    return trans
