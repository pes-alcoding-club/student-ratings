#!/usr/bin/env bash

echo "Starting executor"

export PYTHONPATH="${PYTHONPATH}../alcoding"

echo "-- Starting tests --"
python3 tests/*
echo "-- Tests completed --"

python3 database/db_tools.py reset_database
echo "Finished Database Reset"
echo "Processing ratings. Please wait..."

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

echo "Finished Ratings Update"

echo "-- Starting tests --"
python3 tests/*
echo "-- Tests completed --"
python3 database/db_tools.py export_to_csv
echo "Exported Scoreboard from database. You can now quit."

read # Prevents the terminal from closing