import csv
from src.data.Fields import Fields, parse_field
from src.data.Type import Type, parse_type
from src.data.ProjectMember import ProjectMember
from src.data.Project import Project
import io
from src.translations.Translator import _


def __load_members(ages: [str], first_names: [str], last_names: [str], project_name: str):
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
            raise ValueError(_("Firstname of the {id} user ('{name}') is empty").format(id=idx + 1, name=project_name))
        if not lname_valid:
            raise ValueError(_("Lastname of the {id} user ('{name}') is empty").format(id=idx + 1, name=project_name))
        if not age_valid:
            raise ValueError(_("Age of the {id} user ('{name}') is empty").format(id=idx + 1, name=project_name))

        # Ensures the age has the correct suffix
        if not age.endswith(" Jahre"):
            raise ValueError(
                _("Age of the {id} user ('{name}') is invalid, ' Jahre' must be the suffix of the age-field").format(id=idx + 1, name=project_name))

        # Gets the real age-number without suffix
        age = age[:-len(" Jahre")]

        # Ensures the age is a valid positive number
        if not age.isdigit():
            raise ValueError(_("Age of the {id} user ('{name}') is not a digit. Found '{raw}'.").format(idx + 1, age, name=project_name))

        # Gets the real age
        age_int = int(age)

        # Appends the members
        members.append(ProjectMember(fname, lname, age_int))

    # Ensures that at least one single project member got found
    if len(members) <= 0:
        raise ValueError(_("The project '{name}' has no members").format(name=project_name))

    return members


def __save_index(data: list[str], value: str):
    try:
        return data.index(value)
    except ValueError:
        raise ValueError(_("Field '{value}' wasn't found").format(value=value))


def __get_stand_number(raw_number: str, field: Fields, type: Type, project_name: str):
    # Ensures a correct length
    if len(raw_number) != 5:
        raise ValueError(
            _("The standnumber from '{name}' must be 5 characters in length - found '{number}' ({length})").format(
                name=project_name, number=raw_number, length=len(raw_number)))

    # Ensures the correct type
    if raw_number[0] != type.value[1]:
        raise ValueError(
            _("The standnumber from '{name}' doesn't match it's type (JUFO/SUEX) - found '{number}', wanted '{type}'").format(
                name=project_name, number=raw_number, type=type.value[0]))

    # Ensures the correct field
    if raw_number[1] != field.value[1]:
        raise ValueError(
            _("The standnumber from '{name}' doesn't match it's field - found '{number}', wanted '{field}'").format(
                name=project_name, number=raw_number, field=field.value[0]))

    # Cuts away the redundant information
    raw_number_digit = raw_number[2:]

    # Ensures a correct number
    if not raw_number_digit.isdigit():
        raise ValueError(_("Number part of standnumber from '{name}' isn't a number...").format(name=raw_number))

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
                    raise ValueError(
                        _("Project-row '{row}' has an invalid length - found {length}, required {requirement}").format(
                            row=row, length=len(row), requirement=len(fields)))

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
                members = __load_members(DATA_MEMBERS_AGE, DATA_MEMBERS_FIRSTNAME, DATA_MEMBERS_LASTNAME, DATA_TITLE)

                # Parses the field
                field = parse_field(DATA_FACH)

                # Ensures the field is valid
                if field == None:
                    raise ValueError(
                        _("Field from '{name}' ('{field}') is invalid").format(name=DATA_TITLE, field=DATA_FACH))

                # Parses the type
                type = parse_type(DATA_SPARTE)

                # Ensure the type is valid
                if type == None:
                    raise ValueError(_("Type (JUFO/SUEX) from '{name}' ('{type}') is invalid").format(name=DATA_TITLE,
                                                                                                      type=DATA_FACH))

                # Ensures the stand number is valid
                stand_number = __get_stand_number(DATA_STANDNUMMER, field, type, DATA_TITLE)

                # Validates that the standnumber isn't duplicated
                if DATA_STANDNUMMER in loaded_ids:
                    raise ValueError(
                        _("Standnumber of project '{name}' ('{id}') is duplicated!").format(name=DATA_TITLE,
                                                                                            id=DATA_STANDNUMMER))

                loaded_ids.append(DATA_STANDNUMMER)

                projects.append(Project(DATA_TITLE, DATA_ERARBEITUNGSORT, type, field, stand_number, members))

        return projects

    except FileNotFoundError:
        raise ValueError(_("File couldn't be opened"))
