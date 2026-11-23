import unittest
from ostoskori import Ostoskori
from tuote import Tuote

class TestOstoskori(unittest.TestCase):
    def setUp(self):
        self.ostoskori = Ostoskori()

    def test_tyhjan_ostoskorin_hinta_on_nolla(self):
        self.assertEqual(self.ostoskori.hinta(), 0)

    def test_lisaa_kasvattaa_hintaa(self):
        self.ostoskori.lisaa(Tuote(1, "maito", 5))
        self.ostoskori.lisaa(Tuote(2, "leipä", 3))

        self.assertEqual(self.ostoskori.hinta(), 8)

    def test_poista_poistaa_tuotteen_id_n_perusteella(self):
        self.ostoskori.lisaa(Tuote(1, "maito", 5))
        self.ostoskori.lisaa(Tuote(2, "leipä", 3))

        self.ostoskori.poista(Tuote(1, "maito", 5))

        self.assertEqual(self.ostoskori.hinta(), 3)

    def test_poista_ei_muuta_korin_sisaltoa_jos_tuotetta_ei_ole(self):
        self.ostoskori.lisaa(Tuote(1, "maito", 5))

        self.ostoskori.poista(Tuote(2, "leipä", 3))

        self.assertEqual(self.ostoskori.hinta(), 5)
