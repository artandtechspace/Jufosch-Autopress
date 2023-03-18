class ProjectMember:

    def __init__(self, first_name: str, last_name: str, age: int):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def get_short_description(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.age)

    def __str__(self):
        return "Member(Name: '{}'-'{}', Age: '{}')".format(self.first_name, self.last_name, self.age)