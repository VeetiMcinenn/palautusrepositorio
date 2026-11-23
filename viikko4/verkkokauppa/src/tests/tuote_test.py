import unittest
from tuote import Tuote

class TestTuote(unittest.TestCase):
    def setUp(self):
        self.tuote = Tuote(1, "maito", 5)

    def test_tuotteen_attribuutit_asetetaan(self):
        self.assertEqual(self.tuote.id, 1)
        self.assertEqual(self.tuote.nimi, "maito")
        self.assertEqual(self.tuote.hinta, 5)

    def test_samalla_idlla_olevat_tuotteet_ovat_yhtasuuret(self):
        toinen = Tuote(1, "eri nimi", 10)

        self.assertEqual(self.tuote, toinen)

    def test_eri_idlla_olevat_tuotteet_eivat_ole_yhtasuuret(self):
        toinen = Tuote(2, "maito", 5)

        self.assertNotEqual(self.tuote, toinen)

    def test_hash_perustuu_idhen(self):
        self.assertEqual(hash(self.tuote), hash(1))

    def test_str_palauttaa_nimen(self):
        self.assertEqual(str(self.tuote), "maito")
