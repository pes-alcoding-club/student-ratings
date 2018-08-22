# Student Ratings
## Alcoding Club, PES University

Alcoding Club of [PES University](https://pes.edu/) maintains ratings of its students who are active in [competitive programming](https://en.wikipedia.org/wiki/Competitive_programming). This repository contains the ratings and the code which generates it.


## Purpose
An intra-college rating is maintained so that the club can identify good coders.  The club will group these students and help them improve at competitive programming by organizing meet-ups, providing resources, arranging contests and develop a coding community in the University.


## Ratings
The ratings are calculated by students' performances in [specified contests](database/README.md).

### Mechanism
A [rank list](database/contest_ranks) of registered students is generated at the end of each contest. A rating is computed from the rank list, which indicates their relative performance. The implementation is almost the same as [Codechef's Rating Mechanism](https://www.codechef.com/ratings) which is a modified version of [Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system). To avoid students from [protecting their ratings](https://en.wikipedia.org/wiki/Elo_rating_system#Game_activity_versus_protecting_one's_rating) and encourage participation, a decay rule is also added which decrements a student's rating by 10% if she does not take part in 5 consecutive contests.


### Verification
The [code that generates the rating](ratings/processor.py) is open. Along with that we have provided [a script with which you can verify](executor.sh) that the displayed ratings are correct. This script resets all students' ratings, and computes the ratings after all the contest ranks are considered. You may [report an issue](https://github.com/varunvora/alcoding/issues) if you find any discrepancy.

## Calendar
Alcoding Club maintains a [Google calendar for competitive programming](https://calendar.google.com/calendar?cid=N3RsZGt1dXEwcW1mOW9ub2Jxb3ByZ2Z1cDRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ). Contests that are marked as "Rated" will be considered for these ratings. 
## Contribute
This project is still very small so there are no strict guidelines for contribution. For now we are following [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).

You can [report an issue](https://github.com/varunvora/alcoding/issues) if you find a bug or any other change you would like to make. You may also make a [pull request](https://github.com/varunvora/alcoding/pulls). Be sure to clearly document and describe any issues or changes.

## FAQ

1. How can I improve my rating?

    The only way you can improve your rating is by consistently scoring more than those who are rated higher than you.
2. Which contests are taken into account for rating?

    Contests in ['Competitive Programming PESU' Calendar](https://calendar.google.com/calendar?cid=N3RsZGt1dXEwcW1mOW9ub2Jxb3ByZ2Z1cDRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ) that are marked as "Rated" are considered for ratings.
 
   
