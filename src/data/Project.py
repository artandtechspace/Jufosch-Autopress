from PIL.Image import Image

from src.data.Fields import Fields
from src.data.Price import DEFAULT_PRICE
from src.data.Type import Type
from src.data.ProjectMember import ProjectMember

class Project:

    def __init__(self, name: str, location: str, type: Type, field: Fields, stand_number: int,
                 members: [ProjectMember]):
        self.name = name
        self.location = location
        self.type = type
        self.field = field
        self.stand_number = stand_number
        self.members = members
        # Special price name: [Presentation, Lookup]
        self.special_price_name = ["",""]
        self.price = DEFAULT_PRICE
        self.image: Image = None

    def get_raw_stand_number(self):
        return "{}{}{:03d}".format(self.type.value[1], self.field.value[1], self.stand_number)

    def __str__(self):
        members = ""
        for x in self.members:
            members += str(x)+" "

        return "Project(Name: '{}', Location: '{}', Type: '{}', Field: '{}', Stand: '{}', Members: ({}))".format(self.name, self.location, self.type.value[0], self.field.value[0], self.stand_number, members)