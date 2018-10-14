#!/usr/bin/env bash

echo "Starting executor"

export PYTHONPATH="${PYTHONPATH}../alcoding"

python database/db_tools.py reset_database
echo "Finished Database Reset"

# List all contests ranks here in chronological order
python ratings/processor.py database/contest_ranks/codejam-qualification.in codejam
python ratings/processor.py database/contest_ranks/codejam-1a.in codejam
python ratings/processor.py database/contest_ranks/codejam-1b.in codejam
python ratings/processor.py database/contest_ranks/codejam-1c.in codejam
python ratings/processor.py database/contest_ranks/alcoding2018.in hackerearth

echo "Finished Ratings Update"

python database/db_tools.py export_to_csv
echo "Exported Scoreboard from database. You can now quit."

read # Prevents the terminal from closing