from gi.repository import Gtk

from src.data.Project import Project
from src.ui import Signals, UserRessources
from src.utils import EventDispatcher


@Gtk.Template.from_file("rsc/glade/Statistics.glade")
class Statistics(Gtk.Box):
    __gtype_name__ = "baseStatistics"

    fld_amt_projects: Gtk.Label = Gtk.Template.Child("amt_projects")
    fld_amt_projects_with_imgs: Gtk.Label = Gtk.Template.Child("amt_projects_wimg")
    fld_amt_projects_without_imgs: Gtk.Label = Gtk.Template.Child("amt_projects_nimg")
    fld_amt_images: Gtk.Label = Gtk.Template.Child("amt_images")

    def __set_loaded_project(self, amt: str | None):
        self.fld_amt_projects.set_text("" if amt is None else amt)

    def __set_loaded_images(self, proj_with: str | None, proj_without: str | None, total: str | None):
        self.fld_amt_projects_with_imgs.set_text("" if proj_with is None else proj_with)
        self.fld_amt_projects_without_imgs.set_text("" if proj_without is None else proj_without)

        self.fld_amt_images.set_text("" if total is None else total)

    def __update_internal_ui(self, _):
        # Checks if projects are loaded
        if UserRessources.projects is None:
            self.__set_loaded_project(None)
        else:
            # Updates the projects
            self.__set_loaded_project(str(len(UserRessources.projects)))

        # Checks if images are loaded
        if UserRessources.project_images is None:
            self.__set_loaded_images(None, None, None)

        if UserRessources.project_images is not None and UserRessources.projects is not None:
            # Calculates the amount of projects with and without an image
            amt_with = len(list(filter(lambda proj: proj.get_raw_stand_number() in UserRessources.project_images,
                                       UserRessources.projects)))

            amt_without = len(list(filter(lambda proj: proj.get_raw_stand_number() not in UserRessources.project_images,
                                          UserRessources.projects)))

            self.__set_loaded_images(str(amt_with), str(amt_without), str(len(UserRessources.project_images)))

    def __init__(self):
        super().__init__()

        # Registers the event listeners
        EventDispatcher.start_lurking(Signals.SIGNAL_PROJECTS_CHANGE, self.__update_internal_ui)
        EventDispatcher.start_lurking(Signals.SIGNAL_IMAGES_CHANGE, self.__update_internal_ui)

        self.__update_internal_ui(None)
