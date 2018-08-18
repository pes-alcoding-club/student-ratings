from unittest import TestCase

from ratings import elo

class TestRatings(TestCase):

    def test_Eab(self):
        self.assertEqual(elo.Eab(1000, 3, 1000, 900), 0.5)
        self.assertEqual(elo.Eab(10, 3, 5, 4), 0.2)

