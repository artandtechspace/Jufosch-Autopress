from pptx.presentation import Presentation

from src.core.presentation.data.PreLayout import PreLayout
from src.data.Fields import Fields


class LoadedPresentation:

    def __init__(self, root: Presentation, field_layouts: {Fields: PreLayout}, lookup_layout: PreLayout):
        self.root = root
        self.field_layouts = field_layouts
        self.lookup_layout = lookup_layout
