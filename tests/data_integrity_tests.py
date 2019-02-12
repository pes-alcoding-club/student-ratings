import unittest
import re
from tinydb import TinyDB, where
import database.db_tools as db
from ratings import elo

database = TinyDB(db.DB_FILE)
mandatory_cols = [db.USN, db.NAME, db.RATING, db.VOLATILITY, db.EMAIL, db.YEAR, db.BEST, db.LAST_FIVE, db.TIMES_PLAYED]
sites = [db.CODEJAM, db.KICKSTART, db.CODECHEF, db.HACKERRANK, db.HACKEREARTH, db.CODEFORCES]


class MyTestCase(unittest.TestCase):

    def test_mandatory_cols(self):
        for row in database.all():
            for col in mandatory_cols:
                self.assertIn(col, row)

    def test_unique_usn(self):
        rows = [x[db.USN] for x in database.all()]
        self.assertEqual(len(database), len(rows))
        self.assertEqual(len(rows), len(set(rows)))

    def test_unique_email(self):
        rows = [x[db.EMAIL] for x in database.all()]
        self.assertEqual(len(database), len(rows))
        self.assertEqual(len(rows), len(set(rows)))

    def test_unique_handles(self):
        for site in sites:
            results = database.search(where(site))
            handles = [result[site] for result in results]
            self.assertEqual(len(results), len(handles))
            self.assertEqual(len(results), len(set(handles)))

    def test_valid_usn(self):
        valid_usn_regex = re.compile(db.VALID_USN_REGEX)
        for row in database.all():
            self.assertRegex(row[db.USN], valid_usn_regex)

    def test_valid_handles(self):
        valid_handle_regex = re.compile(r"^[\w_\-.]{3,}$")
        for row in database.all():
            for site in sites:
                if site in row:
                    self.assertRegex(row[site], valid_handle_regex)

    def test_valid_year(self):
        for row in database.all():
            self.assertGreaterEqual(row[db.YEAR], db.VALID_MIN_YEAR)
            self.assertLessEqual(row[db.YEAR], db.VALID_MAX_YEAR)

    def test_valid_name(self):
        valid_name_regex = re.compile(db.VALID_NAME_REGEX)
        for row in database.all():
            self.assertRegex(row[db.NAME], valid_name_regex)

    def test_valid_email(self):
        valid_email_reqex = re.compile(db.VALID_EMAIL_REGEX)
        for row in database.all():
            self.assertRegex(row[db.EMAIL], valid_email_reqex)

    def test_valid_rating_and_best(self):
        for row in database.all():
            self.assertGreaterEqual(row[db.RATING], 0)
            self.assertGreaterEqual(row[db.BEST], 0)

    def test_valid_volatility(self):
        for row in database.all():
            self.assertGreaterEqual(row[db.VOLATILITY], elo.MIN_VOLATILITY)
            self.assertLessEqual(row[db.VOLATILITY], elo.MAX_VOLATILITY)

    def test_valid_defaults(self):
        for row in database.search(where(db.TIMES_PLAYED) == 0):
            self.assertEqual(row[db.RATING], elo.DEFAULT_RATING)
            self.assertEqual(row[db.BEST], elo.DEFAULT_RATING)
            self.assertEqual(row[db.VOLATILITY], elo.DEFAULT_VOLATILITY)
            self.assertEqual(row[db.LAST_FIVE], 5)

    def test_valid_last_five(self):
        for row in database.all():
            self.assertGreaterEqual(row[db.LAST_FIVE], 1)
            self.assertLessEqual(row[db.LAST_FIVE], 5)


if __name__ == '__main__':
    unittest.main()
