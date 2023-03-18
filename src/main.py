import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from src.ui.windows import MainWindow

MainWindow.open()
Gtk.main()
