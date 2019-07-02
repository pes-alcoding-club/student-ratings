import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, where
from database.db_tools import DB_FILE, HACKEREARTH
import logging

# 0 - event_id
# 1 - page number
leaderboard_base_url = 'https://www.hackerearth.com/AJAX/feed/newsfeed/icpc-leaderboard/event/{0}/{1}/'


def get_handles(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    '''
    <div class="inline-block less-margin-left hof-user-info">
        <div class="no-color hover-link weight-600"> Gennady Korotkevich </div>
        <div class="gray-text body-font-small hover-link">gennady</div>
    </div>
    '''

    handles = list(map(lambda d: d.find_all('div')[1].text, soup.select('div.hof-user-info')))
    return handles


def get_leaderboard(event_id):
    page_num = 1
    leaderboard = []
    
    while True:
        r = requests.get(leaderboard_base_url.format(event_id, page_num))
        handles = get_handles(r.text)
        # url returns last page for page_num greater than last page number
        if leaderboard[-len(handles):] == handles:
            break
        
        leaderboard.extend(handles)
        page_num += 1
        logging.info(page_num)

    return leaderboard


if __name__ == "__main__":
    logging.basicConfig(level='INFO')
    event_id = '736148'
    leaderboard = get_leaderboard(event_id)
    print(*leaderboard, sep='\n')

"""Uncomment to output mapped PES handles only
    with TinyDB(DB_FILE) as database:
        pes_hackerearth_users = {x[HACKEREARTH] for x in database.search(where(HACKEREARTH))}

    pes_leaderboard = filter(pes_hackerearth_users.__contains__, leaderboard)
    print(*pes_leaderboard, sep='\n')
"""


