#!/usr/bin/env bash

echo "Starting executor"

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    alias py='python3'
fi

export PYTHONPATH="${PYTHONPATH}../alcoding"

py database/db_tools.py reset_database
echo "Finished Database Reset"

# List all contests ranks here in chronological order
py ratings/processor.py database/contest_ranks/codejam-qualification.in codejam
py ratings/processor.py database/contest_ranks/codejam-1a.in codejam
py ratings/processor.py database/contest_ranks/codejam-1b.in codejam
py ratings/processor.py database/contest_ranks/codejam-1c.in codejam
py ratings/processor.py database/contest_ranks/codejam-2.in codejam
py ratings/processor.py database/contest_ranks/alcoding2018.in hackerearth

echo "Finished Ratings Update"

py database/db_tools.py export_to_csv
echo "Exported Scoreboard from database. You can now quit."

read # Prevents the terminal from closing
