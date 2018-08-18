import logging
from database import json


def read_database():
    player_dict_dict = []

    try:
        assert isinstance(player_dict_dict, list)
        assert all(isinstance(x, dict) for x in player_dict_dict)
        assert all(json.RATING in x for x in player_dict_dict)
        assert all(json.VOLATILITY in x for x in player_dict_dict)
        assert all(json.TIMES_PLAYED in x for x in player_dict_dict)
        assert all(json.BEST in x for x in player_dict_dict)
    except AssertionError:
        logging.error('Invalid input to RatingProcessor')


def write_database(player_dict_dict):
    pass
