import gettext
import locale
from src.translations import globals

LANGUAGE_DOMAIN = "jufusch-presentation-tool"
LOCALE_PATH = "locale"

# Used by GNU/Gettext to translate strings
def _(base: str) -> str:
    return globals.i18n(base)


# Initalizes the translator
# Based on https://stackoverflow.com/a/10540744
def initalize():
    gettext.bindtextdomain(LANGUAGE_DOMAIN, LOCALE_PATH)
    gettext.textdomain(LANGUAGE_DOMAIN)
    globals.i18n = gettext.gettext
    locale.setlocale(locale.LC_ALL, '')
    locale.bindtextdomain(LANGUAGE_DOMAIN, LOCALE_PATH)
    locale.textdomain(LANGUAGE_DOMAIN)
