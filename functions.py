import datetime
import os
import zipfile

import utils


def add_item(liststore, path):
    try:
        size = str(round(os.path.getsize(path) / 1024 / 1024, 2))
        liststore.append([path, size])
    except:
        utils.message("error", "File does not exist.")


def remove_item(treeview):
    store, paths = treeview.get_selection().get_selected_rows()

    for path in reversed(paths):
        iter = store.get_iter(path)
        store.remove(iter)


def backup(liststore, filename, check_timestamp, check_version, builder):
    files = {}
    name = filename
    timestamp = "{0:%Y%m%d_%H%M}".format(datetime.datetime.now())

    spin_version = builder.get_object("spin_version")

    if check_timestamp and not check_version:
        name = f"{filename}_{timestamp}"
    elif not check_timestamp and check_version:
        name = f"{filename}_v{str(spin_version.get_value_as_int())}"
    elif check_timestamp and check_version:
        name = f"{filename}_{timestamp}_v{str(spin_version.get_value_as_int())}"

    # Create zipfile
    with zipfile.ZipFile("backups/" + name + ".zip", 'w') as zf:
        for i in range(0, len(liststore)):
            # Add all paths and sizes to the files dict
            files[liststore[i][0]] = liststore[i][1]
            zf.write(liststore[i][0])

    # Calculate total size and show dialog
    utils.message("info", name + ".zip created. Total filesize: " + str(round(sum(files.values()), 2)) + "MB")


def check_local(treestore):
    path = "backups/"
    files = os.listdir(path)

    treestore.clear()

    iter = treestore.append(None, ["Local", " "])

    for file in files:
        size = str(round(os.path.getsize(path + file) / 1024 / 1024, 2))
        treestore.append(iter, [str(file), size])


def check_googledrive(treestore):
    pass


def check_dropbox(treestore):
    pass
