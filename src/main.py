import gi

from src.ui import UserRessources

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from src.ui.windows import MainWindow

# Initalizes the user-ressources
UserRessources.init()

# Opens the main application
MainWindow.open()
Gtk.main()
