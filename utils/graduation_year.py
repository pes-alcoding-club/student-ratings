import re
import logging
from tinydb import TinyDB, where, Query
from database.db_tools import DB_FILE

USN_OF_2018_GRAD = re.compile(r'(^01FB14.*)|(^1PI*)', re.IGNORECASE)
USN_OF_2019_GRAD = re.compile(r'^01FB15.*', re.IGNORECASE)
USN_OF_2020_GRAD = re.compile(r'^01FB1(6|7).*', re.IGNORECASE) # one guy with use 01fb17.. graduates in 2020
USN_OF_2021_GRAD = re.compile(r'^PES12017.*', re.IGNORECASE)


def get_year_from_usn(usn: str) -> int:
    year = 0
    if USN_OF_2019_GRAD.match(usn):
        year = 2019
    elif USN_OF_2020_GRAD.match(usn):
        year = 2020
    elif USN_OF_2021_GRAD.match(usn):
        year = 2021
    else:
        logging.debug(f"{usn} did not match with any year")
    logging.info(f"{usn} matched with {year}")
    return year


with TinyDB(DB_FILE) as database:
    Player = Query()

    print(len(database.update({'year': 0})))
    print(len(database.upsert({'year': 2018}, where('usn').matches(USN_OF_2018_GRAD))))
    print(len(database.upsert({'year': 2019}, where('usn').matches(USN_OF_2019_GRAD))))
    print(len(database.upsert({'year': 2020}, where('usn').matches(USN_OF_2020_GRAD))))
    print(len(database.upsert({'year': 2021}, where('usn').matches(USN_OF_2021_GRAD))))

    items = database.search(Player.year == 0)
    for item in items:
        print(item)
    print(len(items))
