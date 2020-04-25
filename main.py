import gi, os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("ui/main.glade")

liststore = builder.get_object("liststore")

def additem(button):
    path = builder.get_object("entry_path").get_text()
    size = os.path.getsize(path)
    liststore.append([path, round(size / 1024 / 1024, 2)])

def on_selection_changed(selection):
    (model, iter) = selection.get_selected()

    if iter is not None:
        print("Path: " + (model[iter][0]) + " Size: " + str((model[iter][1])))
    else:
        print("")
    return True

handlers = {
    "on_button_add_clicked": additem,
    "on_selection_changed": on_selection_changed
}
builder.connect_signals(handlers)

window = builder.get_object("main")
window.connect('delete-event', Gtk.main_quit)
window.show_all()

Gtk.main()