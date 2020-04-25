import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("ui/mockup.glade")

window = builder.get_object("mockup")
window.show_all()

Gtk.main()