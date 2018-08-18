import csv
import logging
from json import load, dump
from ratings import elo

DB_FILE = 'database.json'

# Following attributes must be present for all players in the database
RATING = 'rating'
VOLATILITY = 'volatility'
TIMES_PLAYED = 'timesPlayed'
BEST = 'best'
LAST_FIVE = 'lastFive'

# Following attriabutes are optional in the database
CODEJAM = 'codejam'
KICKSTART = 'kickstart'
HACKEREARTH = 'hackerearth'
HACKERRANK = 'hackerrank'
FACEBOOK = 'facebook'
CODECHEF = 'codechef'


def read_database(filename=DB_FILE):
    try:
        with open(filename, 'r') as f:
            player_dict_dict = load(f)
            try:
                assert isinstance(player_dict_dict, dict)
                assert all(isinstance(player_dict_dict[x], dict) for x in player_dict_dict)
                assert all(RATING in x for x in player_dict_dict)
                assert all(VOLATILITY in x for x in player_dict_dict)
                assert all(TIMES_PLAYED in x for x in player_dict_dict)
                assert all(BEST in x for x in player_dict_dict)
                assert all(LAST_FIVE in x for x in player_dict_dict)
            except AssertionError:
                logging.error('Database not read in expected format. Missing some fields.')
            return player_dict_dict

    except IOError:
        logging.error('Could not open ' + filename)


def write_database(player_dict_dict, filename=DB_FILE):
    try:
        with open(filename, 'w') as f:
            dump(player_dict_dict, f)

    except IOError:
        logging.error('Could not open ' + filename)


def reset_database(filename=DB_FILE, outfile=DB_FILE):
    try:
        with open(filename, 'r') as f:
            player_dict_dict = load(f)

        for player_srn in player_dict_dict:
            player_dict_dict[player_srn][RATING] = elo.DEFAULT_RATING
            player_dict_dict[player_srn][VOLATILITY] = elo.DEFAULT_VOLATILITY
            player_dict_dict[player_srn][BEST] = elo.DEFAULT_RATING
            player_dict_dict[player_srn][TIMES_PLAYED] = 0
            player_dict_dict[player_srn][LAST_FIVE] = 5

        with open(outfile, 'w') as f:
            dump(player_dict_dict, f)

        logging.info('Successfully reset database and stored in ' + outfile)

    except IOError:
        logging.error('Could not open ' + filename)


def export_to_csv(filename=DB_FILE, outfile='alcoding/scoreboard.csv'):
    player_dict_dict = read_database(filename)
    csv_table = []

    for player_srn in player_dict_dict:
        if player_dict_dict[player_srn][TIMES_PLAYED] == 0:
            continue
        row = list()
        row.append(player_srn)
        row.append(player_dict_dict[player_srn]['name'])
        row.append(player_dict_dict[player_srn][TIMES_PLAYED])
        row.append(player_dict_dict[player_srn][RATING])
        row.append(player_dict_dict[player_srn][BEST])
        csv_table.append(row[:])

    csv_table.sort(key=lambda x: x[3], reverse=True)

    for rank in range(1, len(csv_table)+1):
        csv_table.insert(0, rank)

    csv_table.insert(0, ["Rank", "SRN", "Name", "Contests", "Rating", "Best"])

    with open(outfile, 'w') as f:
        wr = csv.writer(f)
        wr.writerows(csv_table)
