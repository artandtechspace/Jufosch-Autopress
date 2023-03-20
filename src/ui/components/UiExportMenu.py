from typing import Callable

from gi.repository import Gtk

from src.core import ExportManager
from src.ui import UserRessources, Signals
from src.utils import EventDispatcher


@Gtk.Template.from_file("rsc/glade/ExportView.glade")
class UiExportMenu(Gtk.Popover):
    __gtype_name__ = "baseExportMenu"

    # Path-chooser elements
    path_chooser_txt: Gtk.Entry = Gtk.Template.Child("path_chooser")

    # Export button and error icon
    btn_export: Gtk.Button = Gtk.Template.Child("btn_export")
    icn_export: Gtk.Image = Gtk.Template.Child("icon_export")

    # Simple bool-settings error-icons and checkbox-buttons
    icn_err_price: Gtk.Image = Gtk.Template.Child("icon_error_price_slides")
    icn_err_wimgs: Gtk.Image = Gtk.Template.Child("icon_error_with_images")
    cb_price: Gtk.CheckButton = Gtk.Template.Child("btn_price_slides")
    cb_wimgs: Gtk.CheckButton = Gtk.Template.Child("btn_with_images")
    cb_with_project_slides: Gtk.CheckButton = Gtk.Template.Child("btn_project_slides")
    cb_gen_lookup: Gtk.CheckButton = Gtk.Template.Child("btn_gen_lookup")
    cb_gen_normal: Gtk.CheckButton = Gtk.Template.Child("btn_gen_normal")

    # Updates the simple yes/no us settings
    def __update_ui_boolsettings(self):
        # Simple settings that are enabled based on simple tests
        # They have the following format:
        # Icon-Image with a tooltip what is wrong (If there is something wrong)
        # Check-button that enables/disables the setting
        # Function that tests if the condition for enabling is active
        # Error-tooltip
        # TODO: Language
        settings: [(Gtk.Image, Gtk.CheckButton, Callable[[], bool])] = [
            (
                self.icn_err_price,
                self.cb_price,
                lambda: UserRessources.price_images is not None
            ), (
                self.icn_err_wimgs,
                self.cb_wimgs,
                lambda: UserRessources.project_images is not None
            )
        ]

        # Iterates over every setting to update it
        for setting in settings:
            # Gets the elements
            icon: Gtk.Image
            btn: Gtk.CheckButton
            testcondition: Callable[[], bool]
            icon, btn, testcondition = setting

            # Checks the condition
            res = testcondition()

            # Some bool logic
            btn.set_sensitive(res)
            icon.set_visible(not res)

            # Resets the active condition if the settings is not applicable
            if not res:
                btn.set_active(False)

    # Updates the uis export button
    def __update_ui_export_button(self):
        # Checks if the export button is enabled
        is_enabled = UserRessources.projects is not None and UserRessources.presentation is not None

        # Checks if a path is choosen
        path_is_choosen = len(self.path_chooser_txt.get_text().strip()) > 0

        # Updates the button and icon
        self.btn_export.set_sensitive(is_enabled and path_is_choosen)
        self.icn_export.set_visible(not is_enabled)

    # Used to refresh
    def __update_ui(self):
        # Updates the simple bool settings
        self.__update_ui_boolsettings()

        # Updates the export button
        self.__update_ui_export_button()
        pass

    # (External) Event: Whenever the menu toggles (opens/closes)
    def on_menu_toggle(self, _: Gtk.MenuButton):
        self.__update_ui()

    @Gtk.Template.Callback("on_path_input")
    def on_path_input(self, _: Gtk.Entry):
        # Sends a ui-update
        self.__update_ui_export_button()
        pass

    @Gtk.Template.Callback("on_path_btn_clicked")
    def on_path_btn_clicked(self, _: Gtk.Button):
        def on_result(path: str):
            if path is None:
                return

            # Updates the path-input
            self.path_chooser_txt.set_text(path)
            self.__update_ui_export_button()

        # TODO: Language
        # Creates the filters
        filter_pres = Gtk.FileFilter()
        filter_pres.set_name("Präsentation (.pptx)")
        filter_pres.add_mime_type("application/vnd.openxmlformats-officedocument.presentationml.presentation")

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")

        # Sends the chooser-open signal
        EventDispatcher.shout(Signals.SIGNAL_SHOW_FILE_CHOOSER, (
            "Save file as",
            Gtk.FileChooserAction.SAVE,
            [
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE,
                Gtk.ResponseType.OK,
             ],
            [
                filter_pres,
                filter_any
            ],
            on_result
        ))

    @Gtk.Template.Callback("on_export_clicked")
    def on_click_export(self, _: Gtk.Button):
        # Gets the settings
        path = self.path_chooser_txt.get_text()

        export_normal_slides = self.cb_gen_normal.get_active()
        export_lookup_slides = self.cb_gen_lookup.get_active()

        with_project_slides = self.cb_with_project_slides.get_active()

        with_project_images = self.cb_wimgs.get_active()
        with_prices = self.cb_price.get_active()

        # Tries to export the presentation
        try:
            ExportManager.export_presentation(
                presentation=UserRessources.presentation,
                projects=UserRessources.projects,
                export_path=path,

                with_normal_slides=export_normal_slides,
                with_lookup_slides=export_lookup_slides,
                generate_project_slides=with_project_slides,

                project_images=UserRessources.project_images if with_project_images else None,
                price_images=UserRessources.price_images if with_prices else None
            )

            # Shows the successful export
            EventDispatcher.shout(Signals.SIGNAL_SHOW_SIMPLE_DIALOG, ("Exportiert", "Präsentation wurde erfolgreich exportiert", Gtk.MessageType.INFO))
        except ValueError as err:
            # TODO: Language
            # Opens the error dialog
            EventDispatcher.shout(Signals.SIGNAL_SHOW_SIMPLE_DIALOG,
                                  ("Fehler beim exportieren der Präsentation", err.args[0], Gtk.MessageType.ERROR))

    def __init__(self):
        super().__init__()
