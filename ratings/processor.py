import sys
import logging
from ratings import elo
from database import db_tools as db
from tinydb import TinyDB, where


class RatingProcessor:

    def __init__(self, database: TinyDB, rank_file, contest_site: str):
        self.database: TinyDB = database
        self.contest_site = contest_site

        self.N: int = 0
        self.Cf: float = 0.0
        self.Rb_Vb_list: list = []
        self.handle_rank_dict = {}

        self.read_contest_ranks(rank_file)  # sets_handle rank_dict
        self.set_contest_details()  # sets N, Cf and Rb_Vb_list
        self.process_competition()  # uses the set attributes to compute new ratings

    def read_contest_ranks(self, rank_file) -> None:
        """
        Reads the file containing rank list and builds a dict
        :param rank_file: .in file containing the rank list
        :return: dict with key as player's handle of the website and value as rank
        """
        current_rank = 1
        for handles in rank_file:
            handles = handles.split()  # multiple players with same rank
            for handle in handles:
                self.handle_rank_dict[handle] = current_rank
            current_rank += len(handles)

    def set_contest_details(self) -> None:
        """
        Generates some details about the participants of the contest
        that are required to update all players' ratings
        """

        # Check if the provided handles are present in the database
        if not all(self.database.contains(where(self.contest_site) == handle) for handle in self.handle_rank_dict):
            logging.error('Some provided handle(s) are not in the database')
            quit(1)

        # Get all the details of the participants from the provided handles
        participants = self.database.search(where(self.contest_site).test(lambda x: x in self.handle_rank_dict))

        rating_list = [x[db.RATING] for x in participants]
        vol_list = [x[db.VOLATILITY] for x in participants]

        self.N = len(self.handle_rank_dict)
        self.Cf = elo.Cf(rating_list, vol_list, self.N)
        self.Rb_Vb_list = list(zip(rating_list, vol_list))

    @staticmethod
    def _decay_player(player_dict: dict) -> dict:
        """
        Reduces ratings by 10% for those who have competed at least once
        but have not taken part in the past 5 contests
        :param player_dict: dict with all details of a player
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

    def process_competition(self) -> None:

        rows = self.database.all()
        for row in rows:
            if self.contest_site in row and row[self.contest_site] in self.handle_rank_dict:
                handle = row[self.contest_site]
                actual_rank = self.handle_rank_dict[handle]
                new_data = self._update_player(row, actual_rank)
            else:
                new_data = self._decay_player(row)
            row.update(new_data)
        self.database.write_back(rows)


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
            open(rank_file).close()
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
    database_obj = TinyDB(db.DB_FILE)
    rank_file_obj = open(rank_file_path)
    rp = RatingProcessor(database_obj, rank_file_obj, contest_site_str)
    database_obj.close()
