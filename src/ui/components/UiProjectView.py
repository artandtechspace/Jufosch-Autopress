
from PIL import Image
from gi.overrides.GLib import GLib
from gi.overrides.GdkPixbuf import GdkPixbuf
from gi.repository import Gtk

from src.data.Fields import Fields
from src.data.Price import PRICES
from src.data.Project import Project
from src.data.ProjectMember import ProjectMember
from src.data.Type import Type
from src.ui import Signals, CachedRessource, UserRessources
from src.utils import EventDispatcher

# Dummy project
DUMMY_PROJECT = Project("", "", Type.JUFO, Fields.MATH_AND_INFO, 0, [])


@Gtk.Template.from_file("rsc/glade/ProjectView.glade")
class ProjectView(Gtk.Stack):
    __gtype_name__ = "baseProjectView"

    fld_icon: Gtk.Image = Gtk.Template.Child("fld_icon")

    fld_location: Gtk.Label = Gtk.Template.Child("fld_location")
    fld_stand: Gtk.Label = Gtk.Template.Child("fld_stand")
    fld_title: Gtk.Label = Gtk.Template.Child("fld_title")
    fld_field: Gtk.Label = Gtk.Template.Child("fld_field")

    fld_m1: Gtk.Label = Gtk.Template.Child("fld_m1")
    fld_m2: Gtk.Label = Gtk.Template.Child("fld_m2")
    fld_m3: Gtk.Label = Gtk.Template.Child("fld_m3")

    fld_price: Gtk.ComboBox = Gtk.Template.Child("fld_price")
    area_special_price: Gtk.Box = Gtk.Template.Child("area_specialPrice")
    fld_special_price: Gtk.Entry = Gtk.Template.Child("fld_specialPrice")

    store_prices: Gtk.ListStore = Gtk.Template.Child("priceStore")
    store_specialPriceSuggestions: Gtk.ListStore = Gtk.Template.Child("specialPriceStore")

    img_project: Gtk.Image = Gtk.Template.Child("img_project")

    # Ref to the currently selected project
    current_project: Project = None

    @Gtk.Template.Callback("on_specialprice_name_changed")
    def on_specialprice_name_changed(self, elm: Gtk.Entry):
        self.current_project.special_price_name = elm.get_text()

    @Gtk.Template.Callback("on_price_changed")
    def on_price_changed(self, elm: Gtk.ComboBox):
        if self.current_project is None:
            return

        # Gets the project
        price = PRICES[elm.get_active()]

        self.current_project.price = price

        self.__update_internal_ui()
        # Dispatches the event
        EventDispatcher.shout(Signals.SIGNAL_UI_PROJECT_CHANGED)

    # Event: Must be called from outside to setup required functions
    def on_post_creation(self):

        # Injects all price possibilities
        for price in PRICES:
            self.store_prices.append([price.get_name(" + ")])

        # Attaches all name suggestions
        with open(CachedRessource.SPECIAL_PRICE_NAME_SUGGESTIONS) as f:
            for line in f:
                self.store_specialPriceSuggestions.append(["@" + line.strip()])

        # Registers the project-selectors
        EventDispatcher.start_lurking(Signals.SIGNAL_UI_PROJECT_SELECT, self.set_project)
        EventDispatcher.start_lurking(Signals.SIGNAL_UI_PROJECT_UNSELECT, self.set_project)

    def __update_internal_ui(self):
        # Updates the special price section
        if self.current_project is not None:
            self.area_special_price.set_visible(self.current_project.price.has_special_price)

    def set_project(self, proj: Project | None):
        self.current_project = proj

        # Switches to the visible window
        self.set_visible_child(self.get_children()[1 if proj != None else 0])

        # Sets a dummy-project to prevent memory with possible critical data
        if proj is None:
            proj = DUMMY_PROJECT

        # Updates all fields
        self.fld_location.set_text(proj.location)
        self.fld_stand.set_text(proj.get_raw_stand_number())
        self.fld_title.set_text(proj.name)
        self.fld_field.set_text(proj.field.value[0])

        def set_member(i: int, label: Gtk.Label):
            if len(proj.members) > i:
                member: ProjectMember = proj.members[i]
                label.set_text(member.get_short_description())
            else:
                label.set_text("")

        # Sets the project members
        set_member(0, self.fld_m1)
        set_member(1, self.fld_m2)
        set_member(2, self.fld_m3)

        # Updates the icon
        self.fld_icon.set_from_pixbuf(
            CachedRessource.JUFO_LOGO if proj.type == Type.JUFO else CachedRessource.SUEX_LOGO)

        # Updates the price-combobox
        self.fld_price.set_active(PRICES.index(proj.price))

        # Setups the special price field
        self.fld_special_price.set_text(proj.special_price_name)

        # Updates the project-image
        if UserRessources.project_images is not None and proj.get_raw_stand_number() in UserRessources.project_images:
            self.img_project.set_visible(True)

            # Gets the image
            img = UserRessources.project_images[proj.get_raw_stand_number()]

            img = img.resize((400, int(img.height * 400/img.width)))

            buffer = GLib.Bytes.new(img.tobytes())
            gdata = GdkPixbuf.Pixbuf.new_from_bytes(buffer, GdkPixbuf.Colorspace.RGB, True, 8, img.width,
                                                    img.height, len(img.getbands()) * img.width)

            self.img_project.set_from_pixbuf(gdata)
        else:
            self.img_project.set_visible(False)

        # Performs other internal ui updates
        self.__update_internal_ui()
