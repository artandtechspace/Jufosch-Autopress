from enum import Enum


class Type(Enum):
    JUFO = "JF", "J"
    SUEX = "SE", "S"

# Takes in the value and returns a type
def parse_type(name: str):
    for x in Type:
        if x.value[0] == name:
            return x
    return None
