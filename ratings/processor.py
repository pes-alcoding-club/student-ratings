import sys
import logging
from ratings import elo
from database import db_tools as db


class RatingProcessor:
    """
    Uses database and rank file, and uses ELO to update the database with new ratings
    """

    def __init__(self, database, rank_file, contest_site):
        self.database = database
        handle_rank_dict = self.read_contest_ranks(rank_file)
        if len(handle_rank_dict) == 0:
            logging.error('Failed to load rankings, rank file empty')
            quit()

        srn_rank_dict = self.create_srn_rank_dict(handle_rank_dict, contest_site)
        self.N, self.Cf, self.Rb_Vb_list = self.get_contest_details(srn_rank_dict)
        self.process_competition(srn_rank_dict)
        self.decay_ratings(srn_rank_dict)

    @staticmethod
    def read_contest_ranks(file_path):
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

    def create_srn_rank_dict(self, handle_rank_dict, contest_site):
        handle_srn_dict = dict()

        for srn in self.database:
            if contest_site in self.database[srn]:
                handle = self.database[srn][contest_site]
                handle_srn_dict[handle] = srn

        unassigned_handles = set(handle_rank_dict.keys()) - set(handle_srn_dict.keys())
        if unassigned_handles:
            logging.error('Following handles are provided in rank list but not mapped to any player:\n{0}'.format(
                str(unassigned_handles)))
            quit()

        srn_rank_dict = dict()

        for handle in handle_rank_dict:  # Joining the 2 dictionaries using handle
            srn = handle_srn_dict[handle]
            rank = handle_rank_dict[handle]
            srn_rank_dict[srn] = rank

        return srn_rank_dict

    def get_contest_details(self, srn_rank_dict):
        rating_list = []
        vol_list = []

        for srn in srn_rank_dict:
            rating = self.database[srn][db.RATING]
            volatility = self.database[srn][db.VOLATILITY]
            rating_list.append(rating)
            vol_list.append(volatility)

        n = len(srn_rank_dict)
        competition_factor = elo.Cf(rating_list, vol_list, n)
        rating_vol_tup_list = list(zip(rating_list, vol_list))

        return n, competition_factor, rating_vol_tup_list

    def _process_player(self, player_dict, actual_rank):
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

    def process_competition(self, srn_rank_dict):
        for srn in srn_rank_dict:
            actual_rank = srn_rank_dict[srn]
            player_dict = self.database[srn]
            player_dict = self._process_player(player_dict, actual_rank)
            self.database[srn] = player_dict

        logging.info('Successfully processed competition')

    def decay_ratings(self, srn_rank_dict):
        """
        Reduces ratings by 10% for those who have competed at least once
        but have not taken part in the past 5 contests
        :param srn_rank_dict: dict with key as srn and value as rank
        :return: None
        """
        for srn in self.database:
            if srn not in srn_rank_dict:
                rating = self.database[srn][db.RATING]
                times_played = self.database[srn][db.TIMES_PLAYED]
                last_five = self.database[srn][db.LAST_FIVE] - 1

                if last_five == 0 and times_played > 0:
                    rating = rating * 0.9
                    last_five = 5

                self.database[srn][db.RATING] = rating
                self.database[srn][db.LAST_FIVE] = max(1, last_five)

        logging.info('Successfully decayed ratings')


def read_argv(argv_format_alert):
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
    old_db = db.read_database()
    rp = RatingProcessor(old_db, rank_file_path, contest_site_str)
    new_db = rp.database
    db.write_database(new_db)
    logging.info('Ratings processed successfully')
