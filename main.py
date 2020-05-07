import os
import zipfile

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import functions
import utils

# Builder
builder = Gtk.Builder()
builder.add_from_file("ui/main.glade")

# Windows
window_main = builder.get_object("window_main")
window_main.connect('delete-event', Gtk.main_quit)

window_backup = builder.get_object("window_backup")
window_backup.connect('delete-event', lambda w, e: w.hide() or True)

window_create = builder.get_object("window_create")
window_create.connect('delete-event', lambda w, e: w.hide() or True)

# Objects
liststore_files = builder.get_object("liststore_files")
treestore_backups = builder.get_object("treestore_backups")
treeview_backups = builder.get_object("treeview_backups")
treeview_files = builder.get_object("treeview_files")
check_timestamp = builder.get_object("check_timestamp")
check_version = builder.get_object("check_version")


functions.check_local(treestore_backups)


class Handlers:
    def on_button_openfolder_clicked(self, button):
        utils.open_filechooser("folder", liststore_files)

    def on_button_openfile_clicked(self, button):
        utils.open_filechooser("file", liststore_files)

    def on_button_add_clicked(self, button):
        path = builder.get_object("entry_path").get_text()
        functions.add_item(liststore_files, path)

    def on_button_backup_clicked(self, button):
        window_create.show()

    def on_button_newbackup_clicked(self, button):
        window_backup.show()

    def on_button_removebackup_clicked(self, button):
        functions.remove_item(treeview_backups)

    def on_button_removepath_clicked(self, button):
        functions.remove_item(treeview_files)

    def on_button_create_clicked(self, button):
        filename = builder.get_object("entry_filename").get_text()
        functions.backup(liststore_files, filename, check_timestamp.get_active(), check_version.get_active(), builder)

        functions.check_local(treestore_backups)

        window_create.hide()
        window_backup.hide()


builder.connect_signals(Handlers())

window_main.show_all()

Gtk.main()
