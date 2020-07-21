import requests
import sys
import os
from bs4 import BeautifulSoup
from tinydb import TinyDB, where
from database.db_tools import DB_FILE, HACKEREARTH
from utils import log

# 0 - event_id
# 1 - page number
API = 'https://www.hackerearth.com/AJAX/feed/newsfeed/icpc-leaderboard/event/{0}/{1}/'
leaderboard_base_url = 'https://www.hackerearth.com/challenges/competitive/{}/leaderboard/'

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

        handles = get_handles(requests.get(API.format(event_id, page_num)).text)
        # url returns last page for page_num greater than last page number
        if leaderboard[-len(handles):] == handles:
            break
        
        leaderboard.extend(handles)
        log.debug(f'Handles retrieved for page {page_num}')
        page_num += 1

    return leaderboard

def get_contest_IDs(contest_codes):
    contest_IDs = dict()
    for contest_code in contest_codes:
        # Gets the ICPC contest ID from the url; We use this ID to send the request
        contest_IDs[contest_code] = BeautifulSoup(requests.get(leaderboard_base_url.format(contest_code)).text, 'html.parser').find('div', class_='event-id').text

    return contest_IDs

def scrape(contest_codes):
    contest_IDs = get_contest_IDs(contest_codes)
    leaderboards = []
    for contest in contest_IDs:
        log.info(f'HackerEarth contest {contest}:')
        leaderboard = get_leaderboard(contest_IDs[contest])
        leaderboards.append(leaderboard)
    return leaderboards

"""Uncomment to output mapped PES handles only
    with TinyDB(DB_FILE) as database:
        pes_hackerearth_users = {x[HACKEREARTH] for x in database.search(where(HACKEREARTH))}

    pes_leaderboard = filter(pes_hackerearth_users.__contains__, leaderboard)
    print(*pes_leaderboard, sep='\n')
"""


