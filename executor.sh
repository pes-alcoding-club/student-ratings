#!/usr/bin/env bash

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
python3 ratings/processor.py database/contest_ranks/codechef-oct18.in
python3 ratings/processor.py database/contest_ranks/codechef-nov18.in
python3 ratings/processor.py database/contest_ranks/codechef-dec18.in
python3 ratings/processor.py database/contest_ranks/hackerearth-jan-easy-2019.in
python3 ratings/processor.py database/contest_ranks/codechef-jan19.in
python3 ratings/processor.py database/contest_ranks/codechef-feb19.in
python3 ratings/processor.py database/contest_ranks/codechef-feb-cookoff19.in

echo "Finished Ratings Update in $(( SECONDS - start ))s"

echo "-- Starting tests --"
python3 -m unittest discover -s tests -p '*_tests.py'
echo "-- Tests completed --"
python3 database/db_tools.py export_to_csv
echo "Exported Scoreboard from database. You can now quit."

read # Prevents the terminal from closing