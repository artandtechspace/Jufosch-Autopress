from gi.repository import Gtk

from src.data.Project import Project
from src.ui import Signals, UserRessources
from src.ui.CachedRessource import RSC_PATH
from src.utils import EventDispatcher

LINE_PROJECTS = 0
LINE_PROJECTS_WITH_IMAGES = 1
LINE_PROJECTS_WITHOUT_IMAGES = 2
LINE_IMAGES = 3

@Gtk.Template.from_file(RSC_PATH+"/glade/Statistics.glade")
class Statistics(Gtk.Popover):
    __gtype_name__ = "baseStatistics"

    fld_amt_projects: Gtk.Label = Gtk.Template.Child("amt_projects")
    fld_amt_projects_with_imgs: Gtk.Label = Gtk.Template.Child("amt_projects_wimg")
    fld_amt_projects_without_imgs: Gtk.Label = Gtk.Template.Child("amt_projects_nimg")
    fld_amt_images: Gtk.Label = Gtk.Template.Child("amt_images")

    lbl_projects: Gtk.Label = Gtk.Template.Child("lbl_projects")
    lbl_projects_with_imgs: Gtk.Label = Gtk.Template.Child("lbl_projects_wimg")
    lbl_projects_without_imgs: Gtk.Label = Gtk.Template.Child("lbl_projects_nimg")
    lbl_images: Gtk.Label = Gtk.Template.Child("lbl_images")

    # Updates the line with the given index on the ui
    def __update_line(self, line_idx: int, value: int|None = None):
        fld: Gtk.Label = self.lines[line_idx][0]
        lbl: Gtk.Label = self.lines[line_idx][1]

        # Updates their visibility
        fld.set_visible(value is not None)
        lbl.set_visible(value is not None)

        if value is not None:
            fld.set_text(str(value))

    # Updates the ui according to the current state
    def __update_internal_ui(self, _=None):

        # Updates projects
        self.__update_line(LINE_PROJECTS, None if UserRessources.projects is None else len(UserRessources.projects))

        # Updates images
        self.__update_line(LINE_IMAGES, None if UserRessources.project_images is None else len(UserRessources.project_images))

        # Updates sub-images
        if UserRessources.project_images is None or UserRessources.projects is None:
            self.__update_line(LINE_PROJECTS_WITH_IMAGES, None)
            self.__update_line(LINE_PROJECTS_WITHOUT_IMAGES, None)
        else:
            # Calculates the amount of projects with and without an image
            amt_with = len(list(filter(lambda proj: proj.get_raw_stand_number() in UserRessources.project_images,
                                       UserRessources.projects)))

            amt_without = len(list(filter(lambda proj: proj.get_raw_stand_number() not in UserRessources.project_images,
                                          UserRessources.projects)))

            self.__update_line(LINE_PROJECTS_WITH_IMAGES, amt_with)
            self.__update_line(LINE_PROJECTS_WITHOUT_IMAGES, amt_without)

    # Initializes the line-assignments to program-labels
    def __init_lines(self):
        # Generates the lines
        self.lines = {
            LINE_PROJECTS: [self.fld_amt_projects, self.lbl_projects],
            LINE_PROJECTS_WITH_IMAGES: [self.fld_amt_projects_with_imgs, self.lbl_projects_with_imgs],
            LINE_PROJECTS_WITHOUT_IMAGES: [self.fld_amt_projects_without_imgs, self.lbl_projects_without_imgs],
            LINE_IMAGES: [self.fld_amt_images, self.lbl_images]
        }

    def __init__(self):
        super().__init__()

        # Initializes the lines
        self.__init_lines()

        # Registers the event listeners
        EventDispatcher.start_lurking(Signals.SIGNAL_PROJECTS_CHANGE, self.__update_internal_ui)
        EventDispatcher.start_lurking(Signals.SIGNAL_IMAGES_CHANGE, self.__update_internal_ui)

        # Performs the first ui update
        self.__update_internal_ui()
