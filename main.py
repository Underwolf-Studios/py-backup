from gi.repository import Gtk
import gi
import os

gi.require_version("Gtk", "3.0")

builder = Gtk.Builder()
builder.add_from_file("ui/main.glade")


def add_item(path):
    size = os.path.getsize(path)
    liststore = builder.get_object("liststore")
    liststore.append([path, round(size / 1024 / 1024, 2)])


def on_button_add_clicked(self):
    # Get path from text field
    path = builder.get_object("entry_path").get_text()
    add_item(path)


def on_selection_changed(selection):
    # Get treeview selection
    (model, iter) = selection.get_selected()

    if iter is not None:
        print("Path: " + (model[iter][0]) + " Size: " + str((model[iter][1])))
    else:
        print("")
    return True


def open_file_dialog(self):
    # Set dialog
    file_dialog = Gtk.FileChooserDialog(
        title="Select the File", parent=None, action=Gtk.FileChooserAction.OPEN)

    # Set buttons for dialog
    file_dialog.add_buttons(
        "Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)

    response = file_dialog.run()

    # Button responses
    if response == Gtk.ResponseType.OK:
        add_item(file_dialog.get_filename())

    # Close dialog after finishing
    file_dialog.destroy()


handlers = {
    "on_button_add_clicked": on_button_add_clicked,
    "on_selection_changed": on_selection_changed,
    "on_botton_browse_clicked": open_file_dialog
}
builder.connect_signals(handlers)

window = builder.get_object("main")
window.connect('delete-event', Gtk.main_quit)
window.show_all()

Gtk.main()
