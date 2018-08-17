import logging
from ratings import elo

# this should be in db folder
JSON_RATING = 'rating'
JSON_VOL = 'volatility'
JSON_TIMES = 'timesPlayed'
JSON_BEST = 'best'


class RatingProcessor:

    def __init__(self, player_dict_list):
        """
        Takes a list of student
        """
        try:
            assert isinstance(player_dict_list, list)
            assert all(isinstance(x, dict) for x in player_dict_list)
            assert all(JSON_RATING in x for x in player_dict_list)
            assert all(JSON_VOL in x for x in player_dict_list)
            assert all(JSON_TIMES in x for x in player_dict_list)
            assert all(JSON_BEST in x for x in player_dict_list)

        except AssertionError:
            logging.error('Invalid input to RatingProcessor')
        self.N = None
        self.Cf = None
        self.Rb_Vb_list = None

    def process_player(self, player_dict, actual_rank):

        old_rating = player_dict[JSON_RATING]
        old_volatility = player_dict[JSON_VOL]
        times_played = player_dict[JSON_TIMES]
        old_best = player_dict[JSON_BEST]

        new_rating, new_volatility = elo.process(
            old_rating, old_volatility, times_played, actual_rank, self.Rb_Vb_list, self.N, self.Cf)

        player_dict[JSON_RATING] = new_rating
        player_dict[JSON_VOL] = new_volatility
        player_dict[JSON_TIMES] = times_played + 1
        player_dict[JSON_BEST] = max(old_best, new_rating)
