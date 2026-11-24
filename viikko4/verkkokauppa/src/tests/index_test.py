import io
import runpy
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import index
from kirjanpito import Kirjanpito
from pankki import Pankki
from varasto import Varasto
from viitegeneraattori import Viitegeneraattori

class TestIndex(unittest.TestCase):
    def test_main_tulostaa_kirjanpidon_tapahtumat(self):
        kirjanpito = Kirjanpito()

        # korvataan oletusoliot omilla, jotta testi ei muuta globaaleja olioita
        with patch.multiple(
            index,
            kirjanpito=kirjanpito,
            varasto=Varasto(kirjanpito),
            pankki=Pankki(kirjanpito),
            viitegeneraattori=Viitegeneraattori()
        ):
            tuloste = io.StringIO()
            with redirect_stdout(tuloste):
                index.main()

        rivit = tuloste.getvalue().splitlines()

        # ensimmäinen asiakas: 1 poistettu, kaksi tuotetta 3e ja 5e -> ei, 5e + 5e = 10e
        self.assertIn("tilisiirto: tililtä 1234-12345 tilille 33333-44455 viite 2 summa 10e", rivit)
        # toinen asiakas: varastossa vain 15 kpl tuotetta 5 -> 15 * 4e = 60e
        self.assertIn("tilisiirto: tililtä 3425-1652 tilille 33333-44455 viite 3 summa 60e", rivit)
        # 5 tapahtumaa ensimmäiseltä asiakkaalta, 15 varastotapahtumaa ja tilisiirto toiselta
        self.assertEqual(len(rivit), 21)

    def test_suoritettaessa_tiedostona_kutsutaan_main(self):
        tiedosto = Path(index.__file__)

        tuloste = io.StringIO()
        with redirect_stdout(tuloste):
            runpy.run_path(str(tiedosto), run_name="__main__")

        self.assertIn("tilisiirto", tuloste.getvalue())
