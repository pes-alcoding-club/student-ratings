import sys
import logging
from time import time
from ratings import elo
from database import db_tools as db
from tinydb import TinyDB, where


class RatingProcessor:

    def __init__(self, database: TinyDB, rank_file):
        self.database: TinyDB = database

        self.N: int = 0
        self.Cf: float = 0.0
        self.Rb_Vb_list: list = []
        self.usn_rank_dict: dict = {}

        self.read_contest_ranks(rank_file)  # sets usn_rank_dict
        self.set_contest_details()  # sets N, Cf and Rb_Vb_list
        self.process_competition()  # uses the set attributes to compute new ratings

    def read_contest_ranks(self, rank_file) -> None:
        """
        Reads the file containing rank list and builds a dict
        :param rank_file: .in file containing the rank list
        :return: dict with key as player's USN and value as rank
        """
        current_rank = 1
        for usns in rank_file:
            usns = usns.split()
            same_rank_count = 0  # number of players with same rank
            for usn in usns:  # multiple usn with the same rank is possible
                if self.database.contains(where(db.USN) == usn):
                    self.usn_rank_dict[usn] = current_rank
                    same_rank_count += 1
                else:
                    logging.info(f'Ignoring usn {usn}')
            current_rank += same_rank_count  # ranks are not 1, 1, 1, 2 but 1, 1, 1, 4
        logging.debug(self.usn_rank_dict)

    def set_contest_details(self) -> None:
        """
        Generates some details about the participants of the contest
        that are required to update all players' ratings
        """

        # Get all the details of the participants from the provided USN
        participants = self.database.search(where(db.USN).test(lambda x: x in self.usn_rank_dict))

        rating_list = [x[db.RATING] for x in participants]
        vol_list = [x[db.VOLATILITY] for x in participants]

        self.N = len(self.usn_rank_dict)
        self.Cf = elo.Cf(rating_list, vol_list, self.N)
        self.Rb_Vb_list = list(zip(rating_list, vol_list))
        logging.debug(f'Contest: {rank_file_path}\nPlayers: {self.N}\nCompetition Factor: {self.Cf}')

    @staticmethod
    def _decay_player(player_dict: dict) -> None:
        """
        Reduces ratings by 10% for those who have competed at least once
        but have not taken part in the past 5 contests
        :param player_dict: dict with all details of a player
        """
        rating = player_dict[db.RATING]
        times_played = player_dict[db.TIMES_PLAYED]
        last_five = player_dict[db.LAST_FIVE]

        if times_played > 0:  # decay does not take effect for people who have never taken part
            last_five -= 1
            if last_five == 0:  # indicates that player has not taken part for last 5 contests
                rating = rating * 0.99
                last_five = 5  # reduces the rating and resets last_five

        player_dict[db.RATING] = rating
        player_dict[db.LAST_FIVE] = max(1, last_five)

        logging.debug('Successfully decayed ratings')

    def _update_player(self, player_dict: dict, actual_rank: int) -> None:
        """
        :param player_dict: dictionary containing player's details
        :param actual_rank: rank of the player in the competition
        :return: dictionary of player's details after processing rank
        """

        old_rating = player_dict[db.RATING]
        old_volatility = player_dict[db.VOLATILITY]
        times_played = player_dict[db.TIMES_PLAYED]
        old_best = player_dict[db.BEST]

        new_rating, new_volatility = elo.process(
            old_rating, old_volatility, times_played, actual_rank, self.Rb_Vb_list, self.N, self.Cf)

        player_dict[db.RATING] = new_rating
        player_dict[db.VOLATILITY] = new_volatility
        player_dict[db.TIMES_PLAYED] = times_played + 1
        player_dict[db.BEST] = max(old_best, new_rating)
        player_dict[db.LAST_FIVE] = 5

        logging.debug('Successfully updated ratings')

    def process_competition(self) -> None:

        rows = self.database.all()
        for row in rows:
            logging.debug(f'Before: {row}')
            if row[db.USN] in self.usn_rank_dict:
                actual_rank = self.usn_rank_dict[row[db.USN]]
                self._update_player(row, actual_rank)
            else:
                self._decay_player(row)
            logging.debug(f'After: {row}')
        self.database.write_back(rows)


def read_argv(argv_format_alert: str):
    """
    :param argv_format_alert: An error message on what the command line arguments should be
    :return: rank file if argv is valid
    """
    try:
        assert len(sys.argv) == 2
        rank_file = sys.argv[1]
        try:
            open(rank_file).close()
            return rank_file

        except IOError or FileNotFoundError:
            logging.error(f'Invalid file path for rank file: {rank_file}\n{argv_format_alert}')
            quit()

    except AssertionError:
        logging.error(f'Invalid command line arguments.\n{argv_format_alert}')
        quit()


if __name__ == "__main__":
    start_time = time()

    argv_format = 'processor.py rank_file_path'
    rank_file_path = read_argv(argv_format)

    # Main logic starts here
    database_obj = TinyDB(db.DB_FILE)
    rank_file_obj = open(rank_file_path)
    RatingProcessor(database_obj, rank_file_obj)
    database_obj.close()

    duration = time()-start_time
    logging.debug(f'Updated ratings for {rank_file_path}')
    if duration > 10:
        logging.critical(f'Ratings update for {rank_file_path} took {duration} seconds.\n'
                         f'Consider removing unnecessary handles or optimize ratings algorithm')
