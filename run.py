import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import os
sys.path.append( # Add absolute path of utils to sys.path
    os.path.join( os.path.dirname( os.path.realpath( __file__ )), 
    '../student-ratings' ))
from scrapers import codechef, hackerearth
from database import db_tools as tools
from ratings import processor
from pathlib import Path
from collections import defaultdict
from utils import log

PATH_TO_RANK_FILES = 'database/contest_ranks/' # Change this path to 'database/[YOUR_CUSTOM_RANKS_DIR]' to calculate ratings for only a few contests
contest_names_file_path = 'database/contest_names_file.in' # Change this path to 'database/[YOUR_CUSTOM_CONTEST_NAMES_FILE.in]' and add required (supported) contests to calculate ratings for only those
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
months = ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec']

# Objects of this class are made for each contest; This allows the association of name, website, etc to that particular contest
class contest_details():
    def __init__(self, url):
        self.website = str(url[0].split('.')[1]) # Fetch the platform name
        self.contest_code = str(url[-1])
        self.file_name = self.make_file_name()

    def make_file_name(self):
        if self.website == 'codechef':
            if self.contest_code[0:5] == 'LTIME':
                # Specific formula to determine month and year for Lunchtime based on numeric ID
                month, year = months[(int(self.contest_code[5:]) + 4) % 12], int((int(self.contest_code[5:]) + 5) / 12) + 13 
                return f'codechef-{month}-lunchtime-{year}.in'
                # Specific formula to determine month and year for Cookoff based on numeric ID
            elif self.contest_code[0:4]=="COOK":
                month, year = months[(int(self.contest_code[4:]) + 6) % 12], int((int(self.contest_code[4:]) + 7) / 12) + 10
                return f'codechef-{month}-cookoff-{year}.in'
            else:
                month = self.contest_code[:-2].lower()
                return f'codechef-{month}-long-{self.contest_code[-2:]}.in'
        elif self.website == 'hackerearth':
            return f'hackerearth-{self.contest_code}.in'
    
    def set_leaderboard(self, leaderboard):
        self.leaderboard = leaderboard


def get_calendar_events(DAYS):
    #This block of code is to allow OAuth
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    """ Call the Calendar API
        Z indicates UTC time, as Google requires
        the input timezones to be consistent """
    now = datetime.utcnow().isoformat() + 'Z'                                                     
    tmin = (datetime.utcnow() - timedelta(days=DAYS)).isoformat() + 'Z'
    response = service.events().list(calendarId='7tldkuuq0qmf9onobqoprgfup4@group.calendar.google.com', timeMin=tmin,
                                        timeMax=now, singleEvents=True,
                                        orderBy='startTime').execute()

    calendar_response = response.get('items', [])
    return calendar_response


def get_all_contests(DAYS):
    calendar_response = get_calendar_events(DAYS) # Gets all contest event in the last [DAYS] days
    contests = defaultdict(list)
    contest_names_file = open(contest_names_file_path, 'r+') # Contains list of all contests scraped till now
    existing_contests = list(contest_names_file.read().split('\n'))
    if not calendar_response:
        log.error('No upcoming contests found.')
        contest_names_file.close()
        return calendar_response
    else:
        for event in calendar_response:
            try:
                url = event['location'].replace('https://', '').split('/') # Remove the https and make the parts of the url a list
            except:
                log.error('The contest {} does not have an associated website and is hence ignored.'.format(event['summary']))
                continue
            try:
                url.remove('') # To remove any unexpected blank items caused by a trailing slash
            except:
                pass
            
            contest = contest_details(url) # Create a contest_details object for the contest
            if contest.website not in ['codechef', 'hackerearth']: # Only codechef and hackerearth scrapers are compatible as of now
                continue
            if contest.file_name not in existing_contests: # Checks whether the contest has already been scraped, if not writes it to scraped contests
                contest_names_file.write(contest.file_name+'\n')
                contests[contest.website].append(contest)
            else:
                log.warn(f'{contest.file_name} already exists, ignoring; To re-scrape, delete the file and remove this entry.')
 
        contest_names_file.close()
        return contests


""" The scrapers take in a list of contest id's at a go to avoid the overhead of repeatedly calling it. This means that the output
    leaderboards have to be reverse mapped back to the contest_details objects; Since they are in a list and the order is preserved,
    we use the index of the leaderboard and map it to the object of the same index """
def scrape(DAYS=30):
    contests = get_all_contests(DAYS) # Returns a list of contest_details objects for each contest event in the calendar
    if contests: # If contests have been found
        leaderboards = codechef.scrape(list(contest.contest_code for contest in contests['codechef']))
        assert len(leaderboards) == len(contests['codechef']) # Make sure the number of leaderboards is the same as number of contests
        for i in range(len(leaderboards)):
            contests['codechef'][i].set_leaderboard(leaderboards[i])

        leaderboards = hackerearth.scrape(list(contest.contest_code for contest in contests['hackerearth']))
        assert len(leaderboards) == len(contests['hackerearth']) # Make sure the number of leaderboards is the same as number of contests
        for i in range(len(leaderboards)):
            contests['hackerearth'][i].set_leaderboard(leaderboards[i])
    
    else:
        return
    
    for platform in contests:
        for contest in contests[platform]:
            file_path = PATH_TO_RANK_FILES + contest.file_name
            with open (file_path, 'w+') as rank_file:
                for rank in contest.leaderboard:
                    rank_file.write(rank + '\n')
            log.info('Wrote to {file_path}')


def recalculate(clean=False): # Recalculates the ratings from ground-up; This is to ensure integrity and to allow for later joinees
    contest_names_file = open(contest_names_file_path, 'r')
    contest_names = list(contest_names_file.read().split('\n'))
    try:
        contest_names.remove('') # Removes trailing newline in case the input file had it
    except:
        pass   
    log.info('Built list of files to process')
    for contest in contest_names:
        if clean:
            """ Removes handles that couldn't be mapped to a USN
                Usually required in a contest where we couldn't obtain handles of only required students, such as HackerEarth """
            tools.remove_unmapped_handles_from_rank_file(f'{PATH_TO_RANK_FILES}{contest}') 
        processor.process(f'{PATH_TO_RANK_FILES}{contest}') # Call the processor for each contest
        log.info(f'Processed contest: {contest}')
    tools.export_to_csv()
    tools.prettify()
    contest_names_file.close()


def make_scoreboard(map_USN=True, clean=False):
    tools.reset_database()
    if map_USN:
        tools.map_username_to_usn()
    recalculate(clean)

''' [DAYS]: No of days to fetch calendar events from
    [map_USN]: Whether to map usernames to USNs
    [clean]: Whether to remove unmapped handles '''
def execute(DAYS=30, map_USN=True, clean=False): # 
    scrape(DAYS=DAYS)
    make_scoreboard(map_USN=map_USN, clean=clean)


""" Uncomment one of the two lines depending on requirement, or call your desired function yourself """

# execute(clean=True)
# make_scoreboard(map_USN=True, clean=True)