from gi.overrides.Gio import Gio
from gi.repository import Gtk

from src.core import CSVProjectLoader, ImageLoader
from src.core.presentation import PresentationLoader
from src.ui import CachedRessource, Signals
from src.ui.CachedRessource import RSC_PATH
from src.utils import EventDispatcher
import gio
import os

# Default file/folder-names
DF_NAME_PRESENTATION = "Präsentation.pptx"
DF_NAME_PROJECT_IMAGES = "Projektbilder"
DF_NAME_PRICE_IMAGES = "Preise"
DF_NAME_PROJEKTE = "Projekte.csv"

@Gtk.Template.from_file(RSC_PATH+"/glade/LoadMenu.glade")
class UiLoadMenu(Gtk.Popover):
    __gtype_name__ = "baseLoadMenu"

    # Image references
    img_impress: Gtk.Image = Gtk.Template.Child("img_impress")
    img_calc: Gtk.Image = Gtk.Template.Child("img_calc")
    img_images: Gtk.Image = Gtk.Template.Child("img_images")
    img_prices: Gtk.Image = Gtk.Template.Child("img_prices")
    img_multi: Gtk.Image = Gtk.Template.Child("img_multi")

    # Button references
    btn_prices: Gtk.FileChooserButton = Gtk.Template.Child("btnPrices")
    btn_pj_images: Gtk.FileChooserButton = Gtk.Template.Child("btnProjectImages")
    btn_presentation: Gtk.FileChooserButton = Gtk.Template.Child("btnPresentation")
    btn_projects: Gtk.FileChooserButton = Gtk.Template.Child("btnProjects")

    @Gtk.Template.Callback("on_select_all")
    def on_select_all(self, btn: Gtk.FileChooserButton):
        # Gets the path
        path = btn.get_file().get_path()

        # Directly unselects the folder
        btn.unselect_all()

        # References for all element that are required together to open the required elements
        refs = [
            (DF_NAME_PRESENTATION, self.btn_presentation, self.on_presentation_open, os.path.isfile),
            (DF_NAME_PROJEKTE, self.btn_projects, self.on_projects_open, os.path.isfile),
            (DF_NAME_PRICE_IMAGES, self.btn_prices, self.on_price_images_open, os.path.isdir),
            (DF_NAME_PROJECT_IMAGES, self.btn_pj_images, self.on_images_open, os.path.isdir),
        ]

        # Flag to indicate if at least one element was tries to be loaded
        found_smth = False

        # Tries to load all elements
        for filename, button, eventHandler, filefilter in refs:
            # Gets the combined path
            full_path = os.path.join(path, filename)
            # Tries to load the elements
            if os.path.exists(full_path) and filefilter(full_path):
                found_smth = True
                button.select_filename(full_path)
                eventHandler(button)

        # Checks if no elements where found
        if not found_smth:
            EventDispatcher.shout(Signals.SIGNAL_SHOW_SIMPLE_DIALOG, ("Nichts wurde geladen", "Im ausgewählten Ordner wurde kein Element mit dem korrekten Namen gefunden.", Gtk.MessageType.ERROR))

    @Gtk.Template.Callback("on_presentation_open")
    def on_presentation_open(self, btn: Gtk.FileChooserButton):

        # TODO: Load presentation
        # Gets the path
        path = btn.get_file().get_path()
        try:
            # Tries to load the presentation
            loadedPres = PresentationLoader.load_presentation(path)

            # Forwards the event with the presentation as the argument
            EventDispatcher.shout(Signals.SIGNAL_PRESENTATION_CHANGE, loadedPres)
        except ValueError as err:
            # Removes the file
            btn.unselect_all()
            # Unselects any previous projects
            EventDispatcher.shout(Signals.SIGNAL_PRESENTATION_CHANGE)
            # Opens the error dialog
            # TODO: Translate error code and embed external data
            EventDispatcher.shout(Signals.SIGNAL_SHOW_SIMPLE_DIALOG,
                                  ("Fehler beim laden der Präsentation", err.args[0], Gtk.MessageType.ERROR))
        # Forwards the event with a string (path) as the argument
        #EventDispatcher.shout(Signals.SIGNAL_LOAD_PRESENTATION, )

    @Gtk.Template.Callback("on_projects_open")
    def on_projects_open(self, btn: Gtk.FileChooserButton):
        try:
            # Tries to laod the projects
            projects = CSVProjectLoader.load_projects_from_file(btn.get_file().get_path())

            # Forwards the event with all projects as the argument
            EventDispatcher.shout(Signals.SIGNAL_PROJECTS_CHANGE, projects)

        except ValueError as e:
            # Removes the file
            btn.unselect_all()
            # Unselects any previous projects
            EventDispatcher.shout(Signals.SIGNAL_PROJECTS_CHANGE)
            # Opens the error dialog
            # TODO: Translate error code and embed external data
            EventDispatcher.shout(Signals.SIGNAL_SHOW_SIMPLE_DIALOG, ("Fehler beim laden der Projekte", e.args[0], Gtk.MessageType.ERROR))
        except FileNotFoundError as e:
            # Removes the file
            btn.unselect_all()
            # Unselects any previous projects
            EventDispatcher.shout(Signals.SIGNAL_PROJECTS_CHANGE)
            # Opens the error dialog
            EventDispatcher.shout(Signals.SIGNAL_SHOW_SIMPLE_DIALOG, ("Fehler beim laden der Projekte", "Datei existiert nicht...", Gtk.MessageType.ERROR))


    @Gtk.Template.Callback("on_images_open")
    def on_images_open(self, btn: Gtk.FileChooserButton):
        # Gets the path
        path = btn.get_file().get_path()

        # Tries to load the images
        inv_imgs, inv_names, dup_names, imgs = ImageLoader.load_project_images_from_folder(path)


        # Message-appender
        messages = []

        # TODO: Language lookup

        # Checks if some names were invalid
        if len(inv_names) > 0:
            if len(inv_names) < 5:
                messages.append("Folgende "+str(len(inv_names))+" Bilder haben einen falschen Namen:\n('"+"', '".join(inv_names)+"')")
            else:
                messages.append(str(len(inv_names))+" Bilder haben einen falschen Namen")

        # Checks if some images were duplicated
        if len(dup_names) > 0:
            if len(dup_names) < 5:
                messages.append("Folgende "+str(len(dup_names))+" Projekte haben mehrere Bilder:\n('"+"', '".join(dup_names)+"')")
            else:
                messages.append(str(len(dup_names))+" Projekte haben mehrere Bilder.")

        # Checks if some images were duplicated
        if len(inv_imgs) > 0:
            if len(inv_imgs) < 5:
                messages.append(
                    "Folgende " + str(len(inv_imgs)) + " Bilder konnten nicht geladen werden:\n('" + "', '".join(inv_imgs)+"')")
            else:
                messages.append(str(len(inv_imgs)) + " Bilder konnten nicht geladen werden.")

        # Checks if no other error occurred and no images were loaded
        if len(messages) <= 0 and len(imgs) <= 0:
            messages.append("Es wurden keine Bilder mit JUFO-Standnamen gefunden.")

        # Checks if an error occurred
        if len(messages) > 0:
            # Resets the field
            btn.unselect_all()

            # Sends the error message
            EventDispatcher.shout(Signals.SIGNAL_SHOW_SIMPLE_DIALOG, ("Fehler beim laden der Bilder", "\n\n".join(messages), Gtk.MessageType.ERROR))

            # Dispatches the image-unload event
            EventDispatcher.shout(Signals.SIGNAL_IMAGES_CHANGE)
        else:
            # Dispatches the image-load event
            EventDispatcher.shout(Signals.SIGNAL_IMAGES_CHANGE, imgs)

    @Gtk.Template.Callback("on_prices_open")
    def on_price_images_open(self, btn: Gtk.FileChooserButton):
        # Gets the path
        path = btn.get_file().get_path()

        try:
            # Loads the images
            load = ImageLoader.load_price_images(path)

            # Dispatches the prices-load event
            EventDispatcher.shout(Signals.SIGNAL_PRICE_IMAGES_CHANGE, load)
        except ValueError as err:
            # Removes the folder
            btn.unselect_all()

            # Dispatches the prices-unload event
            EventDispatcher.shout(Signals.SIGNAL_PRICE_IMAGES_CHANGE)

            # Shows how many images were loaded
            EventDispatcher.shout(Signals.SIGNAL_SHOW_SIMPLE_DIALOG, ("Fehler beim laden der Preisbilder", err.args[0], Gtk.MessageType.ERROR))

    def __init__(self):
        super().__init__()

        # Updates the icons
        self.img_calc.set_from_pixbuf(CachedRessource.ICON_LO_CALC)
        self.img_impress.set_from_pixbuf(CachedRessource.ICON_LO_IMPRESS)
        self.img_images.set_from_pixbuf(CachedRessource.ICON_IMAGES_FOLDER)
        self.img_prices.set_from_pixbuf(CachedRessource.ICON_MEDAL)
        self.img_multi.set_from_pixbuf(CachedRessource.ICON_OPEN_ALL)
