import gi
import os
import zipfile
import functions
import utils

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


builder = Gtk.Builder()
builder.add_from_file("src/ui/main.glade")

window_backup = builder.get_object("window_backup")
window_backup.connect('delete-event', window_backup.close)

window_create = builder.get_object("window_create")
window_create.connect('delete-event', window_create.close)

liststore = builder.get_object("liststore_files")


class Handlers:
    def on_button_openfolder_clicked(self, button):
        utils.open_filechooser("folder", liststore)

    def on_button_openfile_clicked(self, button):
        utils.open_filechooser("file", liststore)

    def on_button_add_clicked(self, button):
        path = builder.get_object("entry_path").get_text()
        functions.add_item(liststore, path)

    def on_selection_files_changed(self, selection):
        # Get treeview selection
        (model, iter) = selection.get_selected()

        if iter is not None:
            print("Path: " + (model[iter][0]) + " Size: " + str((model[iter][1])))
        return True

    def on_selection_backups_changed(self, selection):
        # Get treeview selection
        (model, iter) = selection.get_selected()

        if iter is not None:
            print("Path: " + (model[iter][0]) + " Size: " + str((model[iter][1])))
        return True

    def on_button_backup_clicked(self, button):
        window_create.show_all()

    def on_button_newbackup_clicked(self, button):
        window_backup.show_all()

    # TODO: get treeview selection
    def on_button_removebackup_clicked(self, button):
        functions.remove_item(liststore, "path")

    def on_button_removepath_clicked(self, button):
        functions.remove_item(liststore, "path")

    def on_button_create_clicked(self, button):
        try:
            filename = builder.get_object("entry_filename").get_text()
            functions.backup(liststore, filename)
        except:
            utils.message("error", "Sorry, something went wrong.")

        window_create.close()
        window_backup.close()


builder.connect_signals(Handlers())


window_main = builder.get_object("window_main")
window_main.connect('delete-event', Gtk.main_quit)
window_main.show_all()

Gtk.main()
