import csv
import logging
import re
from database import db_tools as db
from tinydb import TinyDB, where
from ratings import elo

logging.basicConfig(level='DEBUG')

incorrect_handles, incorrect_usns = [], []


def get_validated_data(csv_row) -> dict:
    details_dict = {
        db.EMAIL: csv_row[1].strip(),
        db.USN: csv_row[2].strip(),
        db.NAME: csv_row[3].strip(),
        db.YEAR: int(csv_row[4].split()[-1])}
    handles_dict = {
        db.CODEJAM: csv_row[6].strip()}

    def is_not_empty_str(candidate_str: str) -> bool:
        return candidate_str.strip() != ""

    def is_valid_year(year_of_graduation: int) -> bool:
        return db.VALID_MIN_YEAR <= year_of_graduation <= db.VALID_MAX_YEAR

    def is_valid_usn(usn: str) -> bool:
        if db.VALID_USN_REGEX.match(usn) is None:
            incorrect_usns.append(details_dict[db.USN])
            return False
        return True

    def is_valid_handle(handle: str) -> bool:
        is_valid = is_not_empty_str(handle) and len(handle.split()) == 1 and re.match(r"^[^\@\s]*$", handle)
        if handle and not is_valid:
            incorrect_handles.append(handle)
        return is_valid

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
            if is_valid_handle(handle):
                validated_data_dict[site] = handle
    return validated_data_dict


if __name__ == "__main__":
    count = 0
    with TinyDB("../" + db.DB_FILE) as database:
        with open('list.csv') as fp:
            reader = csv.reader(fp)
            next(reader)
            for row_count, row in enumerate(reader, start=1):
                csv_row_dict = get_validated_data(row)
                if not csv_row_dict:
                    continue
                if database.get(where(db.USN) == csv_row_dict[db.USN]) is None:
                    csv_row_dict[db.RATING] = elo.DEFAULT_RATING
                    csv_row_dict[db.VOLATILITY] = elo.DEFAULT_VOLATILITY
                    csv_row_dict[db.BEST] = elo.DEFAULT_RATING
                    csv_row_dict[db.TIMES_PLAYED] = 0
                    csv_row_dict[db.LAST_FIVE] = 5
                    count += 1
                    database.upsert(csv_row_dict, where(db.USN) == csv_row_dict[db.USN])
                else:
                    doc = database.get(where(db.USN) == csv_row_dict[db.USN])
                    csv_row_dict[db.EMAIL] = doc[db.EMAIL]  # keep the email that is already in the database
                    if doc[db.NAME].lower() != csv_row_dict[db.NAME].lower() and\
                            " " in doc[db.NAME] and " " not in csv_row_dict[db.NAME]\
                            or len(doc[db.NAME]) > len(csv_row_dict[db.NAME]):
                        logging.info(f'Choosing "{doc[db.NAME]}" over "{csv_row_dict[db.NAME]}"')
                        csv_row_dict[db.NAME] = doc[db.NAME].title()
                    if db.CODEJAM in doc:  # keep the codejam handle that is already in the database
                        if db.CODEJAM in csv_row_dict:
                            if csv_row_dict[db.CODEJAM] != doc[db.CODEJAM]:
                                logging.info('-'*20)
                                logging.info(doc)
                                logging.info(csv_row_dict)
                                csv_row_dict[db.CODEJAM] = doc[db.CODEJAM]
                                logging.info('-' * 20)
                    count += 1
                    database.upsert(csv_row_dict, where(db.USN) == csv_row_dict[db.USN])
                logging.info(f'{row_count} row(s) processed')

    logging.info(f'total rows: {count}')
    logging.debug(f'incorrect_usns ({len(incorrect_usns)}) :\n{incorrect_usns}')
    logging.debug(f'incorrect_handles ({len(incorrect_handles)}):\n{incorrect_handles}')
