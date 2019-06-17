#!/usr/bin/env bash

set -e
echo "Starting executor"

export PYTHONPATH="${PYTHONPATH}../alcoding"

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


echo "Finished Ratings Update in $(( SECONDS - start ))s"

echo "-- Starting tests --"
python3 -m unittest discover -s tests -p '*_tests.py'
echo "-- Tests completed --"
python3 database/db_tools.py export_to_csv
python3 database/db_tools.py prettify
echo "Exported Scoreboard from database. You can now quit."

read # Prevents the terminal from closing