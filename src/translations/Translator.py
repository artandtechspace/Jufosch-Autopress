import gettext
import locale
from src.translations import globals
from sys import platform

LANGUAGE_DOMAIN = "jufusch-presentation-tool"
LOCALE_PATH = "locale"

# Used by GNU/Gettext to translate strings
def _(base: str) -> str:
    return globals.i18n(base)

def load_linux_translations():
    gettext.bindtextdomain(LANGUAGE_DOMAIN, LOCALE_PATH)
    gettext.textdomain(LANGUAGE_DOMAIN)
    globals.i18n = gettext.gettext
    locale.setlocale(locale.LC_ALL, '')
    locale.bindtextdomain(LANGUAGE_DOMAIN, LOCALE_PATH)
    locale.textdomain(LANGUAGE_DOMAIN)

def load_windows_translations():
    
    def echo_back(x: str) -> str:
        return x
    
    globals.i18n = echo_back 

# Initalizes the translator
# Based on https://stackoverflow.com/a/10540744
def initalize():
    # Ensures that the os is not windows
    is_enabled = platform != "win32"

    if is_enabled:
        load_linux_translations()
    else:
        load_windows_translations()