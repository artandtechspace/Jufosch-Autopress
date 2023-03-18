from gi.repository import GdkPixbuf

# Reference-path to load a resource
__load_logo = GdkPixbuf.Pixbuf.new_from_file_at_size

JUFO_LOGO : GdkPixbuf.Pixbuf = __load_logo("rsc/LOGO_JUFO.png", 32, 32)
JUFO_LOGO_SMALL = __load_logo("rsc/LOGO_JUFO_NOTEXT.png", 16, 16)
SUEX_LOGO = __load_logo("rsc/LOGO_SUEX.png", 32, 32)
SUEX_LOGO_SMALL = __load_logo("rsc/LOGO_SUEX_NOTEXT.png", 16, 16)

SPECIAL_PRICE_NAME_SUGGESTIONS = "rsc/SpecialpriceNames.txt"

ICON_LO_IMPRESS = __load_logo("rsc/icon/LO_IMPRESS.png", 16, 16)
ICON_LO_CALC = __load_logo("rsc/icon/LO_CALC.png", 16, 16)
ICON_IMAGES_FOLDER = __load_logo("rsc/icon/IMAGES_FOLDER.png", 16, 16)
ICON_MEDAL = __load_logo("rsc/icon/MEDAL.png", 16, 16)
ICON_OPEN_ALL = __load_logo("rsc/icon/OPEN_ALL.png", 16, 16)