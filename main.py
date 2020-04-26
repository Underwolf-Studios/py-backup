import gi
import os
import zipfile

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


builder = Gtk.Builder()
builder.add_from_file("ui/main.glade")

liststore = builder.get_object("liststore")


def message(title, message, parent=None):
    dialog = Gtk.MessageDialog(
        title=title,
        parent=parent,
        type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        message_format=message)
    dialog.run()
    dialog.destroy()


def add_item(path):
    try:
        f = open(path)
        size = os.path.getsize(path)
        liststore.append([path, round(size / 1024 / 1024, 2)])
    except IOError:
        message("Error", "File does not exist.")
        return
    finally:
        f.close()


def on_button_openfolder_clicked(self):
    # Set dialog for folder selection
    file_dialog = Gtk.FileChooserDialog(
        title="Select the File", parent=None, action=Gtk.FileChooserAction.SELECT_FOLDER)
    file_dialog.set_select_multiple(True)
    button_response_dialog(file_dialog)


def on_button_openfile_clicked(self):
    # Set dialog for file selection
    file_dialog = Gtk.FileChooserDialog(
        title="Select the File", parent=None, action=Gtk.FileChooserAction.OPEN)
    file_dialog.set_select_multiple(True)
    button_response_dialog(file_dialog)


def on_button_add_clicked(self):
    # Get path from text field
    path = builder.get_object("entry_path").get_text()
    add_item(path)


def on_selection_changed(selection):
    # Get treeview selection
    (model, iter) = selection.get_selected()
    print(selection.get_selected())

    if iter is not None:
        print("Path: " + (model[iter][0]) + " Size: " + str((model[iter][1])))
    else:
        print("")
    return True


def on_button_backup_clicked(self):
    files = {}

    # Create zipfile
    with zipfile.ZipFile("backup.zip", 'w') as zf:
        for i in range(0, len(liststore)):
            # Add all paths and sizes to the files dict
            files[liststore[i][0]] = liststore[i][1]
            zf.write(liststore[i][0])

    # Calculate total size and show dialog
    message("Info", "Backup created. Total filesize: " +
            str(round(sum(files.values()), 2)) + "MB")


def button_response_dialog(file_dialog):
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
    "on_button_openfolder_clicked": on_button_openfolder_clicked,
    "on_button_openfile_clicked": on_button_openfile_clicked,
    "on_button_add_clicked": on_button_add_clicked,
    "on_selection_changed": on_selection_changed,
    "on_button_backup_clicked": on_button_backup_clicked
}
builder.connect_signals(handlers)

window = builder.get_object("main")
window.connect('delete-event', Gtk.main_quit)
window.show_all()

Gtk.main()
