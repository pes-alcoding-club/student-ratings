"""
This script identifies those usernames which have not been mapped to any USNs
"""
from os import listdir, path
from collections import Counter
from utils.union_responses_with_db import VALID_USN_PATTERN

RANKS_DIR = "database/contest_ranks"
candidates = []
for file in listdir(RANKS_DIR):
    with open(path.join(RANKS_DIR, file)) as fp:
        site_name = file.split("-")[0]
        candidates += [(site_name, x) for x in fp.read().split()]
candidates = list(filter(lambda x: not VALID_USN_PATTERN.match(x[1]), candidates))
counter = Counter(candidates)
with open("utils/unmapped-handles.out", "w") as fp:
    print(len(counter), file=fp)
    print(*counter.most_common(), sep='\n', file=fp)
