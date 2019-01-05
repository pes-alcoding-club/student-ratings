import sys
import logging
from ratings import elo
from database import db_tools as db
from tinydb import TinyDB, Query, where

class RatingProcessor:

    def __init__(self, rank_file: str, contest_site: str):
        self.handle_rank_dict = self.read_contest_ranks(rank_file)
        self.N, self.Cf, self.Rb_Vb_list = self.get_contest_details(contest_site)
        self.process_competition(contest_site)


    @staticmethod
    def read_contest_ranks(file_path: str) -> dict:
        """
        Reads the file containing rank list and builds a dict
        :param file_path: .in file containing the rank list
        :return: dict with key as player's handle of the website and value as rank
        """
        handle_rank_dict = dict()
        current_rank = 1
        with open(file_path, 'r') as f:
            for handles in f:
                handles = handles.split()  # multiple players with same rank
                next_rank = current_rank + len(handles)
                for handle in handles:
                    handle_rank_dict[handle] = current_rank
                current_rank = next_rank

        return handle_rank_dict

    def get_contest_details(self, contest_site: str) -> tuple:

        db_obj = TinyDB(db.DB_FILE)
        rating_list, vol_list = [], []

        for handle in self.handle_rank_dict:
            temp_player =  db_obj.search(where(contest_site) == handle)
            if len(temp_player) != 1:
                logging.error("Username: " + handle + " in " + contest_site + " does not exist in the database")
                quit()
            rating_list.append(temp_player[0][db.RATING])
            vol_list.append(temp_player[0][db.VOLATILITY])

        n = len(self.handle_rank_dict)
        competition_factor = elo.Cf(rating_list, vol_list, n)
        rating_vol_tup_list = list(zip(rating_list, vol_list))
        db_obj.close()

        return n, competition_factor, rating_vol_tup_list


    def _decay_player(self, player_dict: dict) -> dict:
        """
        Reduces ratings by 10% for those who have competed at least once
        but have not taken part in the past 5 contests
        :param srn_rank_dict: dict with key as srn and value as rank
        :return: None
        """
        rating = player_dict[db.RATING]
        times_played = player_dict[db.TIMES_PLAYED]
        last_five = player_dict[db.LAST_FIVE] - 1

        if last_five == 0 and times_played > 0:
            rating = rating * 0.9
            last_five = 5

        player_dict[db.RATING] = rating
        player_dict[db.LAST_FIVE] = max(1, last_five)

        logging.info('Successfully decayed ratings')
        return player_dict


    def _update_player(self, player_dict: dict, actual_rank: int) -> dict:
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

        return player_dict


    def process_competition(self, contest_site: str):

        db_obj = TinyDB(db.DB_FILE)
        rows = db_obj.all()
        for row in rows:
            if contest_site in row and row[contest_site] in self.handle_rank_dict:
                actual_rank = self.handle_rank_dict[row[contest_site]]
                new_data = self._update_player(row, actual_rank)
            else:
                new_data = self._decay_player(row)
            row.update(new_data)
        db_obj.write_back(rows)


def read_argv(argv_format_alert: str):
    """
    :param argv_format_alert: An error message on what the command line arguments should be
    :return: 2-tuple of rank file and the contest site if argv is valid
    """
    try:
        assert len(sys.argv) == 3
        rank_file = sys.argv[1]
        contest_site = sys.argv[2]
        try:
            f = open(rank_file)
            f.close()
            return rank_file, contest_site

        except IOError or FileNotFoundError:
            logging.error('Invalid file path for rank file\n' + argv_format_alert)
            quit()

    except AssertionError:
        logging.error('Invalid command line arguments.\n' + argv_format_alert)
        quit()


if __name__ == "__main__":

    argv_format = 'processor.py rank_file_path contest_site_str'
    rank_file_path, contest_site_str = read_argv(argv_format)
    rp = RatingProcessor(rank_file_path, contest_site_str)
