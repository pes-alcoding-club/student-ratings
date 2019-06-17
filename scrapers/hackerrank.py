import requests
import logging

# Base Url - 0:contest_name, 1:participant_offset, 3:number of participants from offset (max 100)
base_url="https://www.hackerrank.com/rest/contests/{0}/leaderboard?offset={1}&limit={2}"  

"""
    Json response contains:
    - "models" -> list of participants with their "rank", "score", "time_taken", "hacker", "school"
    - "total" -> Total number of participants
    - "page" -> current page number
"""

def get_leaderboard(contest_name):
    scoreboard=[]
    response=requests.get(base_url.format(contest_name, 0, 100))
    if response.status_code==200:
        response_json=response.json()
        total_participants=response_json["total"]
        while len(scoreboard)<total_participants:
            for participant in response_json["models"]:
                scoreboard.append( ( participant["rank"], participant["hacker"] ) )
            logging.info( len( scoreboard ) )
            response=requests.get( base_url.format( contest_name, len(scoreboard), 100) )
            response_json=response.json()
        return scoreboard
    else:
        logging.error("Couldn't connect to scoreboard, please check URL/Contest name")

if __name__=="__main__":
    logging.basicConfig(level='INFO')
    contest_name="alcoding-summer-weekly-contest-2"
    scraped_scoreboard=get_leaderboard(contest_name)
    if scraped_scoreboard:
        lowest_so_far = int(scraped_scoreboard[0][0])
        for row in scraped_scoreboard:
            rank, handle = row
            rank = int(rank)
            if rank > lowest_so_far:
                print()
                lowest_so_far = rank
            print(handle, end=' ')