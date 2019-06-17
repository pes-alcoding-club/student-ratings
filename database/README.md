### Database

This module contains the data about students' performances in contests.

It also contains functions necessary to query and update this data.

#### Description
1. contest_ranks: Each file contains rank list of students
2. db_pass.txt: Password to access the database. This version of the file is accessible only to those managing the repository.
3. db_tools.py: Variables and functions to read, write and reset database

##### Contest Ranks
Following is the list of contests that have been considered for rating so far

| S.no. | Contest Name | Rank File | Start Date | End Date |
| ----- | ----------------- | ----------- | ------------- | ---------- |
| 1. | [Google Codejam 2018 Qualification Round](https://codejam.withgoogle.com/2018/challenges/00000000000000cb/scoreboard) | codejam_qualification-2018.in | 07/04/2018(04:30) | 08/04/2018(07:30) |
| 2. | [Google Codejam 2018 Round 1A](https://codejam.withgoogle.com/2018/challenges/0000000000007883/scoreboard) | codejam-1a-2018.in | 14/04/2018(06:30) | 14/04/2018(09:00) |
| 3. | [Google Codejam 2018 Round 1B](https://codejam.withgoogle.com/2018/challenges/0000000000007764/scoreboard) | codejam-1b-2018.in | 29/04/2018(21:30) | 30/04/2018(00:00) |
| 4. | [Google Codejam 2018 Round 1C](https://codejam.withgoogle.com/2018/challenges/0000000000007765/scoreboard) | codejam-1c-2018.in | 05/05/2018(14:30) | 05/05/2018(20:00) |
| 5. | [PESU Alcoding Club April 2018](https://www.hackerearth.com/challenge/college/pes-alcoding-contest-2018-april/leaderboard/) | hackerearth-alcoding-2018.in | 18/04/2018(16:00) | 18/04/2018(20:30) |
| 6. | [Codechef June Long Challenge 2018](https://www.codechef.com/JUNE18) | codechef-june18.in | 01/06/2018(15:00) | 11/06/2018(15:00) |
| 7. | [Codechef July Long Challenge 2018](https://www.codechef.com/JULY18) | codechef-july18.in | 06/06/2018(15:00) | 16/07/2018(15:00) |
| 8. | [Codechef August Long Challenge 2018](https://www.codechef.com/AUG18) | codechef-aug18.in | 03/08/2018(15:00) | 13/08/2018(15:00) |
| 9. | [Codechef September Long Challenge 2018](https://www.codechef.com/SEPT18) | codechef-sept18.in | 07/09/2018(15:00) | 17/09/2018(15:00) |
| 10. | [Codechef October Long Challenge 2018](https://www.codechef.com/OCT18) | codechef-oct18.in | 05/10/2018 (15:00) | 17/10/2018(15:00) |
| 11. | [Codechef November Long Challenge 2018](https://www.codechef.com/NOV18) | codechef-nov18.in | 02/11/2018(15:00) | 12/11/2018(15:00) |
| 12. | [Codechef December Long Challenge 2018](https://www.codechef.com/DEC18) | codechef-dec18.in | 07/12/2018(15:00) | 17/12/2018(15:00) |
| 13. | [Hackearth January Easy 2019](https://www.hackerearth.com/challenge/competitive/january-easy-19/) | hackerearth-jan-easy-2019.in | 06/01/2019(21:00) | 07/01/2019(00:00) |
| 14. | [Codechef January Long Challenge 2019](https://www.codechef.com/JAN19) | codechef-jan19.in | 04/01/2019(15:00) | 14/01/2019(15:00) |
| 15. | [Hackearth February Easy 2019](https://www.hackerearth.com/challenges/competitive/february-easy-19/) | hackerearth-feb-easy-2019.in | 01/02/2019(21:00) | 02/02/2019(00:00) |
| 16. | [Codechef February Long Challenge 2019](https://www.codechef.com/FEB19) | codechef-feb19.in | 01/02/2019(15:00) | 11/02/2019(15:00) |
| 17. | [Codechef February Cookoff 2019](https://www.codechef.com/COOK103) | codechef-feb-cookoff19.in | 17/02/2019(21:30) | 18/02/2019(00:00) |
| 18. | [Hackerearth February Circuits 2019](https://www.hackerearth.com/challenges/competitive/february-circuits-19/) | hackerearth-feb-circuits19.in | 15/02/2019(21:00) | 24/02/2019(21:00) |
| 19. | [Codechef March Long Challenge 2019](https://www.codechef.com/MARCH19) | codechef-mar19.in | 01/03/2019(15:00) | 11/03/2019(15:00) |
| 20. | [Google Kickstart 2019 Round A](https://codingcompetitions.withgoogle.com/kickstart/round/0000000000050e01) | kickstart-a-2019.in | 24/03/2019(09:30) | 24/03/2019(12:45) |
| 21. | [Codechef March Cookoff 2019](https://www.codechef.com/COOK104) | codechef-mar-cookoff19.in | 24/03/2019(21:30) | 25/03/2019(00:00) |
| 22. | [Codechef March Lunchtime 2019](https://www.codechef.com/LTIME70) | codechef-mar-lunchtime19.in | 30/03/2019(19:30) | 30/03/2019(22:30) |
| 23. | [Hackerearth March Circuits 2019](https://www.hackerearth.com/challenges/competitive/march-circuits-19/) | hackerearth-mar-circuits-2019.in | 22/03/2019(21:00) | 31/03/2019(21:00) |
| 24. | [Hackerearth April Easy 2019](https://www.hackerearth.com/challenge/competitive/april-easy-19/) | hackerearth-april-easy-2019.in | 06/04/2019(21:30) | 07/04/2019(00:30) |
| 25. | [Google Codejam 2019 Qualification Round](https://codingcompetitions.withgoogle.com/codejam/round/0000000000051705) | codejam_qualification-2019.in | 06/04/2019(04:30) | 07/04/2019(7:30) |
| 26. | [Google Codejam 2019 Round 1A](https://codingcompetitions.withgoogle.com/codejam/round/0000000000051635) | codejam-1a-2019.in | 13/04/2019(06:30) | 13/04/2019(09:00) |
| 27. | [Hackerearth HourStorm #10 2019](https://www.hackerearth.com/challenges/competitive/hourstorm-10/) | hackerearth-hourstorm#10-2019.in | 13/04/2019(21:30) | 13/04/2019(22:30) |
| 28. | [Codechef April Long Challenge 2019](https://www.codechef.com/APRIL19) | codechef-april19.in | 05/04/2019(15:00) | 15/04/2019(15:00) |
| 29. | [Google Kickstart 2019 Round B](https://codingcompetitions.withgoogle.com/kickstart/round/0000000000050eda) | kickstart-b-2019.in | 21/04/2019(04:30) | 21/04/2019(07:30) |
| 30. | [Codechef April Cookoff 2019](https://www.codechef.com/COOK105) | codechef-april-cookoff19.in | 21/04/2019(21:30) | 22/04/2019(00:00) |
| 31. | [Codechef April Lunchtime 2019](https://www.codechef.com/LTIME71) | codechef-april-lunchtime19.in | 27/04/2019(19:30) | 27/04/2019(22:30) |
| 32. | [Google Codejam 2019 Round 1B](https://codingcompetitions.withgoogle.com/codejam/round/0000000000051706) | codejam-1b-2019.in | 28/04/2019(21:30) | 29/04/2019(00:00) |
| 33. | [Google Codejam 2019 Round 1C](https://codingcompetitions.withgoogle.com/codejam/round/00000000000516b9) | codejam-1c-2019.in | 04/05/2019(14:30) | 04/05/2019(17:00) |
| 34. | [Hackerearth April Circuits 2019](https://www.hackerearth.com/challenges/competitive/april-circuits-19/) | hackerearth-april-circuits19.in | 26/04/2019(21:00) | 05/05/2019(21:00) |
| 35. | [Codechef May Long Challenge 2019](https://www.codechef.com/MAY19) | codechef-may19.in | 03/05/2019(15:00) | 13/05/2019(15:00) |
| 36. | [Hackerearth May Easy 2019](https://www.hackerearth.com/challenge/competitive/may-easy-19/) | hackerearth-may-easy-2019.in | 13/05/2019(21:30) | 14/05/2019(00:00) |
| 37. | [Google Codejam 2019 Round 2](https://codingcompetitions.withgoogle.com/codejam/round/0000000000051679) | codejam-round2-2019.in | 18/05/2019(19:30) | 18/05/2019(22:00) |
| 38. | [Codechef May Cookoff 2019](https://www.codechef.com/COOK106) | codechef-may-cookoff19.in | 19/05/2019(21:30) | 19/05/2019(00:00) |
| 39. | [Codechef May Lunchtime 2019](https://www.codechef.com/LTIME72) | codechef-may-lunchtime19.in | 25/05/2019(19:30) | 25/05/2019(22:30) |
| 40. | [Google Kickstart 2019 Round C](https://codingcompetitions.withgoogle.com/kickstart/round/0000000000050ff2) | kickstart-c-2019.in | 26/05/2019(14:30) | 26/05/2019(17:30) |
| 41. | [Hackerearth May Circuits 2019](https://www.hackerearth.com/challenges/competitive/may-circuits-19/) | hackerearth-may-circuits19.in | 24/05/2019(21:00) | 02/06/2019(21:00) |
| 42. | [Hackerearth June Easy 2019](https://www.hackerearth.com/challenge/competitive/june-easy-19/) | hackerearth-june-easy-2019.in | 2/06/2019(21:30) | 3/06/2019(00:30) |
| 43. | [Hackerrank Alcoding Summer Week 1](https://www.hackerrank.com/contests/alcoding-summer-weekly-contest-1/challenges) | hackerrank-alcoding-summer19-1.in | 7/06/2019(21:00) | 8/06/2019(00:00) |
| 44. | [Hackerrank Alcoding Summer Week 2](https://www.hackerrank.com/contests/alcoding-summer-weekly-contest-2/challenges) | hackerrank-alcoding-summer19-2.in | 14/06/2019(21:00) | 14/06/2019(00:00) |