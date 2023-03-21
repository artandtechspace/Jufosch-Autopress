from gi.repository import Gtk
from gi.repository.Gtk import SortType

from src.data.Price import DEFAULT_PRICE
from src.data.Project import Project
from src.data.Type import Type
from src.ui import Signals
from src.ui.CachedRessource import JUFO_LOGO_SMALL, SUEX_LOGO_SMALL, RSC_PATH
from src.utils import EventDispatcher


@Gtk.Template.from_file(RSC_PATH+"/glade/ProjectList.glade")
class ProjectList(Gtk.TreeView):
    __gtype_name__ = "baseProjectList"

    # List with loaded projects
    loaded_projects: list[Project] | None

    @Gtk.Template.Callback("on_select_row")
    def on_select_row(self, row: Gtk.TreeSelection):
        # Ensures one row is selected
        if row.count_selected_rows() != 1:
            return

        # Gets the raw row
        row_raw: Gtk.TreeModelRow = row.get_selected_rows()[0][row.get_selected_rows()[1][0]]

        # Gets the project-id (Stand number)
        proj_number = row_raw[4]

        # Gets the corresponding project
        proj = next(x for x in self.loaded_projects if x.get_raw_stand_number() == proj_number)

        # Dispatches the event
        EventDispatcher.shout(Signals.SIGNAL_UI_PROJECT_SELECT, proj)

    @Gtk.Template.Callback("on_sort_clicked")
    def on_column_clicked(self, column: Gtk.TreeViewColumn):

        # Gets the index/id of the column
        idx = column.get_sort_column_id()

        # Gets the current sort order
        sort_order: Gtk.SortType = column.get_sort_order()

        # Revokes all sort icons
        self.__revoke_sort_from_columns()

        # Reverses sort order, resorts and updates the icon
        column.set_sort_order(SortType.ASCENDING if sort_order != SortType.DESCENDING else SortType.DESCENDING)
        column.set_sort_indicator(True)
        self.get_model().set_sort_column_id(idx, sort_order != SortType.ASCENDING)

    # Event: Fires whenever a project got changed
    def on_project_changed(self, none):
        # Gets the raw row
        row_raw: Gtk.TreeModelRow = self.get_selection().get_selected_rows()[0][
            self.get_selection().get_selected_rows()[1][0]]

        # Gets the project-id (Stand number)
        proj_number = row_raw[4]

        # Gets the corresponding project
        proj = next(x for x in self.loaded_projects if x.get_raw_stand_number() == proj_number)

        # Updates the price-field
        row_raw[5] = proj.price != DEFAULT_PRICE

    def __revoke_sort_from_columns(self):
        for c in self.get_columns():
            c.set_sort_indicator(False)
            c.set_sort_order(SortType.DESCENDING)

    def initalize(self, store: Gtk.ListStore):
        self.set_model(store)
        # Resets all columns
        self.__revoke_sort_from_columns()

        # Registers the project-changed listener
        EventDispatcher.start_lurking(Signals.SIGNAL_UI_PROJECT_CHANGED, self.on_project_changed)

    def unload_projects(self):
        store: Gtk.ListStore = self.get_model()

        # Removes any previous projects
        store.clear()

        self.loaded_projects = None

        # Dispatches the event
        EventDispatcher.shout(Signals.SIGNAL_UI_PROJECT_UNSELECT)
        pass

    def load_projects(self, projects: list[Project]):

        # Unloads any previously loaded projects
        self.unload_projects()

        store: Gtk.ListStore = self.get_model()

        # Updates the loaded projects
        self.loaded_projects = projects

        # Adds all projects to the list
        for p in projects:
            store.append([
                JUFO_LOGO_SMALL if p.type == Type.JUFO else SUEX_LOGO_SMALL,
                p.name,
                p.location,
                p.field.value[0],
                p.get_raw_stand_number(),
                p.price != DEFAULT_PRICE
            ])
