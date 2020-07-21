# Student Ratings
## Alcoding Club, PES University

[![Build Status](https://travis-ci.com/varunvora/alcoding.svg?branch=master)](https://travis-ci.com/varunvora/alcoding)

Alcoding Club of [PES University](https://pes.edu/) maintains ratings of its students who are active in [competitive programming](https://en.wikipedia.org/wiki/Competitive_programming). This repository contains the ratings and the code that generates it.

## Purpose
An intra-college rating is maintained to aid the club in identifying good coders. The club aims to help these students improve their competitive programming skills by organizing meet-ups, providing resources, arranging contests and developing a coding community in the University.


## Ratings
The ratings are calculated using students' performances in [specified contests](database/README.md).

### Mechanism
A [rank list](database/contest_ranks) of registered students is generated at the end of each contest. A rating is computed from the rank list, which indicates their relative performance. The implementation is very similar to [Codechef's Rating Mechanism](https://www.codechef.com/ratings) which is a modified version of the [Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system). To prevent students from [protecting their ratings](https://en.wikipedia.org/wiki/Elo_rating_system#Game_activity_versus_protecting_one's_rating) and encourage participation, a decay rule, which decrements a student's rating by 1% if they do not take part in 5 consecutive rated contests, is also added.


### Verification
The [code that generates the rating](ratings/processor.py) is open. Further, we also provide [a method with which you can verify](run.py) the displayed ratings. This method resets all students' ratings, and recomputes the ratings of every student after considering all contest ranks. Please do [report an issue](https://github.com/pes-alcoding-club/student-ratings/issues) if you find any discrepancy.

## Calendar
Alcoding Club maintains a [Google Calendar for competitive programming](https://calendar.google.com/calendar?cid=N3RsZGt1dXEwcW1mOW9ub2Jxb3ByZ2Z1cDRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ). Contests that are marked "Rated" will be considered for these ratings. 
## Contribute
At the moment, there are no strict guidelines for contribution. As a standard, we follow the [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).

Feel free to [report an issue](https://github.com/pes-alcoding-club/student-ratings/issues) if you find a bug, or have any other change you would like to see. You may also create a [pull request](https://github.com/pes-alcoding-club/student-ratings/pulls). It would be helpful if you use [our Github labels](https://github.com/pes-alcoding-club/student-ratings/labels) for all issues and pull requests. Be sure to clearly document and describe any issues or changes.

## FAQ

1. How can I improve my rating?

    The only way you can improve your rating is by consistently scoring more than those who are rated higher than you.
1. Which contests have been considered for these ratings?

    The contests considered for ratings have been listed [here](database/README.md). This list will be updated after calculating the ratings for each contest.
1. Which contests are taken into account for rating?

    Contests in ['Competitive Programming PESU' Calendar](https://calendar.google.com/calendar?cid=N3RsZGt1dXEwcW1mOW9ub2Jxb3ByZ2Z1cDRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ) are considered for ratings.
1. How can I tell whether these ratings are legitimate?

    You can verify the ratings yourself by calling the [make_scoreboard] function in [run.py](run.py). It resets all students' ratings to default values and recomputes it for all contests so far in chronological order. 
   
1. How can I make a scoreboard for a few particular contests?
    Firstly, clone this repository.
    Create your own [contest_names_file.in](database/contest_names_file.in) and add the contest names in the format [platform]-[month]-[contest_code]. In [run.py](run.py), change the [contest_names_file_path] variable's value to your file's path.
    Now call the [make_scoreboard] function in [run.py](run.py) with the required parameters and check [scoreboard.csv](scoreboard.csv).