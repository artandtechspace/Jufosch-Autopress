import os
import re

from PIL import Image

from src.data.Price import NormalPriceTypes

__PROJECT_REGEX = "^(J|S)(P|T|M|G|B|C|A)(\d{3})\.\w+$"

# File-names for the price-types
__PRICES = {
    NormalPriceTypes.FIRST: "first.png",
    NormalPriceTypes.SECOND: "second.png",
    NormalPriceTypes.THIRD: "third.png"
}
# Filename for the special file
__SPECIAL_PRICE_NAME = "special.png"


# Takes in a path to a folder with the price-images
# Loads these images and returns a tuple with the following:
# (
#   {NormalPriceTypes: Image},  # for the normal prices
#   Image                       # Special price image
# )
#
def load_price_images(path):
    # TODO: Language

    # Helper-function to convert any error while loading the image to a single value-error
    def load_img(name):
        # Tries to load the image
        try:
            return Image.open(os.path.join(path, name), "r")
        except:
            raise ValueError("Bild '" + str(name) + "' konnte nicht geladen werden.")

    # Will contain all loaded images
    price_images: {NormalPriceTypes: Image} = {}

    # Loads the normal images
    for price in __PRICES:
        price_images[price] = load_img(__PRICES[price])

    # Loads the special price
    return (
        price_images,
        load_img(__SPECIAL_PRICE_NAME)
    )


# Takes in a folder-path were only project-images should be located using the __PROJECT_REGEX
# format to match them to their respective projects
# This loads all those images and returns a tuple of the following:
# (
#   invalid_images: [str],
#   invalid_names: [str],
#   duplicated_images: [str],
#   loaded_images: {str: Image}
# )
def load_project_images_from_folder(path):
    invalid_names = []
    invalid_images = []
    duplicated_images = []
    loaded_images: {str: Image} = {}

    # Iterates over all files
    for f in os.listdir(path):
        # Gets the full file-path
        filepath = os.path.join(path, f)

        # Ensures a file
        if not os.path.isfile(filepath):
            continue

        # Checks if the file-name matches
        if not re.search(__PROJECT_REGEX, f):
            # Registers invalid file
            invalid_names.append(f)
            continue

        # Tries to load the image
        try:
            img = Image.open(filepath, "r")

            # Gets the project-only-name
            proj_name = f[:5]

            # Checks for duplicated names
            if proj_name in loaded_images and proj_name not in duplicated_images:
                duplicated_images.append(proj_name)

            # Appends the name
            loaded_images[proj_name] = img
        except:
            # Registers the image
            invalid_images.append(f)

    # Returns the results
    return (
        invalid_images,
        invalid_names,
        duplicated_images,
        loaded_images
    )
