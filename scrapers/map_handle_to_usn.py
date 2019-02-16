import sys
from os import listdir, path
from tinydb import TinyDB

from database.db_tools import DB_FILE, USN, CONTEST_RANKS_DIR


def get_handle_usn_map(site):
    handle_usn_map = dict()
    with TinyDB(DB_FILE) as database:
        for doc in database:
            if site in doc:
                handle_usn_map[doc[site]] = doc[USN]
    return handle_usn_map


if __name__ == "__main__":
    for file_path in listdir(CONTEST_RANKS_DIR):
        with open(path.join(CONTEST_RANKS_DIR, file_path)) as fp:
            site = file_path.split("-")[0]
            input_data = fp.read()
        handle_usn_dict = get_handle_usn_map(site)
        for handle in sorted(handle_usn_dict.keys(), key=lambda x: len(x), reverse=True):
            usn = handle_usn_dict[handle]
            input_data = input_data.replace(handle, usn, 1)
        with open(path.join(CONTEST_RANKS_DIR, file_path), "w") as fp:
            fp.write(input_data)
