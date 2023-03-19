from typing import Callable

from gi.repository import Gtk

from src.ui import UserRessources


@Gtk.Template.from_file("rsc/glade/ExportView.glade")
class UiExportMenu(Gtk.Popover):
    __gtype_name__ = "baseExportMenu"

    # Export button and error icon
    btn_export: Gtk.Button = Gtk.Template.Child("btn_export")
    icn_export: Gtk.Image = Gtk.Template.Child("icon_export")

    # Dropdown for the modus-selection
    modus_select: Gtk.ComboBox = Gtk.Template.Child("modus_select")

    # Simple bool-settings error-icons and checkbox-buttons
    icn_err_price: Gtk.Image = Gtk.Template.Child("icon_error_price_slides")
    icn_err_wimgs: Gtk.Image = Gtk.Template.Child("icon_error_with_images")
    cb_price: Gtk.CheckButton = Gtk.Template.Child("btn_price_slides")
    cb_wimgs: Gtk.CheckButton = Gtk.Template.Child("btn_with_images")

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

            # Resets the active condition if the settings is not applyable
            if not res:
                btn.set_active(False)

    # Updates the uis export button
    def __update_ui_export_button(self):
        # Checks if the export button is enabled
        is_enabled = UserRessources.projects is not None and UserRessources.presentation is not None

        # Updates the button and icon
        self.btn_export.set_sensitive(is_enabled)
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

    @Gtk.Template.Callback("on_export_clicked")
    def on_click_export(self, _: Gtk.Button):
        print("Clicked export")

    def __init__(self):
        super().__init__()

        # Sets the default modus
        self.modus_select.set_active(0)
