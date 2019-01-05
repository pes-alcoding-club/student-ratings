### Scrapers

This module contains scripts responsible for scraping contest pages.

#### Description

1. codejam.py: Scraper for scoreboard for Google Codejam for its new interface that was launched in 2018. 
2. codechef.py: Scraper for Codechef contests. This one uses regular expression to fetch the score board from the raw web page.

#### Usage

1. Modify the first few variables in the file and run `python3 codejam.py`. Ensure you have selenium driver from Chrome.
2. Copy the raw scoreboard from codechef to a file say `codechef-contest-year.in` and run `python3 codechef.py codechef-contest-year.in` 
