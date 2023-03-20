'''
This file holds user-loaded ressources like the presentation or projects
'''
from PIL import Image

from src.core.presentation.data.LoadedPresentation import LoadedPresentation
from src.data.Price import NormalPriceTypes
from src.data.Project import Project
from src.ui import Signals
from src.utils import EventDispatcher

# Project list (CSV)
projects: list[Project] = None

# Presentation (PPTX)
presentation: LoadedPresentation = None

# Project-Images (Folder)
project_images: {str: Image} = None

# Price-Images (Price)
price_images: ({NormalPriceTypes: Image}, Image) = None


def on_presentation_load(obj: LoadedPresentation | None):
    global presentation
    presentation = obj


def on_projects_load(obj: list[Project] | None):
    global projects
    projects = obj


def on_project_images_load(obj: {str: Image}):
    global project_images
    project_images = obj


def on_price_images_load(obj: ({NormalPriceTypes: Image}, Image)):
    global price_images
    price_images = obj


def init():
    # Registers the load-signals
    EventDispatcher.start_lurking(Signals.SIGNAL_PROJECTS_CHANGE, on_projects_load)
    EventDispatcher.start_lurking(Signals.SIGNAL_IMAGES_CHANGE, on_project_images_load)
    EventDispatcher.start_lurking(Signals.SIGNAL_PRICE_IMAGES_CHANGE, on_price_images_load)
    EventDispatcher.start_lurking(Signals.SIGNAL_PRESENTATION_CHANGE, on_presentation_load)
