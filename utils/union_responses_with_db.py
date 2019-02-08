import csv
import requests
import logging
import re
from database import db_tools as db
from tinydb import TinyDB, where
from ratings import elo

logging.basicConfig(level='INFO')

# The following fields may need to be adjusted before running the script
MIN_VALID_GRAD_YEAR = 2019
MAX_VALID_GRAD_YEAR = 2021
VALID_USN_PATTERN = re.compile(r'(01FB1(5|6|7)\w{3}\d{3})|(PES12017\d{5})', re.IGNORECASE)

profile_base_url = {
    db.CODECHEF: 'https://www.codechef.com/users/',
    db.HACKEREARTH: 'https://www.hackerearth.com/@',
    db.HACKERRANK: 'https://www.hackerrank.com/',
    db.CODEFORCES: 'https://codeforces.com/profile/'
}

sess = requests.Session()
sess.headers.update({'User-Agent': 'Mozilla/5.0'})

incorrect_handles, incorrect_usns = [], []


def get_validated_data(csv_row) -> dict:
    details_dict = {
        db.EMAIL: row[1],
        db.USN: row[2],
        db.NAME: row[3],
        db.YEAR: int(row[4])}
    handles_dict = {
        db.CODEJAM: row[5],
        db.KICKSTART: row[6],
        db.CODECHEF: row[7],
        db.HACKEREARTH: row[8],
        db.HACKERRANK: row[9],
        db.CODEFORCES: row[10]}

    def is_not_empty_str(candidate_str: str) -> bool:
        return candidate_str.strip() != ""

    def is_valid_year(year_of_graduation: int) -> bool:
        return MIN_VALID_GRAD_YEAR <= year_of_graduation <= MAX_VALID_GRAD_YEAR

    def is_valid_usn(usn: str) -> bool:
        if VALID_USN_PATTERN.match(usn) is None:
            incorrect_usns.append(csv_row[db.USN])
            return False
        return True

    def is_valid_handle(handle_str: str, site_str: str) -> bool:
        if is_not_empty_str(handle_str) and\
                len(handle_str.split()) == 1 and\
                site_str in [db.CODECHEF, db.CODEFORCES, db.HACKEREARTH, db.HACKERRANK]:
            while True:
                try:
                    r = sess.get(profile_base_url[site_str] + handle_str, timeout=5)
                    break
                except:
                    pass
            if r.ok:  # if this is saying `ok` for handles with spaces then querying the website is no use
                return True
        incorrect_handles.append((handle_str, details_dict[db.NAME], site_str))
        return False

    validated_data_dict = dict()
    if is_valid_usn(details_dict[db.USN])\
            and is_not_empty_str(details_dict[db.NAME])\
            and is_not_empty_str(details_dict[db.EMAIL])\
            and is_valid_year(details_dict[db.YEAR]):
        validated_data_dict[db.USN] = details_dict[db.USN].strip().upper()
        validated_data_dict[db.NAME] = details_dict[db.NAME].strip().title()
        validated_data_dict[db.EMAIL] = details_dict[db.EMAIL].strip().lower()
        validated_data_dict[db.YEAR] = int(details_dict[db.YEAR])
        for site, handle in handles_dict.items():
            if is_valid_handle(site, handle):
                validated_data_dict[site] = handle
    return validated_data_dict


with TinyDB(db.DB_FILE) as database:
    with open('list.csv') as fp:
        reader = csv.reader(fp)
        next(reader)
        for row_count, row in enumerate(reader, start=1):
            csv_row_dict = get_validated_data(row)
            if database.get(where(db.USN) == csv_row_dict[db.USN]) is None:
                csv_row_dict[db.RATING] = elo.DEFAULT_RATING
                csv_row_dict[db.VOLATILITY] = elo.DEFAULT_VOLATILITY
                csv_row_dict[db.BEST] = elo.DEFAULT_RATING
                csv_row_dict[db.TIMES_PLAYED] = 0
                csv_row_dict[db.LAST_FIVE] = 5
            database.upsert(csv_row_dict, where(db.USN) == csv_row_dict[db.USN])
            logging.info(f'{row_count} row(s) processed')

logging.debug(f'incorrect_usns:\n{incorrect_usns}')
logging.debug(f'incorrect_handles:\n{incorrect_handles}')
