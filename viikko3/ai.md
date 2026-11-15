# Raportti: rekisteröitymisen storyt agentin avulla

Toteutin Claude Code -agentin avulla kaksi user storya login-sovellukseen:

1. Salasana ei saa koostua pelkästään kirjaimista
2. Salasanan ja salasanan vahvistuksen on oltava samat

Kummankin kohdalla agentti kirjoitti ensin hyväksymiskriteerit Robot Framework
-testeiksi `register.robot`-tiedostoon, ajoi testit ja osoitti niiden hajoavan,
ja vasta sitten lisäsi tarkistukset `user_service.py`:n `validate`-metodiin.
Lopputulos: 15 testiä, kaikki läpi, kaksi committia.

## Minkälaisen ohjetiedoston agentti generoi, ja mitä jouduit korjaamaan?

Projektissa ei ollut ohjetiedostoa ennen storyjen toteutusta; agentti teki työn
pelkän tehtävänannon ja koodin lukemisen varassa. Generoin `CLAUDE.md`:n vasta
raporttia kirjoittaessa `/init`-komennolla, jotta voin verrata sitä siihen, mitä
agentti joutui itse selvittämään matkan varrella.

Tiedostosta tuli lyhyt, kaksi osiota:

- **Commands:** sovelluksen käynnistys porttiin 5000 `flask run` -komennolla,
  testien ajo kokonaisuutena, yhden suiten ja yhden testin ajo
  `-t "nimi*"` -valitsimella, sekä `HEADLESS`-muuttujan käyttö.
- **Architecture:** kolmikerroksinen rakenne (`app.py` → `user_service` →
  `user_repository`), virheilmoitusten kulku `flash`-viesteinä templateihin,
  ja se että `validate()`-metodin virhetekstit ovat osa testien sopimusta.
  Lisäksi selitys siitä, miten `AppLibrary.py` nollaa sovelluksen tilan
  `/tests/reset`-reitin kautta ennen jokaista testiä.

Huomionarvoisinta on, että tiedosto varoittaa porttiristiriidasta: `index.py`
käynnistää sovelluksen porttiin 5001, mutta testit ja `AppLibrary.py` olettavat
porttia 5000. Tämä oli juuri se asia, johon agentti kompastui storyja
toteuttaessaan (ks. alla). Ohjetiedosto ei siis sisällä mitään, mitä koodista
ei voisi lukea, mutta se säästää seuraavalta sessiolta sen puolen tunnin
kompastelun, joka tähän sessioon kului.

Korjattavaa jäi vähän, koska tiedosto on lyhyt ja perustuu koodiin, jonka agentti
oli juuri lukenut. Kaksi asiaa, jotka tarkistin erikseen: väite pre-commit-hookin
pylint-ajosta piti paikkansa (se näkyi commitin tulosteessa), ja porttiohjeessa
mainittu `netstat`-komento toimii Windowsilla. Tiedosto on englanniksi, vaikka
koodin kommentit ovat suomeksi; jätin sen niin, koska agentti lukee kumpaakin.

## Noudattiko agentti pyyntöä kirjoittaa testit ennen toteutusta?

Kyllä, kummassakin storyssa ilman muistuttamista. Järjestys oli joka kerta:
lisää testit → aja koko testisarja → raportoi mitkä hajosivat → lisää tarkistus
→ aja uudelleen. Story 1:ssä hajosi kaksi hylkäystestiä (kallekalle, KalleKalle)
ja story 2:ssa yksi (eroavat salasanat). Hyväksymistestit ("kalle123",
"kalle#abc", samat salasanat) menivät läpi jo ennen toteutusta, mikä on oikein:
ne vartioivat, ettei uusi tarkistus hylkää liikaa.

Tämä järjestys osoittautui tärkeäksi ensimmäisellä ajolla, kun hajosi myös kaksi
vanhaa tehtävän 7 testiä. Jos testit olisi kirjoitettu toteutuksen jälkeen,
ne olisivat todennäköisesti menneet läpi ja porttiongelma olisi jäänyt huomaamatta.

## Kuinka paljon jouduit ohjaamaan agenttia matkan varrella?

Vähän, mutta kahdessa kohdassa.

**Portti.** Agentti huomasi itse, että portissa 5000 pyöri vanha, validoimaton
kopio samasta sovelluksesta edellisestä sessiosta, ja että `index.py` käynnistää
uuden kopion porttiin 5001. Testit ajettiin siis koodia vasten, jossa ei ollut
edes tehtävän 7 tarkistuksia. Agentti ei tappanut prosessia omin päin vaan kysyi
kolmesta vaihtoehdosta. Valitsin vanhan prosessin lopettamisen ja sovelluksen
käynnistämisen `flask run --port 5000` -komennolla, jolloin koodiin ei tarvinnut
koskea. Tässä ohjaus oli yksi valinta, ei korjaus.

**Rikkomisvaihe.** Keskeytin komennon, joka niputti kolme rikkomista ja kolme
testiajoa yhteen, koska halusin tietää kauanko se kestää. Keskeytys jätti
`user_service.py`:n rikottuun tilaan (vahvistuksen tarkistus oli `if False:`),
minkä agentti kertoi heti ja osoitti varmuuskopion sijainnin. Sen jälkeen
rikkomiset ajettiin yksi per komento, mikä oli helpompi lukea ja hyväksyä.

Muuten ohjaus oli vain komentojen hyväksymistä. `git diff` näytti, että agentti
muutti vain kahta tiedostoa: kaksi `if`-lausetta `user_service.py`:hyn ja kuusi
testiä `register.robot`-tiedostoon. Se ei korjannut porttiristiriitaa koodissa,
ei lisännyt docstringeja vaikka linter valitti niistä, eikä refaktoroinut mitään.
Poistettavaa ei jäänyt.

## Hajosivatko testit, kun rikoit toteutuksen tarkoituksella?

Kyllä, jokaisella kolmella kerralla:

| Rikkominen | Hajonneet testit |
|---|---|
| `isalpha()`-tarkistus pois (`if False:`) | 2: kallekalle ja KalleKalle |
| Vahvistuksen tarkistus pois (`if False:`) | 1: eroavat salasanat |
| Hylätään vain pienet kirjaimet (`isalpha() and islower()`) | 1: KalleKalle |

Kolmas rikkominen oli opettavaisin. Se osoittaa, että "KalleKalle"-testi ei ole
turha kopio "kallekalle"-testistä: se nappaa kiinni toteutuksen, joka tulkitsee
vaatimuksen liian kapeasti. Ilman sitä kaksi ensimmäistä testiä olisivat
päästäneet läpi tarkistuksen, joka hyväksyy "KalleKalle"-tyyppiset salasanat.

Jokaisen rikkomisen jälkeen tiedosto palautettiin varmuuskopiosta, ja lopuksi
koko sarja ajettiin vielä kerran: 15/15 läpi.

## Mitä uutta opit?

- **Testit testaavat sitä, mikä vastaa portissa, eivät sitä, mitä editorissa on
  auki.** Robot-testit eivät käynnistä sovellusta itse, joten unohtunut vanha
  prosessi tekee testituloksista valetta ilman yhtäkään virheilmoitusta.
  "Mahdottomat" tulokset (vanhat testit hajoavat ilman muutosta) ovat merkki
  tästä, eivät bugista koodissa.

- **Punainen vaihe on diagnostiikkaa, ei rituaali.** Se, *mitkä* testit hajoavat
  ennen toteutusta, kertoo enemmän kuin se, että joku hajoaa. Tässä se paljasti
  ympäristöongelman, jota ei muuten olisi huomattu.

- **Mutaatio, joka kohdistuu yhteen hyväksymiskriteeriin kerrallaan, on
  hyödyllisempi kuin koko tarkistuksen poisto.** `islower()`-rikkominen kertoi
  jotain testien laadusta; `if False:` kertoi vain, että testit ovat olemassa.

- **Virheilmoitusten tekstit ovat osa sopimusta.** Storyt eivät määritelleet
  sanamuotoja, joten agentti keksi ne. Ne elävät nyt sekä testeissä että
  koodissa ja pitää muuttaa molemmista yhtä aikaa. Tämä päätyi myös
  `CLAUDE.md`:hen.

- **Agentin pysähtyminen kysymään on arvokkaampaa kuin sen nopeus.** Portin
  kohdalla agentti olisi voinut "korjata" tilanteen muokkaamalla `index.py`:tä
  tai tappamalla prosessin, ja kumpikin olisi ollut muutos, jota en pyytänyt.
