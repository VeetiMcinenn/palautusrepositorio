import unittest
from unittest.mock import Mock
from varasto import Varasto
from tuote import Tuote

class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.kirjanpito_mock = Mock()
        self.varasto = Varasto(self.kirjanpito_mock)

    def test_alustus_luo_viisi_tuotetta(self):
        self.assertEqual(len(self.varasto._saldot), 5)

    def test_hae_tuote_palauttaa_tuotteen_id_n_perusteella(self):
        tuote = self.varasto.hae_tuote(3)

        self.assertEqual(tuote.id, 3)
        self.assertEqual(tuote.nimi, "Sierra Nevada Pale Ale")

    def test_hae_tuote_palauttaa_none_tuntemattomalle_idlle(self):
        self.assertIsNone(self.varasto.hae_tuote(999))

    def test_saldo_palauttaa_alkusaldon(self):
        self.assertEqual(self.varasto.saldo(1), 100)

    def test_ota_varastosta_vahentaa_saldoa(self):
        tuote = self.varasto.hae_tuote(2)

        self.varasto.ota_varastosta(tuote)

        self.assertEqual(self.varasto.saldo(2), 24)

    def test_ota_varastosta_kirjaa_tapahtuman(self):
        tuote = self.varasto.hae_tuote(2)

        self.varasto.ota_varastosta(tuote)

        self.kirjanpito_mock.lisaa_tapahtuma.assert_called_with("otettiin varastosta Fink Bräu I")

    def test_palauta_varastoon_lisaa_saldoa(self):
        tuote = self.varasto.hae_tuote(4)

        self.varasto.palauta_varastoon(tuote)

        self.assertEqual(self.varasto.saldo(4), 41)

    def test_palauta_varastoon_kirjaa_tapahtuman(self):
        tuote = self.varasto.hae_tuote(4)

        self.varasto.palauta_varastoon(tuote)

        self.kirjanpito_mock.lisaa_tapahtuma.assert_called_with("palautettiin varastoon Mikkeller not just another Wit")
