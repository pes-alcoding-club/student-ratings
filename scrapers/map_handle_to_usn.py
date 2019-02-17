"""
This file maps usernames in contests scoreboards to PESU USNs.
This ensures that even if the player changes their username on a site,
we are aware of their rank in the past.
After replacing the username with USN,
it also logs the usernames that have not been mapped to any USNs so far.
Unmapped users are simply ignored from rating calculation and can be added later.

Note: username and handles mean the same but are used interchangeably.
todo: code clean up. Move this function to db_tools and add call it from executor.sh
"""

import re
from os import listdir, path
from collections import Counter
from functools import lru_cache
from tinydb import TinyDB
from database.db_tools import DB_FILE, USN, CONTEST_RANKS_DIR, UNMAPPED_HANDLES_FILE, VALID_USN_REGEX


@lru_cache(maxsize=8)
def get_handle_usn_map(site_name):
    handle_usn_map = dict()
    with TinyDB(DB_FILE) as database:
        for doc in database:
            if site_name in doc:
                handle_usn_map[doc[site_name]] = doc[USN]
    return handle_usn_map


if __name__ == "__main__":
    unmapped_handles: list = []
    valid_usn_regex = re.compile(VALID_USN_REGEX)
    for file_path in listdir(CONTEST_RANKS_DIR):  # go through every contest rank file
        with open(path.join(CONTEST_RANKS_DIR, file_path)) as fp:
            site = file_path.split("-")[0]   # identify the site name from the file name
            input_data = fp.read()
        handle_usn_dict = get_handle_usn_map(site)
        for handle in sorted(handle_usn_dict.keys(), key=lambda x: len(x), reverse=True):
            usn = handle_usn_dict[handle]
            input_data = input_data.replace(handle, usn, 1)  # replace the username with USN
        with open(path.join(CONTEST_RANKS_DIR, file_path), "w") as fp:
            fp.write(input_data)  # write back the replaced names
        candidates = [(site, x) for x in input_data.split()]  # identify handles not mapped to any USN
        unmapped_handles += list(filter(lambda x: not valid_usn_regex.match(x[1]), candidates))
    counter = Counter(unmapped_handles)
    with open(UNMAPPED_HANDLES_FILE, "w") as fp:  # write unmapped handles to a file
        print(len(counter), file=fp)
        print(*counter.most_common(), sep='\n', file=fp)
