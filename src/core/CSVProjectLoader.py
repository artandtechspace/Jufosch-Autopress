import csv
from src.data.Fields import Fields, parse_field
from src.data.Type import Type, parse_type
from src.data.ProjectMember import ProjectMember
from src.data.Project import Project
import io

def __load_members(ages: [str], first_names: [str], last_names: [str]):
    # Array that will hold all members that the end
    members = []

    # Creates every student
    for idx in range(3):
        fname = first_names[idx].strip()
        lname = last_names[idx].strip()
        age = ages[idx].strip()

        fname_valid = len(fname) > 0
        lname_valid = len(lname) > 0
        age_valid = len(age) > 0

        # Checks if the member just doesn't exist
        if not fname_valid and not lname_valid and not age_valid:
            continue

        # Ensures the data is valid
        if not fname_valid:
            raise ValueError("member.firstname.empty", [idx + 1, fname])
        if not lname_valid:
            raise ValueError("member.lastname.empty", [idx + 1, lname])
        if not age_valid:
            raise ValueError("member.age.empty", [idx + 1, age])

        # Ensures the age has the correct suffix
        if not age.endswith(" Jahre"):
            raise ValueError("member.age.invalid", [idx + 1, age])

        # Gets the real age-number without suffix
        age = age[:-len(" Jahre")]

        # Ensures the age is a valid positive number
        if not age.isdigit():
            raise ValueError("member.age.invalid", [idx + 1, age])

        # Gets the real age
        age_int = int(age)

        # Appends the members
        members.append(ProjectMember(fname, lname, age_int))

    # Ensures that at least one single project member got found
    if len(members) <= 0:
        raise ValueError("members.nomember")

    return members


def __save_index(data: list[str], value: str):
    try:
        return data.index(value)
    except ValueError:
        raise ValueError("field.notfound", [value])


def __get_stand_number(raw_number: str, field: Fields, type: Type):
    # Ensures a correct length
    if len(raw_number) != 5:
        raise ValueError("standnumber.length", [raw_number])

    # Ensures the correct type
    if raw_number[0] != type.value[1]:
        raise ValueError("standnumber.type", [raw_number])

    # Ensures the correct field
    if raw_number[1] != field.value[1]:
        raise ValueError("standnumber.field", [raw_number])

    # Cuts away the redundant information
    raw_number_digit = raw_number[2:]

    # Ensures a correct number
    if not raw_number_digit.isdigit():
        raise ValueError("standnumber.number", [raw_number])

    # Parses the number
    return int(raw_number_digit)


# Takes in a path/file to a csv-projects file and tries to load it
# Either raises an FileNotFoundError or ValueError if something went wrong,
# or return all loaded projects as a list[Project]
def load_projects_from_file(file_name: str):
    try:
        # Interprets the csv-file with all projects
        with io.open(file_name, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')

            # Reads in the first line, the fields
            fields = reader.__next__()

            FLD_SPARTE = __save_index(fields, "Sparte")
            FLD_FACH = __save_index(fields, "Fachgebiet")
            FLD_TITLE = __save_index(fields, "Projekttitel")
            FLD_STANDNUMMER = __save_index(fields, "Standnummer")
            FLD_TEILNAHMESTATUS = __save_index(fields, "Teilnahmestatus")
            FLD_ERARBEITUNGSORT = __save_index(fields, "Erarbeitungsort")

            FLDS_MEMBERS_AGE = [__save_index(fields, "T" + str(x + 1) + " Alter") for x in range(3)]
            FLDS_MEMBERS_FIRSTNAME = [__save_index(fields, "T" + str(x + 1) + " Vorname") for x in range(3)]
            FLDS_MEMBERS_LASTNAME = [__save_index(fields, "T" + str(x + 1) + " Nachname") for x in range(3)]

            # List with all loaded stand numbers
            loaded_ids = []

            # List with all projects
            projects: list[Project] = []

            # Iterates over all projects
            for row in reader:

                # Ensures the length matches
                if len(row) != len(fields):
                    raise ValueError("proj.row.invalid", [row])

                # Loads the fields
                DATA_SPARTE = row[FLD_SPARTE]
                DATA_FACH = row[FLD_FACH]
                DATA_TITLE = row[FLD_TITLE]
                DATA_STANDNUMMER = row[FLD_STANDNUMMER]
                DATA_TEILNAHMESTATUS = row[FLD_TEILNAHMESTATUS]
                DATA_ERARBEITUNGSORT = row[FLD_ERARBEITUNGSORT]

                DATA_MEMBERS_AGE = [row[x] for x in FLDS_MEMBERS_AGE]
                DATA_MEMBERS_FIRSTNAME = [row[x] for x in FLDS_MEMBERS_FIRSTNAME]
                DATA_MEMBERS_LASTNAME = [row[x] for x in FLDS_MEMBERS_LASTNAME]

                # Ensures the project is still going
                if DATA_TEILNAHMESTATUS != "Nimmt teil":
                    continue

                # Gets the members
                members = __load_members(DATA_MEMBERS_AGE, DATA_MEMBERS_FIRSTNAME, DATA_MEMBERS_LASTNAME)

                # Parses the field
                field = parse_field(DATA_FACH)

                # Ensures the field is valid
                if field == None:
                    raise ValueError("proj.field.invalid", [DATA_FACH])

                # Parses the type
                type = parse_type(DATA_SPARTE)

                # Ensure the type is valid
                if type == None:
                    raise ValueError("proj.type.invalid", [DATA_SPARTE])

                # Ensures the stand number is valid
                stand_number = __get_stand_number(DATA_STANDNUMMER, field, type)

                # Validates that the standnumber isn't duplicated
                if DATA_STANDNUMMER in loaded_ids:
                    raise ValueError("proj.standnumber.duplicated")

                loaded_ids.append(DATA_STANDNUMMER)

                projects.append(Project(DATA_TITLE, DATA_ERARBEITUNGSORT, type, field, stand_number, members))

        return projects

    except FileNotFoundError:
        raise ValueError("file.open")
