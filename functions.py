import datetime
import os
import zipfile

import utils


def add_item(liststore, path):
    try:
        f = open(path)
        size = os.path.getsize(path)
        liststore.append([path, round(size / 1024 / 1024, 2)])
        f.close()
    except IOError:
        utils.message("error", "File does not exist.")
        return


def remove_item(treeview, liststore):
    selection = treeview.get_selection()
    model, paths = selection.get_selected_rows()

    for path in paths:
        iter = model.get_iter(path)
        model.remove(iter)


def backup(liststore, filename, check_date, check_version, builder):
    files = {}
    name = filename
    date = "{0:%Y%m%d_%H%M}".format(datetime.datetime.now())

    spin_version = builder.get_object("spin_version")

    if check_date == True and check_version == False:
        name = f"{filename}_{date}"
    elif check_date == False and check_version == True:
        name = f"{filename}_v{str(spin_version.get_value_as_int())}"
    elif check_date == True and check_version == True:
        name = f"{filename}_{date}_v{str(spin_version.get_value_as_int())}"

    # Create zipfile
    with zipfile.ZipFile("backups/" + name + ".zip", 'w') as zf:
        for i in range(0, len(liststore)):
            # Add all paths and sizes to the files dict
            files[liststore[i][0]] = liststore[i][1]
            zf.write(liststore[i][0])

    # Calculate total size and show dialog
    utils.message("info", name + ".zip created. Total filesize: " + str(round(sum(files.values()), 2)) + "MB")
