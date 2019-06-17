import re
import sys
import csv
import logging
from os import listdir
from os.path import join
from collections import Counter
from functools import lru_cache
from typing import List, Set, Tuple, Dict, Callable, Any
from tinydb import TinyDB, where
from ratings import elo

DB_FILE: str = 'database/db.json'
CONTEST_RANKS_DIR: str = 'database/contest_ranks'
UNMAPPED_HANDLES_FILE: str = 'database/unmapped_handles.out'
SCOREBOARD_FILE: str = 'scoreboard.csv'

# Following attributes must be present for all players in the database
USN: str = 'usn'
NAME: str = 'name'
EMAIL: str = 'email'
YEAR: str = 'year'  # year of graduation
RATING: str = 'rating'
VOLATILITY: str = 'volatility'
TIMES_PLAYED: str = 'timesPlayed'
BEST: str = 'best'  # best rating so far
LAST_FIVE: str = 'lastFive'  # to keep track of past five contests to decay ratings

# Following attributes are optional in the database
CODEJAM: str = 'codejam'
KICKSTART: str = 'kickstart'
HACKEREARTH: str = 'hackerearth'
HACKERRANK: str = 'hackerrank'
FACEBOOK: str = 'facebook'
CODECHEF: str = 'codechef'
CODEFORCES: str = 'codeforces'

SITES: Set[str] = {CODEJAM, KICKSTART, HACKEREARTH, HACKERRANK, FACEBOOK, CODECHEF, CODEFORCES}

# Following are constraints used to check for validity of data
VALID_MIN_YEAR: int = 2018
VALID_MAX_YEAR: int = 2022
VALID_USN_REGEX = re.compile(r"^((1PI14\w{2}\d{3})|(01FB1([4567])\w{3}\d{3})|(PES1201[7-8]\d{5}))$")
VALID_EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+$")
VALID_USERNAME_REGEX = re.compile(r"^\S+$")
VALID_NAME_REGEX = re.compile(r"^([A-Z][a-z]*\s)*[A-Z][a-z]*$")


def reset_database(db_file: str = DB_FILE) -> None:
    """
    Resets all players' attributes to default values.
    """
    with TinyDB(db_file) as database:
        database.update({
            RATING: elo.DEFAULT_RATING,
            VOLATILITY: elo.DEFAULT_VOLATILITY,
            BEST: elo.DEFAULT_RATING,
            TIMES_PLAYED: 0,
            LAST_FIVE: 5})
    logging.info(f'Successfully reset database and stored in {db_file}')


def get_site_name_from_file_name(file_name: str) -> str:
    """
    Derives the name of the contest site from the name of the rank file.
    :param file_name: Rank list file.
    :return: name of the contest site.
    """
    file_name_parts = file_name.split("-")
    if len(file_name_parts) < 2 or file_name_parts[0] not in SITES:
        logging.error(f"Invalid filename '{file_name}' in contest ranks. File name convention is"
                      f"'site-contest-details.in'")
        quit()
    return file_name_parts[0]


def map_username_to_usn(db_file: str = DB_FILE,
                        ranks_dir: str = CONTEST_RANKS_DIR,
                        unmapped_handles_file: str = UNMAPPED_HANDLES_FILE) -> None:
    """
    Maps usernames in contests' scoreboards to PESU USNs.
    Ensures that change in username on the site preserves past ranks.
    Logs usernames not been mapped to any USNs which are eventually ignored from ratings.
    """

    @lru_cache(maxsize=len(SITES))
    def get_handle_usn_map(site_name: str) -> Dict[str, str]:
        """
        Get a map to replace the username with the USNs.
        :param site_name: Name of the site for which the contest rank list is mapped.
        :return: dictionary with key value as username and value as USN.
        """
        handle_usn_map: Dict[str, str] = dict()
        with TinyDB(db_file) as database:
            for doc in database:
                if site_name in doc:
                    handle_usn_map[doc[site_name]] = doc[USN]
        return handle_usn_map

    def replace_username_with_usn(data: str, find_replace_dict: Dict[str, str]) -> str:
        """
        Replace username with USN in a text given the mapping.
        :param data: text in which replacement is to be made.
        :param find_replace_dict: mapping with key as username and value as usn.
        :return: text after replacements.
        """
        for find_item in sorted(find_replace_dict.keys(), key=str.__len__, reverse=True):
            replace_item: str = find_replace_dict[find_item]
            data = re.sub(rf"\b{find_item}\b", replace_item, data, re.IGNORECASE)
        return data

    def log_unmapped_handles(site_username_tuple_list: List[Tuple[str, str]]) -> None:
        """
        Makes a list of all the usernames that were not mapped to any USN.
        These will be ignored in ratings until the mapping is added to the database.
        """
        unmapped_handles: List[Tuple[str, str]] \
            = list(filter(lambda x: not VALID_USN_REGEX.match(x[1]), site_username_tuple_list))
        counter = Counter(unmapped_handles)
        with open(unmapped_handles_file, "w") as ptr:
            print(len(counter), file=ptr)
            print(*sorted(counter.items(),
                          key=lambda x: (x[1], x[0][0], x[0][1]),
                          reverse=True),
                  sep='\n', file=ptr)

    site_handle_tuple_list: List[Tuple[str, str]] = list()

    for file_path in listdir(ranks_dir):  # go through all contest rank files
        site: str = get_site_name_from_file_name(file_path)

        handle_usn_dict: Dict[str, str] = get_handle_usn_map(site)

        with open(join(ranks_dir, file_path)) as fp:
            input_data: str = fp.read()

        output_data: str = replace_username_with_usn(input_data, handle_usn_dict)

        with open(join(ranks_dir, file_path), "w") as fp:
            fp.write(output_data)

        if site in [CODECHEF, '''HACKERRANK''']:  # only sites that provide university filter
            site_handle_tuple_list += [(site, x) for x in output_data.split()]

        log_unmapped_handles(site_handle_tuple_list)

    logging.info('Mapped ')


def remove_unmapped_handles_from_rank_file(file_name: str) -> None:
    """
    Removes unmapped handles from outdated rank files
    to reduce space and time it takes for the script to run
    """
    with open(join(CONTEST_RANKS_DIR, file_name), 'r') as rank_file:
        input_data: str = rank_file.read()

    with open(join(CONTEST_RANKS_DIR, file_name), 'w') as rank_file:
        for user_name_line in input_data.split("\n"):
            check_occurrence_in_line: bool = False
            for user_name in user_name_line.split():
                if VALID_USN_REGEX.match(user_name):
                    check_occurrence_in_line = True
                    rank_file.write(user_name + " ")
            if check_occurrence_in_line:
                rank_file.write("\n")
    logging.info(f'Cleaned {file_name}')


def export_to_csv(db_file: str = DB_FILE, scoreboard_file: str = SCOREBOARD_FILE) -> None:
    """
    Exports database to CSV file for readable form of scoreboard.
    """
    with TinyDB(db_file) as database:
        player_list: List[Dict[str, Any]] = database.search(where(TIMES_PLAYED) > 0)

    csv_table: List[tuple] = [
        ("Rank", "USN", "Name", "Graduation Year", "Contests", "Rating", "Best")]

    player_list.sort(key=lambda x: x[RATING], reverse=True)

    for rank, player_dict in enumerate(player_list, start=1):
        row: Tuple[int, str, str, int, int, int, int] \
            = (rank, player_dict[USN], player_dict[NAME],
               player_dict[YEAR], player_dict[TIMES_PLAYED],
               round(player_dict[RATING]), round(player_dict[BEST]))
        csv_table.append(row[:])

    with open(scoreboard_file, 'w', newline="") as fp:
        wr = csv.writer(fp)
        wr.writerows(csv_table)

    logging.info(f'Successfully exported database from {db_file} to {scoreboard_file}')


def prettify(db_file: str = DB_FILE) -> None:
    """
    Indents database Json file to make it more readable and easier to assess diffs.
    """
    with TinyDB(db_file, sort_keys=True, indent=4) as fp:
        fp.write_back(fp.all())


if __name__ == "__main__":
    # While executing this script, you can specify which function to execute
    func_str: str = sys.argv[1]
    try:
        func_obj: Callable = globals()[func_str]
        func_obj(*sys.argv[2:])  # Arguments to specified function can be passed
    except KeyError:
        logging.error(f'Provided invalid argument. No function {func_str}')
