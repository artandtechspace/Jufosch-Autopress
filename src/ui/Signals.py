# Whenever the user selects/unselects a project inside the list-view
# Params: Project (that got selected)
SIGNAL_UI_PROJECT_SELECT = "ui_proj_select"
# Params: None (The selected project can be accessed through other ways)
SIGNAL_UI_PROJECT_UNSELECT = "ui_proj_unselect"

# Whenever a specific project get's edited (Eg. price gets changed)
# Params: None (The selected project can be accessed through other ways)
SIGNAL_UI_PROJECT_CHANGED = "ui_proj_changed"

# Whenever the selected presentation changes
# Params: None (If the presentation got unloaded) or LoadedPresentation
SIGNAL_PRESENTATION_CHANGE = "pres_change"

# Whenever new projects get loaded or get unloaded
# Params: None (If projects got unloaded) or list[Project]
SIGNAL_PROJECTS_CHANGE = "proj_change"

# Whenever new project-images get loaded or removed
# Params: None (If unloaded) or {str: Image} where str is the
# Project-ID eg. JA001 for the first jufo-project of the field arbeitswelt
SIGNAL_IMAGES_CHANGE = "proj_img_change"

# Whenever new price-images get loaded or removed
# Params: None (If unloaded) or ({NormalPriceImages: Image}, Image) where the first object are for the normal
# prices and the second is for the special image
SIGNAL_PRICE_IMAGES_CHANGE = "price_img_change"

# Whenever a dialog should be shown
# Params: (title, error, Gtk.MessageType)
SIGNAL_SHOW_SIMPLE_DIALOG = "show_dialog"

# Whenever a file chooser dialog should be shown
# Params: (title, Gtk.FileChooserAction, buttons: [str], filters: [Gtk.FileFilter], Callable[[result],None])
SIGNAL_SHOW_FILE_CHOOSER = "show_saver"
