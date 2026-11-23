import unittest
from unittest.mock import Mock
from pankki import Pankki

class TestPankki(unittest.TestCase):
    def setUp(self):
        self.kirjanpito_mock = Mock()
        self.pankki = Pankki(self.kirjanpito_mock)

    def test_tilisiirto_palauttaa_true(self):
        tulos = self.pankki.tilisiirto("pekka", "42", "12345", "33333-44455", 5)

        self.assertTrue(tulos)

    def test_tilisiirto_kirjaa_tapahtuman(self):
        self.pankki.tilisiirto("pekka", "42", "12345", "33333-44455", 5)

        self.kirjanpito_mock.lisaa_tapahtuma.assert_called_with(
            "tilisiirto: tililtä 12345 tilille 33333-44455 viite 42 summa 5e"
        )
