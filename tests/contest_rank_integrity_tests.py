import unittest
from os import listdir, path

from database.db_tools import CONTEST_RANKS_DIR, VALID_USN_REGEX, VALID_USERNAME_REGEX


class ContestsRanksIntegrityTests(unittest.TestCase):

    def test_unique_entries(self):
        for file_path in listdir(CONTEST_RANKS_DIR):
            with open(path.join(CONTEST_RANKS_DIR, file_path)) as fp:
                usn_or_handle_list = fp.read().split()
            self.assertEqual(len(usn_or_handle_list), len(set(usn_or_handle_list)),msg="Repeated users in file {}".format(file_path))

    def test_valid_entries(self):
        for file_path in listdir(CONTEST_RANKS_DIR):
            with open(path.join(CONTEST_RANKS_DIR, file_path)) as fp:
                usn_or_handle_list = fp.read().split()
            for usn_or_handle in usn_or_handle_list:
                self.assertTrue(VALID_USN_REGEX.match(usn_or_handle) or VALID_USERNAME_REGEX.match(usn_or_handle),msg="Invalid \
                USN or username {} in file {}".format(usn_or_handle,file_path))

    def test_non_empty_lines(self):
        for file_path in listdir(CONTEST_RANKS_DIR):
            with open(path.join(CONTEST_RANKS_DIR, file_path)) as fp:
                line_number:int=1
                for line in fp.readlines():
                    self.assertNotEqual(line.strip(), "",msg="Empty line - {} in {}".format(line_number,file_path))
                    line_number+=1

if __name__ == '__main__':
    unittest.main()
