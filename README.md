# Student Ratings
## Alcoding Club, PES University

Alcoding Club of [PES University](https://pes.edu/) maintains ratings of its students who are active in [competitive programming](https://en.wikipedia.org/wiki/Competitive_programming). This repository contains the ratings and the code which generates it.


## Purpose
An intra-college rating is maintained so that the club can identify good coders.  The club will group these students and help them improve at competitive programming by organizing meetups, providing resources, arranging contests and develop a coding community in the University.


## Ratings
The ratings are calculated by students' performances in specified contests.

### Mechanism
A rank list of registered students is generated at the end of each contest. A rating is computed from the rank list, which indicates their relative performance. The implementation is this as almost the same as [Codechef's Rating Mechanism](https://www.codechef.com/ratings) which is a modified version of [Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system). To avoid students from [protecting their ratings](https://en.wikipedia.org/wiki/Elo_rating_system#Game_activity_versus_protecting_one's_rating) and encourage participation, a decay rule is also added which decrements a student's rating by 10% if she does not take part in 5 consecutive contests.

### Improve Rating
The only way you can improve your rating is by consistently scoring more than those who are rated higher than you. The club will provide you with the necessary guidance and resources for the same.

### Verification
The code that generates the rating is open. Along with that we have provided a script with which you can verify that the displayed ratings are correct. This script resets all students' ratings, and computes the ratings after all the contest ranks are considered. You may report an issue if you find any discrepancy.

## Contribute
This project is still very small so there are no strict guidelines for contribution. You can report an issue if you find a bug or any other change you would like to make. You may also make a pull request. Be sure to clearly document and describe any issues or changes.

## FAQ

