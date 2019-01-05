import sys
import csv
import logging
from ratings import elo
from tinydb import TinyDB, where

DB_FILE = 'database/db.json'

# Following attributes must be present for all players in the database
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


def check_database(database: dict) -> None:
    """
    Checks if the database is in the required format
    :param database: database object expected to be dict of dicts
    :return: None. Quits if database is not in required format
    """
    try:
        assert isinstance(database, dict)
        assert all(isinstance(database[x], dict) for x in database)
        assert all(RATING in database[x] for x in database)
        assert all(VOLATILITY in database[x] for x in database)
        assert all(TIMES_PLAYED in database[x] for x in database)
        assert all(BEST in database[x] for x in database)
        assert all(LAST_FIVE in database[x] for x in database)
        logging.info('Successfully checked database')

    except AssertionError:
        logging.error('Database not read in expected format. Missing some fields.')
        quit()


def export_to_csv(filename: str = DB_FILE, outfile: str = 'scoreboard.csv') -> None:
    """
    Exports database to CSV file for readable form of scoreboard
    :param filename: json file where database is stored
    :param outfile: csv file where database has to be exported
    :return: None
    """
    with TinyDB(filename) as database:

        csv_table = [["Rank", "USN", "Name", "Contests", "Rating", "Best"]]

        player_list = database.search(where(TIMES_PLAYED) > 0)
        player_list.sort(key=lambda x: x[RATING], reverse=True)

        for rank, player_dict in enumerate(player_list, start=1):
            row = [rank,
                   player_dict['usn'],
                   player_dict['name'],
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
