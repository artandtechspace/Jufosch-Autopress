from enum import Enum

class Fields(Enum):
    PHYSICS = "Physik", "P"
    TECHNICS = "Technik", "T"
    MATH_AND_INFO = "Mathematik/Informatik", "M"
    GEO_AND_SPACE = "Geo- und Raumwissenschaften", "G"
    BIOLOGY = "Biologie", "B"
    CHEMISTRY = "Chemie", "C"
    REAL_WORLD = "Arbeitswelt", "A"

# Takes in the value and returns a field
def parse_field(name: str):
    for x in Fields:
        if x.value[0] == name:
            return x
    return None
