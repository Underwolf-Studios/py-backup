from gi.repository import Gtk

import gi
import os
import zipfile

gi.require_version("Gtk", "3.0")

builder = Gtk.Builder()
builder.add_from_file("ui/main.glade")

liststore = builder.get_object("liststore")


def error_msg(msg, parent=None):
    dialog = Gtk.MessageDialog(
        title="Error",
        parent=parent,
        type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        message_format=msg)
    dialog.run()
    dialog.destroy()


def info_msg(msg, parent=None):
    dialog = Gtk.MessageDialog(
        title="Info",
        parent=parent,
        type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        message_format=msg)
    dialog.run()
    dialog.destroy()


def add_item(path):
    try:
        f = open(path)
        size = os.path.getsize(path)
        liststore.append([path, round(size / 1024 / 1024, 2)])
    except IOError:
        error_msg("File does not exist.")
    finally:
        f.close()


def on_button_add_clicked(self):
    # Get path from text field
    path = builder.get_object("entry_path").get_text()
    add_item(path)


def on_button_backup_clicked(self):
    files = {}

    # Create zipfile
    with zipfile.ZipFile("backup.zip", 'w') as zf:
        for i in range(0, len(liststore)):
            # Add all paths and sizes to the files dict
            files[liststore[i][0]] = liststore[i][1]
            zf.write(liststore[i][0])

    # Calculate total size
    info_msg("Backup created. Total filesize: " +
             str(round(sum(files.values()), 2)) + "MB")


def on_selection_changed(selection):
    # Get treeview selection
    (model, iter) = selection.get_selected()
    print(selection.get_selected())

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
    "on_button_backup_clicked": on_button_backup_clicked,
    "on_selection_changed": on_selection_changed,
    "on_botton_browse_clicked": open_file_dialog
}
builder.connect_signals(handlers)

window = builder.get_object("main")
window.connect('delete-event', Gtk.main_quit)
window.show_all()

Gtk.main()
