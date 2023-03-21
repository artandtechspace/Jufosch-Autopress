from gi.repository import GdkPixbuf
import os
import sys


# Returns the given path to ressources (Used to ensure packaged applications will also have valid ressource-paths)
# For more info read https://stackoverflow.com/a/13790741
def __resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Basic-Ressource-path
RSC_PATH = __resource_path("src/rsc")

# Reference-path to load a resource
__load_logo = GdkPixbuf.Pixbuf.new_from_file_at_size

JUFO_LOGO: GdkPixbuf.Pixbuf = __load_logo(RSC_PATH + "/LOGO_JUFO.png", 32, 32)
JUFO_LOGO_SMALL = __load_logo(RSC_PATH + "/LOGO_JUFO_NOTEXT.png", 16, 16)
SUEX_LOGO = __load_logo(RSC_PATH + "/LOGO_SUEX.png", 32, 32)
SUEX_LOGO_SMALL = __load_logo(RSC_PATH + "/LOGO_SUEX_NOTEXT.png", 16, 16)

SPECIAL_PRICE_NAME_SUGGESTIONS = RSC_PATH + "/SpecialpriceNames.txt"

ICON_LO_IMPRESS = __load_logo(RSC_PATH + "/icon/LO_IMPRESS.png", 16, 16)
ICON_LO_CALC = __load_logo(RSC_PATH + "/icon/LO_CALC.png", 16, 16)
ICON_IMAGES_FOLDER = __load_logo(RSC_PATH + "/icon/IMAGES_FOLDER.png", 16, 16)
ICON_MEDAL = __load_logo(RSC_PATH + "/icon/MEDAL.png", 16, 16)
ICON_OPEN_ALL = __load_logo(RSC_PATH + "/icon/OPEN_ALL.png", 16, 16)
