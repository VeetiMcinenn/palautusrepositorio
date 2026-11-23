import unittest
from viitegeneraattori import Viitegeneraattori

class TestViitegeneraattori(unittest.TestCase):
    def setUp(self):
        self.viitegeneraattori = Viitegeneraattori()

    def test_ensimmainen_viite_on_kaksi(self):
        self.assertEqual(self.viitegeneraattori.uusi(), 2)

    def test_jokainen_viite_on_edellista_suurempi(self):
        self.assertEqual(self.viitegeneraattori.uusi(), 2)
        self.assertEqual(self.viitegeneraattori.uusi(), 3)
        self.assertEqual(self.viitegeneraattori.uusi(), 4)
