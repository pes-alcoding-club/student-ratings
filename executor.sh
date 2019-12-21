#!/usr/bin/env bash

set -e
echo "Starting executor"

export PYTHONPATH="${PYTHONPATH}../student-ratings"

echo "-- Starting tests --"
python3 -m unittest discover -s tests -p '*_tests.py'
echo "-- Tests completed --"

# Reset the database to default values for everyone
python3 database/db_tools.py reset_database
echo "Finished Database Reset"

# Map usernames to USNs in all rank files
python3 database/db_tools.py map_username_to_usn

echo "Processing ratings. Please wait..."
start=$SECONDS

# List all contests ranks here in chronological order
python3 ratings/processor.py database/contest_ranks/codejam-qualification-2018.in
python3 ratings/processor.py database/contest_ranks/codejam-1a-2018.in
python3 ratings/processor.py database/contest_ranks/codejam-1b-2018.in
python3 ratings/processor.py database/contest_ranks/codejam-1c-2018.in
python3 ratings/processor.py database/contest_ranks/hackerearth-alcoding-2018.in
python3 ratings/processor.py database/contest_ranks/codechef-june18.in
python3 ratings/processor.py database/contest_ranks/codechef-july18.in
python3 ratings/processor.py database/contest_ranks/codechef-aug18.in
python3 ratings/processor.py database/contest_ranks/codechef-sept18.in
python3 ratings/processor.py database/contest_ranks/codechef-oct18.in
python3 ratings/processor.py database/contest_ranks/codechef-nov18.in
python3 ratings/processor.py database/contest_ranks/codechef-dec18.in
python3 ratings/processor.py database/contest_ranks/hackerearth-jan-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-jan19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-feb-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-feb19.in
python3 ratings/processor.py database/contest_ranks/codechef-feb-cookoff19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-feb-circuits19.in
python3 ratings/processor.py database/contest_ranks/codechef-mar19.in
python3 ratings/processor.py database/contest_ranks/kickstart-a-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-mar-cookoff19.in
python3 ratings/processor.py database/contest_ranks/codechef-mar-lunchtime19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-mar-circuits-2019.in
python3 ratings/processor.py database/contest_ranks/hackerearth-april-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codejam-qualification-2019.in
python3 ratings/processor.py database/contest_ranks/codejam-1a-2019.in
python3 ratings/processor.py database/contest_ranks/hackerearth-hourstorm#10-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-april19.in
python3 ratings/processor.py database/contest_ranks/kickstart-b-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-april-cookoff19.in
python3 ratings/processor.py database/contest_ranks/codechef-april-lunchtime19.in
python3 ratings/processor.py database/contest_ranks/codejam-1b-2019.in
python3 ratings/processor.py database/contest_ranks/codejam-1c-2019.in
python3 ratings/processor.py database/contest_ranks/hackerearth-april-circuits19.in
python3 ratings/processor.py database/contest_ranks/codechef-may19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-may-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codejam-round2-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-may-cookoff19.in
python3 ratings/processor.py database/contest_ranks/codechef-may-lunchtime19.in
python3 ratings/processor.py database/contest_ranks/kickstart-b-2019.in
python3 ratings/processor.py database/contest_ranks/hackerearth-may-circuits19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-june-easy-2019.in
python3 ratings/processor.py database/contest_ranks/hackerrank-alcoding-summer19-1.in
python3 ratings/processor.py database/contest_ranks/hackerrank-alcoding-summer19-2.in
python3 ratings/processor.py database/contest_ranks/codechef-june19.in
python3 ratings/processor.py database/contest_ranks/hackerrank-alcoding-summer19-3.in
python3 ratings/processor.py database/contest_ranks/codechef-june-cookoff19.in
python3 ratings/processor.py database/contest_ranks/hackerrank-alcoding-summer19-4.in
python3 ratings/processor.py database/contest_ranks/codechef-june-lunchtime19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-june-circuits19.in
python3 ratings/processor.py database/contest_ranks/hackerrank-alcoding-summer19-5.in
python3 ratings/processor.py database/contest_ranks/hackerearth-july-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-july19.in
python3 ratings/processor.py database/contest_ranks/hackerrank-alcoding-summer19-6.in
python3 ratings/processor.py database/contest_ranks/codechef-july-cookoff19.in
python3 ratings/processor.py database/contest_ranks/hackerrank-alcoding-summer19-7.in
python3 ratings/processor.py database/contest_ranks/codechef-july-lunchtime19.in
python3 ratings/processor.py database/contest_ranks/kickstart-d-2019.in
python3 ratings/processor.py database/contest_ranks/hackerearth-august-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-aug19.in
python3 ratings/processor.py database/contest_ranks/codechef-aug-cookoff19.in
python3 ratings/processor.py database/contest_ranks/kickstart-e-2019.in
python3 ratings/processor.py database/contest_ranks/hackerearth-aug-circuits19.in
python3 ratings/processor.py database/contest_ranks/codechef-aug-lunchtime19.in
python3 ratings/processor.py database/contest_ranks/codechef-alcoding-global-challenge.in
python3 ratings/processor.py database/contest_ranks/hackerearth-sept-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-sept19.in
python3 ratings/processor.py database/contest_ranks/codechef-sept-cookoff19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-sept-circuits19.in
python3 ratings/processor.py database/contest_ranks/codechef-sept-lunchtime19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-oct-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-oct19.in
python3 ratings/processor.py database/contest_ranks/codechef-oct-cookoff19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-oct-circuits19.in
python3 ratings/processor.py database/contest_ranks/codechef-oct-lunchtime19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-nov-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-nov19.in
python3 ratings/processor.py database/contest_ranks/codechef-nov-cookoff19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-nov-circuits19.in
python3 ratings/processor.py database/contest_ranks/codechef-nov-lunchtime19.in
python3 ratings/processor.py database/contest_ranks/codechef-dec19.in
python3 ratings/processor.py database/contest_ranks/hackerearth-dec-easy-2019.in

echo "Finished Ratings Update in $(( SECONDS - start ))s"

echo "-- Starting tests --"
python3 -m unittest discover -s tests -p '*_tests.py'
echo "-- Tests completed --"
python3 database/db_tools.py export_to_csv
python3 database/db_tools.py prettify
echo "Exported Scoreboard from database. You can now quit."

read # Prevents the terminal from closing
