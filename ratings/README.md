### Ratings

This module contains the implementation of the rating mechanism. View the [description of the repository for more details](../README.md)

#### Description
1. elo.py: Implementations of functions of ELO rating system as described by Codechef.
2. rating_processor.py: Updates the database for every new contest
3. test_ratings.py: Unittests for this module

#### Usage
1. To update the ratings after a contest, run rating_processor.py as follows
`python3 processor.py rank_file_path contest_site_str`