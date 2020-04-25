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

def open_file_dialog(self):

    # Set dialog
    file_dialog = Gtk.FileChooserDialog(
                title = "Select the File", parent = None, action = Gtk.FileChooserAction.OPEN)
    
    # Set buttons for dialog
    file_dialog.add_buttons ("Cancel", Gtk.ResponseType.CANCEL,"Open", Gtk.ResponseType.OK) 
    response = file_dialog.run()

    # Button responses
    if response == Gtk.ResponseType.OK:
        print("Open Button")
        print("File: "+ file_dialog.get_filename())
    elif response == Gtk.ResponseType.CANCEL:
        print("Cancel")

    #Close dialog after finishing
    file_dialog.destroy()

handlers = {
    "on_button_add_clicked": additem,
    "on_selection_changed": on_selection_changed,
    "on_botton_browse_clicked": open_file_dialog
}
builder.connect_signals(handlers)

window = builder.get_object("main")
window.connect('delete-event', Gtk.main_quit)
window.show_all()

Gtk.main()