import sys
import csv
import logging
from json import load, dump
from ratings import elo

DB_FILE = 'database/database.json'

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


def read_database(filename=DB_FILE):
    """
    Reads json file and returns database of all players
    :param filename: json file
    :return: A dictionary with key as SRN and values as dicts with player details
    """
    try:
        with open(filename, 'r') as f:
            database = load(f)
        check_database(database)
        return database

    except IOError or FileNotFoundError:
        logging.error('Could not open ' + filename)
        quit()


def write_database(database, filename=DB_FILE):
    """
    Writes database object to a json file
    :param database: data represented as a dict of dicts
    :param filename: json file where database is saved
    :return: None
    """
    check_database(database)
    try:
        with open(filename, 'w') as f:
            dump(database, f)
        logging.info('Successfully written database to ' + filename)

    except IOError or FileNotFoundError:
        logging.error('Could not open ' + filename)
        quit()


def reset_database(filename=DB_FILE, outfile=DB_FILE):
    """
    Resets all players' attributes to default values
    :param filename: json file where database is stored
    :param outfile: json file where reset database is to be written
    :return: None
    """
    database = read_database(filename)

    for srn in database:
        database[srn][RATING] = elo.DEFAULT_RATING
        database[srn][VOLATILITY] = elo.DEFAULT_VOLATILITY
        database[srn][BEST] = elo.DEFAULT_RATING
        database[srn][TIMES_PLAYED] = 0
        database[srn][LAST_FIVE] = 5

    write_database(database, outfile)
    logging.info('Successfully reset database and stored in ' + outfile)


def check_database(database):
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


def export_to_csv(filename=DB_FILE, outfile='scoreboard.csv'):
    """
    Exports database to CSV file for readable form of scoreboard
    :param filename: json file where database is stored
    :param outfile: csv file where database has to be exported
    :return: None
    """
    database = read_database(filename)

    csv_table = [["Rank", "SRN", "Name", "Contests", "Rating", "Best"]]

    # Remove players who have never played
    srn_list = list(filter(lambda x: database[x][TIMES_PLAYED], database.keys()))

    # Sort the remaining players by their rating
    srn_list.sort(key=lambda x: database[x][RATING], reverse=True)

    # Assign ranks and create rows
    for rank, srn in enumerate(srn_list, start=1):
        row = list()
        row.append(rank)
        row.append(srn)
        row.append(database[srn]['name'])
        row.append(database[srn][TIMES_PLAYED])
        row.append(round(database[srn][RATING]))
        row.append(round(database[srn][BEST]))
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
