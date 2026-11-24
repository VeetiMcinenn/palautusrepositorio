import unittest
from kirjanpito import Kirjanpito

class TestKirjanpito(unittest.TestCase):
    def setUp(self):
        self.kirjanpito = Kirjanpito()

    def test_uusi_kirjanpito_on_tyhja(self):
        self.assertEqual(self.kirjanpito.tapahtumat, [])

    def test_lisaa_tapahtuma_lisaa_tapahtuman_listaan(self):
        self.kirjanpito.lisaa_tapahtuma("testi")

        self.assertEqual(self.kirjanpito.tapahtumat, ["testi"])

    def test_tapahtumat_sailyvat_jarjestyksessa(self):
        self.kirjanpito.lisaa_tapahtuma("ensimmäinen")
        self.kirjanpito.lisaa_tapahtuma("toinen")

        self.assertEqual(self.kirjanpito.tapahtumat, ["ensimmäinen", "toinen"])
