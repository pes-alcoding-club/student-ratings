import csv
import requests
import logging
import re
from database import db_tools as db
from tinydb import TinyDB, where
from ratings import elo

logging.basicConfig(level='INFO')

profile_base_url = {
    'codechef': 'https://www.codechef.com/users/',
    'hackerearth': 'https://www.hackerearth.com/@',
    'hackerrank': 'https://www.hackerrank.com/',
    'codeforces': 'https://codeforces.com/profile/'
}

sess = requests.Session()
sess.headers.update({'User-Agent': 'Mozilla/5.0'})

missing_handles, incorrect_handles, incorrect_usns = [], [], []

def verify_handles(row_dict, handles):
    for site, handle in handles.items():
        if handle == '':
            missing_handles.append((row_dict['name'], site))
            continue
        if site not in ['kickstart', 'codejam']:
            handle = handle.strip()
            while True:
                try:
                    r = sess.get(profile_base_url[site] + handle, timeout=5)
                    break
                except:
                    pass

            if r.ok:
                row_dict[site] = handle
            else:
                incorrect_handles.append((row_dict['name'], site, handle))

def verify_usn(usn):
    if re.match(r'(01FB(15|16|17)ECS[0-9]{3})|(PES120(17|18)[0-9]{5})', usn, re.IGNORECASE) == None:
        incorrect_usns.append(usn)
        return False
    return True

database = TinyDB(db.DB_FILE)

with open('list.csv') as fp:
    reader = csv.reader(fp)
    next(reader)

    row_count = 1
    for row in reader:
        row_dict = {
            'name': row[3],
            'email': row[1],
            'usn': row[2]
        }
        if not verify_usn(row_dict['usn']):
            continue
        handles = {
            'codejam': row[5],
            'kickstart': row[6],
            'codechef': row[7],
            'hackerearth': row[8],
            'hackerrank': row[9],
            'codeforces': row[10],
        }
        verify_handles(row_dict, handles)

        if database.get(where('usn') == row_dict['usn']) == None:
            row_dict[db.RATING] = elo.DEFAULT_RATING
            row_dict[db.VOLATILITY] = elo.DEFAULT_VOLATILITY
            row_dict[db.BEST] = elo.DEFAULT_RATING
            row_dict[db.TIMES_PLAYED] = 0
            row_dict[db.LAST_FIVE] = 5
        database.upsert(row_dict, where('usn') == row_dict['usn'])

        logging.info('%d row(s) processed', row_count)
        row_count += 1

database.close()

print('incorrect_usns', incorrect_usns)
print('missing_handles:', missing_handles)
print('incorrect_handles:', incorrect_handles)


