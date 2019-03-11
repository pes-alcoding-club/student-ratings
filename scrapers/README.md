### Scrapers

This module contains scripts responsible for scraping contest pages.

#### Description

1. map_handle_to_usn.py: After a contest is scraped this one maps the handles to its respective USN so that even if the handle changes in the future, it does not affect the rank.
1. codejam.py: Scraper for scoreboard for Google Codejam for its new interface that was launched in 2018. 
2. codechef.py: Scraper for Codechef contests. This one uses regular expression to fetch the score board from the raw web page.
3. hackearth.py: Scraper for Hackerearth contests. This scrapes the entire global leaderboard without any filter.

#### Usage

1. Modify the scoreboard url in google.py, Run it, make necessary changes in the scoreboard(Change default view to 20, so on...), Press enter to continue.
2. Copy the raw scoreboard from codechef to a file say `codechef-contest-year.in` and run `python3 codechef.py codechef-contest-year.in` 
