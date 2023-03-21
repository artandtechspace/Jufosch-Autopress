from typing import Callable

from gi.repository import Gtk

from src.data.Project import Project
from src.ui import Signals
from src.ui.CachedRessource import RSC_PATH
from src.ui.components.UiExportMenu import UiExportMenu
from src.ui.components.UiLoadMenu import UiLoadMenu
from src.ui.components.UiProjectList import ProjectList
from src.ui.components.UiProjectView import ProjectView
from src.ui.components.UiStatistics import Statistics
from src.utils import EventDispatcher

window: Gtk.Window
project_list: ProjectList
project_view: ProjectView
export_popup: UiExportMenu

# Creates the project list
def __create_project_list(builder: Gtk.Builder):
    # Gets the list-wrapper
    project_list_wrapper: Gtk.ScrolledWindow = builder.get_object("project_list_wrapper")

    # Create the project-list
    pl = ProjectList()
    project_list_wrapper.add(pl)

    # Initalizes it with the project-store
    pl.initalize(builder.get_object("store"))

    # TODO: Remove / Debug

    # projects = load_projects_from_file("../local/in.csv")
    # pl.load_projects(projects)
    return pl

# Creates the statistics-preview
def __create_statistics_view(builder: Gtk.Builder):
    # Gets the project view-split
    project_preview_wrapper: Gtk.Paned = builder.get_object("view_split")

    # Appends it
    project_preview_wrapper.add(Statistics())

# Create the project-preview
def __create_project_preview(builder: Gtk.Builder):
    # Gets the project view-split
    project_preview_wrapper: Gtk.Paned = builder.get_object("view_split")

    # Creates the project-view
    proj_view = ProjectView()
    proj_view.on_post_creation()

    # Appends it
    project_preview_wrapper.add(proj_view)

    return proj_view

# Setups the headers
def __initalize_header(builder: Gtk.Builder):
    # Gets the buttons
    btn_import: Gtk.MenuButton = builder.get_object("btn_import")
    btn_export: Gtk.MenuButton = builder.get_object("btn_export")

    # Creates menus
    export_menu = UiExportMenu()

    # Connects toggle event to export button
    btn_export.connect("toggled", export_menu.on_menu_toggle)

    # Sets the popover for the button
    btn_import.set_popover(UiLoadMenu())
    btn_export.set_popover(export_menu)

    return

# Event: Whenever a simple file-chooser should be displayed
def __on_retrieve_file_chooser_dialog(params: (str, Gtk.FileChooserAction, [str], [Gtk.FileFilter], Callable[[str],None])):
    global window

    title, action, buttons, filters, callback = params

    dialog = Gtk.FileChooserDialog(
        title=title,
        parent=window,
        action=action
    )

    # Appends the filters
    for filt in filters:
        dialog.add_filter(filt)

    # Appends the buttons
    dialog.add_buttons(
        *buttons
    )

    # Lets the file-chooser do it's thing
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        callback(dialog.get_file().get_path())
    elif response == Gtk.ResponseType.CANCEL:
        callback(None)

    dialog.destroy()
    pass

# Event: Whenever an simple dialog should be displayed
def __on_retrieve_show_dialog(params):
    global window

    dialog = Gtk.MessageDialog(
        transient_for=window,
        flags=0,
        message_type=params[2],
        buttons=Gtk.ButtonsType.CLOSE,
        text=params[0],
    )
    dialog.format_secondary_text(params[1])
    dialog.run()
    dialog.destroy()


# Event: Whenever the new projects get loaded or unloaded
def __on_projects_change(projects: None | list[Project]):
    # Updates the project list
    if projects is None:
        project_list.unload_projects()
    else:
        project_list.load_projects(projects)
    pass


# Opens the main window
def open():
    global window, project_list, project_view

    # Interprets the file
    builder = Gtk.Builder()
    builder.add_from_file(RSC_PATH+"/glade/UIBinding.glade")

    # Connect the handlers
    #builder.connect_signals({
    #})

    # Creates the project-view and project-list
    project_view = __create_project_preview(builder)
    project_list = __create_project_list(builder)
    __create_statistics_view(builder)
    __initalize_header(builder)

    # Creates the window and opens it
    window = builder.get_object("window")
    window.connect("destroy", Gtk.main_quit)
    window.show_all()

    # Registers different events
    EventDispatcher.start_lurking(Signals.SIGNAL_SHOW_SIMPLE_DIALOG, __on_retrieve_show_dialog)
    EventDispatcher.start_lurking(Signals.SIGNAL_PROJECTS_CHANGE, __on_projects_change)
    EventDispatcher.start_lurking(Signals.SIGNAL_SHOW_FILE_CHOOSER, __on_retrieve_file_chooser_dialog)
