import re
import unittest
from os import listdir, path

from database.db_tools import CONTEST_RANKS_DIR, VALID_USN_REGEX, VALID_USERNAME_REGEX


class ContestsRanksIntegrityTests(unittest.TestCase):

    def test_unique_entries(self):
        for file_path in listdir(CONTEST_RANKS_DIR):
            with open(path.join(CONTEST_RANKS_DIR, file_path)) as fp:
                usn_or_handle_list = fp.read().split()
            self.assertEqual(len(usn_or_handle_list), len(set(usn_or_handle_list)))

    def test_valid_entries(self):
        valid_usn_or_handle_regex = re.compile(VALID_USN_REGEX + r"|" + VALID_USERNAME_REGEX)
        for file_path in listdir(CONTEST_RANKS_DIR):
            with open(path.join(CONTEST_RANKS_DIR, file_path)) as fp:
                usn_or_handle_list = fp.read().split()
            for usn_or_handle in usn_or_handle_list:
                self.assertRegex(usn_or_handle, valid_usn_or_handle_regex)

    def test_non_empty_lines(self):
        for file_path in listdir(CONTEST_RANKS_DIR):
            with open(path.join(CONTEST_RANKS_DIR, file_path)) as fp:
                for line in fp.readlines():
                    self.assertNotEqual(line.strip(), "")


if __name__ == '__main__':
    unittest.main()
