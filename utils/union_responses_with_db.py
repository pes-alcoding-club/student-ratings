import csv
import requests
import logging
from datetime import datetime
from database import db_tools as db
from tinydb import TinyDB, where
from ratings import elo

logging.basicConfig(level='DEBUG')

profile_base_url = {
    db.CODECHEF: 'https://www.codechef.com/users/',
    db.HACKEREARTH: 'https://www.hackerearth.com/@',
    db.HACKERRANK: 'https://www.hackerrank.com/',
    db.CODEFORCES: 'https://codeforces.com/profile/'
}

sess = requests.Session()
sess.headers.update({'User-Agent': 'Mozilla/5.0'})

incorrect_handles, incorrect_usns = [], []
FORM_RESPONSES_CSV_FILE = 'list.csv'


def get_validated_data(csv_row) -> dict:
    details_dict = {
        db.EMAIL: csv_row[1].strip(),
        db.USN: csv_row[2].strip(),
        db.NAME: csv_row[3].strip(),
        db.YEAR: int(csv_row[4].strip())}
    handles_dict = {
        db.CODEJAM: csv_row[5].strip(),
        db.KICKSTART: csv_row[6].strip(),
        db.CODECHEF: csv_row[7].strip(),
        db.HACKEREARTH: csv_row[8].strip(),
        db.HACKERRANK: csv_row[9].strip(),
        db.CODEFORCES: csv_row[10].strip()}

    def is_not_empty_str(candidate_str: str) -> bool:
        return candidate_str.strip() != ""

    def is_valid_year(year_of_graduation: int) -> bool:
        return db.VALID_MIN_YEAR <= year_of_graduation <= db.VALID_MAX_YEAR

    def is_valid_usn(usn: str) -> bool:
        if db.VALID_USN_REGEX.match(usn) is None:
            incorrect_usns.append(details_dict[db.USN])
            return False
        return True

    def is_valid_handle(handle_str: str, site_str: str) -> bool:
        if is_not_empty_str(handle_str) and\
                len(handle_str.split()) == 1:
            if site_str in [db.CODECHEF, db.CODEFORCES, db.HACKEREARTH, db.HACKERRANK]:
                while True:
                    try:
                        r = sess.get(profile_base_url[site_str] + handle_str, timeout=5)
                        break
                    except:
                        pass
                if r.ok:
                    return True
                else:
                    incorrect_handles.append((handle_str, details_dict[db.NAME], site_str))
                    return False
            else:
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
            if is_valid_handle(handle, site):
                validated_data_dict[site] = handle
    return validated_data_dict


if __name__ == "__main__":
    LAST_UPDATED = datetime(2019, 5, 18)
    # last update before the current run. See metadata sheet in response form.
    with TinyDB(db.DB_FILE) as database:
        with open(FORM_RESPONSES_CSV_FILE) as fp:
            reader = csv.reader(fp)
            next(reader)
            for row_count, row in enumerate(reader, start=1):
                if datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S") < LAST_UPDATED:
                    continue
                csv_row_dict = get_validated_data(row)
                if not csv_row_dict:
                    continue
                if database.get(where(db.USN) == csv_row_dict[db.USN]) is None:
                    csv_row_dict[db.RATING] = elo.DEFAULT_RATING
                    csv_row_dict[db.VOLATILITY] = elo.DEFAULT_VOLATILITY
                    csv_row_dict[db.BEST] = elo.DEFAULT_RATING
                    csv_row_dict[db.TIMES_PLAYED] = 0
                    csv_row_dict[db.LAST_FIVE] = 5
                database.upsert(csv_row_dict, where(db.USN) == csv_row_dict[db.USN])
                logging.info(f'{row_count} row(s) processed')

    logging.debug(f'incorrect_usns ({len(incorrect_usns)}) :\n{incorrect_usns}')
    logging.debug(f'incorrect_handles ({len(incorrect_handles)}):\n{incorrect_handles}')
