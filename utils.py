import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import functions


def message(msg_type, message):
    if msg_type == "error":
        msg_type = Gtk.MessageType.ERROR
        title = "Error"
    elif msg_type == "info":
        msg_type = Gtk.MessageType.INFO
        title = "Info"

    message_dialog = Gtk.MessageDialog(title=title, type=msg_type, buttons=Gtk.ButtonsType.OK, message_format=message, parent=None)
    message_dialog.run()
    message_dialog.destroy()


def open_filechooser(fc_type, liststore):
    if fc_type == "file":
        title = "Select File"
        fc_action = Gtk.FileChooserAction.OPEN
    elif fc_type == "folder":
        title = "Select Folder"
        fc_action = Gtk.FileChooserAction.SELECT_FOLDER

    file_dialog = Gtk.FileChooserDialog(title=title, action=fc_action, parent=None)
    file_dialog.set_select_multiple(True)

    # Set buttons for dialog
    file_dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)

    response = file_dialog.run()

    # Add item
    if response == Gtk.ResponseType.OK:
        functions.add_item(liststore, file_dialog.get_filename())

    # Close dialog after finishing
    file_dialog.destroy()
