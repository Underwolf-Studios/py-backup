import os
import zipfile
import utils


def add_item(liststore, path):
    try:
        f = open(path)
        size = os.path.getsize(path)
        liststore.append([path, round(size / 1024 / 1024, 2)])
    except IOError:
        utils.message("error", "File does not exist.")
        return
    finally:
        f.close()


def remove_item(liststore, path):
    utils.message("info", "Not implemented yet")


def backup(liststore, filename):
    files = {}

    # Create zipfile
    with zipfile.ZipFile(filename + ".zip", 'w') as zf:
        for i in range(0, len(liststore)):
            # Add all paths and sizes to the files dict
            files[liststore[i][0]] = liststore[i][1]
            zf.write(liststore[i][0])

    # Calculate total size and show dialog
    utils.message("info", filename + ".zip created. Total filesize: " + str(round(sum(files.values()), 2)) + "MB")
