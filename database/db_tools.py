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
                assert all(RATING in player_dict_dict[x] for x in player_dict_dict)
                assert all(VOLATILITY in player_dict_dict[x] for x in player_dict_dict)
                assert all(TIMES_PLAYED in player_dict_dict[x] for x in player_dict_dict)
                assert all(BEST in player_dict_dict[x] for x in player_dict_dict)
                assert all(LAST_FIVE in player_dict_dict[x] for x in player_dict_dict)
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


def export_to_csv(filename=DB_FILE, outfile='../scoreboard.csv'):

    player_dict_dict = read_database(filename)

    csv_table = [["Rank", "SRN", "Name", "Contests", "Rating", "Best"]]

    # Remove players who have never played
    player_srn_list = list(filter(lambda x: player_dict_dict[x][TIMES_PLAYED], player_dict_dict.keys()))

    # Sort the remaining players by their rating
    player_srn_list.sort(key=lambda x: player_dict_dict[x][RATING], reverse=True)

    # Assign ranks and create rows
    for rank, player_srn in enumerate(player_srn_list, start=1):
        row = list()
        row.append(rank)
        row.append(player_srn)
        row.append(player_dict_dict[player_srn]['name'])
        row.append(player_dict_dict[player_srn][TIMES_PLAYED])
        row.append(player_dict_dict[player_srn][RATING])
        row.append(player_dict_dict[player_srn][BEST])
        csv_table.append(row[:])

    with open(outfile, 'w', newline="") as f:
        wr = csv.writer(f)
        wr.writerows(csv_table)
