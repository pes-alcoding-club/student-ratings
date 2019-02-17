import sys
import csv
import logging
from ratings import elo
from tinydb import TinyDB, where

DB_FILE = 'database/db.json'
CONTEST_RANKS_DIR = 'database/contest_ranks'
UNMAPPED_HANDLES_FILE = 'database/unmapped_handles.out'

# Following attributes must be present for all players in the database
USN = 'usn'
NAME = 'name'
EMAIL = 'email'
YEAR = 'year'  # year of graduation
RATING = 'rating'
VOLATILITY = 'volatility'
TIMES_PLAYED = 'timesPlayed'
BEST = 'best'
LAST_FIVE = 'lastFive'

# Following attributes are optional in the database
CODEJAM = 'codejam'
KICKSTART = 'kickstart'
HACKEREARTH = 'hackerearth'
HACKERRANK = 'hackerrank'
FACEBOOK = 'facebook'
CODECHEF = 'codechef'
CODEFORCES = 'codeforces'

SITES = [CODEJAM, KICKSTART, HACKEREARTH, HACKERRANK, FACEBOOK, CODECHEF, CODEFORCES]

# Following are constraints used to check for validity of data
VALID_MIN_YEAR = 2018
VALID_MAX_YEAR = 2022
VALID_USN_REGEX = r"^((1PI14\w{2}\d{3})|(01FB1([4567])\w{3}\d{3})|(PES12017\d{5}))$"
VALID_EMAIL_REGEX = r"^[^@]+\@[^@]+$"
VALID_USERNAME_REGEX = r"^[\w_\-.]{3,}$"
VALID_NAME_REGEX = r"^([A-Z][a-z]*\s)*[A-Z][a-z]*$"


def reset_database(filename: str = DB_FILE, outfile: str = DB_FILE) -> None:
    """
    Resets all players' attributes to default values
    :param filename: json file where database is stored
    :param outfile: json file where reset database is to be written
    :return: None
    """
    with TinyDB(filename) as database:
        database.update({RATING: elo.DEFAULT_RATING,
                         VOLATILITY: elo.DEFAULT_VOLATILITY,
                         BEST: elo.DEFAULT_RATING,
                         TIMES_PLAYED: 0,
                         LAST_FIVE: 5})
    logging.info('Successfully reset database and stored in ' + outfile)


def export_to_csv(outfile: str = 'scoreboard.csv', filename: str = DB_FILE) -> None:
    """
    Exports database to CSV file for readable form of scoreboard
    :param filename: json file where database is stored
    :param outfile: csv file where database has to be exported
    :return: None
    """
    with TinyDB(filename) as database:

        csv_table = [["Rank", "USN", "Name", "Graduation Year", "Contests", "Rating", "Best"]]

        player_list = database.search(where(TIMES_PLAYED) > 0)
        player_list.sort(key=lambda x: x[RATING], reverse=True)

        for rank, player_dict in enumerate(player_list, start=1):
            row = [rank,
                   player_dict[USN],
                   player_dict[NAME],
                   player_dict[YEAR],
                   player_dict[TIMES_PLAYED],
                   round(player_dict[RATING]),
                   round(player_dict[BEST])]
            csv_table.append(row[:])

        with open(outfile, 'w', newline="") as f:
            wr = csv.writer(f)
            wr.writerows(csv_table)

    logging.info('Successfully exported database to ' + outfile)


if __name__ == "__main__":
    # While executing this script, you can specify which function to execute
    func_str = sys.argv[1]
    try:
        func_obj = globals()[func_str]
        func_obj(*sys.argv[2:])  # Arguments to specified function can be passed
    except KeyError:
        logging.error('Provided invalid argument. No function ' + func_str)
