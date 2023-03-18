
# Types of placeholders
__TYPE_BODY = 2
__TYPE_TITLE = 1
__TYPE_PICTURE = 18
__TYPE_OBJECT = 7

__COMMON_IMAGE = [__TYPE_PICTURE]
__COMMON_TEXT = [__TYPE_OBJECT, __TYPE_BODY, __TYPE_TITLE]

'''
All below placeholders have firstly their identify text as
the first object and secondly an array of placeholder-types that the placeholder must be an instance of
'''

MEMBER_1 = ("Schüler 1", __COMMON_TEXT)
MEMBER_2 = ("Schüler 2", __COMMON_TEXT)
MEMBER_3 = ("Schüler 3", __COMMON_TEXT)
SCHOOL = ("Schulname", __COMMON_TEXT)

PROJECT_IMAGE = ("Projektbild", __COMMON_IMAGE)

PROJECT_TITLE = ("Überschrift", __COMMON_TEXT)

NOTES = ("Notizen", __COMMON_TEXT)

LOOKUP_PRICE_1 = ("Preis 1", __COMMON_IMAGE)
LOOKUP_PRICE_2 = ("Preis 2", __COMMON_IMAGE)

PROJECT_PRICES_1_FLYIN_TEXT = ("Preis 1 text einfiegend", __COMMON_TEXT)
PROJECT_PRICES_1_FLYIN_IMAGE = ("Preis 1 bild einfliegend", __COMMON_IMAGE)
PROJECT_PRICES_2_FLYIN_TEXT = ("Preis 2 text einfiegend", __COMMON_TEXT)
PROJECT_PRICES_2_FLYIN_IMAGE = ("Preis 2 bild einfliegend", __COMMON_IMAGE)
PROJECT_PRICES_1_ROTATING_TEXT = ("Preis 1 text rotierend", __COMMON_TEXT)
PROJECT_PRICES_1_ROTATING_IMAGE = ("Preis 1 bild rotierend", __COMMON_IMAGE)
PROJECT_PRICES_2_ROTATING_TEXT = ("Preis 2 text rotierend", __COMMON_TEXT)
PROJECT_PRICES_2_ROTATING_IMAGE = ("Preis 2 bild rotierend", __COMMON_IMAGE)
