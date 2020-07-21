from collections import namedtuple
import random
from datetime import datetime
import sys
import os
from utils import selenium_utils, log

driver = selenium_utils.make_driver()  
load_all = selenium_utils.load_all(driver)
load = selenium_utils.load(driver)

name_class: str = "user-name"

division = namedtuple('division',['problems','scraped_scoreboard'])
divisions: dict = {'A':division(set(), list()),'B':division(set(), list())}


def get_problems(site):
    driver.get(site)
    log.info(f'Initialised website: {site}')
    problem_list = list(load(r'tbody', 'tag').text.split('\n'))[1::4]
    problems = set()
    for question in problem_list:
        problems.add(question)
    return problems

def get_rankings(site, contest_code):
    driver.get(site)
    log.info(f'Initialised website: {site}')
    total_pages = int(load_all(r'jump', 'class')[-1].text)
    scraped_scoreboard = []
    for page in range(total_pages):    
        names = load_all(name_class, 'class')
        scores = load_all(r"//td[@class='num']//div[not(@class) and (@title='' or not(@title))]", 'xpath')
        if contest_code[0:4] == "COOK":
            # For cook-off contests, there's an extra penalty provision, we need only the alternate elements.
            scores = scores[::2]            
            ''' Extract all time elements, remove semi-colons, convert to numeric type. 
                Smaller the time, the better. But score needs to be generated with left most digit being
                number of points, hence time's subtracted from 100000 to allow descending order of scores '''            
            times = list(100000-float(time.text.replace(":","")) for time in load_all(r'total-time', 'class'))
            # The score's added to the left of the time             
            scraped_scoreboard.extend(zip(
                [x.find_elements_by_tag_name("span")[-1].text for x in names],
                [float(scores[i].text.split()[0])*100000+times[i] for i in range(len(scores))]))        
        else:
            scraped_scoreboard.extend(zip(
                [x.find_elements_by_tag_name("span")[-1].text for x in names],
                [float(y.text.split()[0]) for y in scores]))                
        if page == total_pages-1: # Reached Last Page
            break    
        driver.get(site + f'&page={page+2}') # go to next page
    return scraped_scoreboard

def scrape(contest_codes):
    scoreboard_base_url:str = "https://www.codechef.com/rankings"
    site_url:str = "https://www.codechef.com"
    scoreboard_filter_query:str = "?filterBy=Institution%3DPES%20University&itemsPerPage=100&order=asc&sortBy=rank"
    leaderboards = []
    for contest_code in contest_codes:
        log.info(f'Codechef contest {contest_code}:')
        final_scoreboard:list=list()
        easy_points:int=100 # Points to add to division A participants assuming they can solve all easy div B problems

        if contest_code[0:4]=="COOK":
            easy_points=100000 # Initial value set to points per problem

        for Division in divisions: # Build the scraped scoreboard
            divisions[Division] = divisions[Division]._replace(problems = get_problems(f"{site_url}/{contest_code}{Division}"))
            divisions[Division] = divisions[Division]._replace(scraped_scoreboard = get_rankings(f"{scoreboard_base_url}/{contest_code}{Division}{scoreboard_filter_query}", contest_code))

        easy_points=len(divisions['B'].problems-divisions['A'].problems)*easy_points # Points to add to div-A participants
        for i in range(len(divisions['A'].scraped_scoreboard)): # Add easy points to all div-A participants
            divisions['A'].scraped_scoreboard[i]=divisions['A'].scraped_scoreboard[i][0],divisions['A'].scraped_scoreboard[i][1]+easy_points
            
        final_scoreboard.extend(divisions['A'].scraped_scoreboard)
        final_scoreboard.extend(divisions['B'].scraped_scoreboard) # Consolidate scoreboard
        final_scoreboard = sorted(final_scoreboard,key=lambda x:x[1],reverse=True) # Sort list in desc. order based on points. (username, points)

        if final_scoreboard: # If scoreboard's not empty
            rank_list = []
            if contest_code[0:5]=="LTIME" or contest_code[0:4]=="COOK": 
                rank_list = [x[0] for x in final_scoreboard]
            else: # Shared ranking possible for long contests.
                last_score = final_scoreboard[0][1]
                shared_rank = []
                for user in final_scoreboard:
                    if user[1] == last_score:
                        shared_rank.append(user[0])
                        if final_scoreboard.index(user) == len(final_scoreboard) - 1:
                            rank_list.append(' '.join(shared_rank))
                    else:
                        rank_list.append(' '.join(shared_rank))
                        shared_rank = []
                        last_score = user[1]
                        shared_rank.append(user[0])
            leaderboards.append(rank_list)
    return leaderboards
    driver.close()