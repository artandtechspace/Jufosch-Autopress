from PIL import Image

from src.core.presentation.data.LoadedPresentation import LoadedPresentation
from src.core.presentation.data.PresentationFactory import PresentationFactory
from src.data.Price import PriceAnimation, score_price, DEFAULT_PRICE, NormalPriceTypes
from enum import Enum

from src.data.Project import Project


class PresentationType(Enum):
    LOOKUP = 0
    NORMAL = 1

# Returns all projects sorted by stand
def __get_sorted_projects(projects: list[Project]):
    return sorted(projects, key=lambda p: p.get_raw_stand_number())

# Returns all projects with a price, sorted in order of presentation
def __get_sorted_priced_projects(projects: list[Project]):
    # Filters for only the prices projects
    projects = list(filter(lambda p: p.price != DEFAULT_PRICE, projects))

    return sorted(projects, key=lambda p: score_price(p.price))

def __create_slides(factory: PresentationFactory, projects: list[Project], with_project_images: bool, with_price_slides: bool,
                           with_project_slides: bool, type: PresentationType):

    # Creates normal slides
    if with_project_slides:
        # Sorts the projects based on their stand number
        projects = __get_sorted_projects(projects)

        for i in range(len(projects)):
            proj = projects[i]

            # Checks which slide type should be created
            if type == PresentationType.NORMAL:
                factory.create_project_slide(
                    project=proj,
                    with_project_image=with_project_images,
                    with_prices=False
                )
            else:
                factory.create_lookup_slide(
                    project=proj,
                    with_prices=False
                )

    # Creates the price-slides
    if with_price_slides:
        # Sorts the projects based on their price
        projects = __get_sorted_priced_projects(projects)

        for i in range(len(projects)):
            proj = projects[i]

            # Checks which slide type should be created
            if type == PresentationType.NORMAL:
                factory.create_project_slide(
                    project=proj,
                    with_project_image=with_project_images,
                    with_prices=True,
                    animation=PriceAnimation.FLYIN if i & 1 == 0 else PriceAnimation.ROTATING
                )
            else:
                factory.create_lookup_slide(
                    project=proj,
                    with_prices=True
                )

# Exports the loaded presentation based on the settings
# Either with_project_slides or with_lookup_slides should be enabled as otherwise no slides will be generated
# If generate_project_slides is enabled, the normal project-slides will be generated,
# If price_images are not None, price slides will also be generated
# If project_images are given, the projects will also have their corresponding image if it exists
# raises ValueError if anything went wrong with saving the presentation
def export_presentation(
        presentation: LoadedPresentation,
        projects: list[Project],
        export_path: str,

        with_normal_slides: bool = True,
        with_lookup_slides: bool = False,
        generate_project_slides: bool = False,

        project_images: {str: Image} = None,
        price_images: ({NormalPriceTypes: Image}, Image) = None
):
    # Creates the factory
    factory = PresentationFactory(
        presentation=presentation.root,
        field_layouts=presentation.field_layouts,
        lookup_layout=presentation.lookup_layout,

        # Optional (None/Ignored if not existing)
        price_images=price_images[0] if price_images is not None else None,
        special_price_image=price_images[1] if price_images is not None else None,
        project_images=project_images
    )

    # Generates the normal slides
    if with_normal_slides:
        __create_slides(
            factory=factory,
            projects=projects,
            with_price_slides=price_images is not None,
            with_project_images=project_images is not None,
            with_project_slides=generate_project_slides,
            type=PresentationType.NORMAL
        )
    # Generates the normal slides
    if with_lookup_slides:
        __create_slides(
            factory=factory,
            projects=projects,
            with_price_slides=price_images is not None,
            with_project_images=project_images is not None,
            with_project_slides=generate_project_slides,
            type=PresentationType.LOOKUP
        )

    try:
        # Tries to save the presentation
        factory.presentation.save(export_path)
    except:
        # TODO: Language
        raise ValueError("failed to save the presentation")
