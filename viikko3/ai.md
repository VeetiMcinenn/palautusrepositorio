# Raportti: rekisteröitymisen storyt agentin avulla

## Mitä tehtiin

Toteutin Claude Code -agentin avulla kaksi user storya login-sovellukseen:

1. Salasana ei saa koostua pelkästään kirjaimista
2. Salasanan ja salasanan vahvistuksen on oltava samat

Kummankin storyn kohdalla agentti kirjoitti ensin hyväksymiskriteerit Robot
Framework -testeiksi tiedostoon `register.robot`, ajoi testit ja osoitti niiden
hajoavan. Vasta sen jälkeen se lisäsi tarkistukset `user_service.py`:n
`validate`-metodiin ja ajoi testit uudelleen. Lopputulos: 15 testiä, kaikki läpi.

## Ongelma: testit osuivat väärään palvelimeen

Ensimmäisellä ajolla tulokset olivat sekavia: uudet hylkäystestit hajosivat
odotetusti, mutta myös kaksi tehtävän 7 vanhaa testiä hajosi, vaikka ne olivat
aiemmin menneet läpi. Agentti huomasi, että `index.py` käynnistää sovelluksen
porttiin 5001, mutta `AppLibrary.py` ja `resource.robot` olettavat portin 5000.
Portissa 5000 pyöri vanha, validoimaton instanssi samasta sovelluksesta, joka
oli jäänyt päälle aiemmasta sessiosta. Testit siis ajettiin koodia vasten, joka
ei sisältänyt edes tehtävän 7 tarkistuksia.

Agentti ei tappanut vierasta prosessia omin päin vaan kysyi. Hyväksyin vanhan
prosessin lopettamisen ja sovelluksen käynnistämisen porttiin 5000 komennolla
`flask --app app run --port 5000 --debug`, jolloin koodiin ei tarvinnut koskea.
Tämän jälkeen tulokset olivat järkeviä. Opetus: jos testit hajoavat "mahdottomalla"
tavalla, kannattaa ensin varmistaa, että ne ylipäätään testaavat sitä koodia,
jota luulee.

## Muutoksen läpikäynti

Kävin muutokset läpi `git diff` -komennolla. Agentti oli muuttanut vain kahta
tiedostoa: `user_service.py` sai kaksi uutta `if`-lausetta ja `register.robot`
kuusi uutta testiä. Se ei korjannut porttiristiriitaa koodissa, ei lisännyt
docstringeja, vaikka linter valitti niistä, eikä refaktoroinut mitään ympäriltä.
Mitään poistettavaa ei jäänyt.

## Miten voin olla varma, että testit testaavat uutta toiminnallisuutta?

Kahdella tavalla:

1. **Punainen ennen vihreää.** Testit ajettiin ennen toteutusta, ja ne hajosivat
   täsmälleen oikeista kohdista: story 1:ssä kaksi hylkäystestiä, story 2:ssa
   yksi. Hyväksymistestit ("kalle123" ja "kalle#abc" hyväksytään, samat salasanat
   hyväksytään) menivät läpi jo ennen toteutusta, mikä on oikein: ne vartioivat,
   ettei uusi tarkistus hylkää liikaa. Jos testi menee läpi ennen toteutusta ja
   sen jälkeen, se ei yksinään todista mitään uudesta koodista.

2. **Tarkoituksellinen rikkominen.** Rikoin toteutuksen kolmella tavalla ja ajoin
   testit joka kerta:

   | Rikkominen | Hajonneet testit |
   |---|---|
   | `isalpha()`-tarkistus pois (`if False:`) | 2: kallekalle ja KalleKalle |
   | Vahvistuksen tarkistus pois (`if False:`) | 1: eroavat salasanat |
   | Hylätään vain pienet kirjaimet (`isalpha() and islower()`) | 1: KalleKalle |

   Kolmas rikkominen oli kiinnostavin: se osoittaa, että "KalleKalle"-testi ei
   ole turha kopio "kallekalle"-testistä, vaan nappaa kiinni toteutuksen, joka
   olisi tulkinnut vaatimuksen liian kapeasti.

Jokaisen rikkomisen jälkeen tiedosto palautettiin varmuuskopiosta ja lopuksi
koko testisarja ajettiin vielä kerran: 15/15 läpi.

## Huomioita agentin kanssa työskentelystä

- Agentti noudatti "testit ensin" -järjestystä ilman, että sitä piti muistuttaa,
  ja ajoi testit itse kummassakin vaiheessa.
- Suurin arvo tuli siitä, että agentti huomasi porttiongelman ja pysähtyi
  kysymään sen sijaan, että olisi "korjannut" sen muuttamalla koodia tai
  tappamalla prosessin itse.
- Keskeytin rikkomisvaiheen komennon, koska se niputti kolme testiajoa yhteen
  komentoon ja mietin kauanko se kestää. Keskeytys jätti tiedoston rikottuun
  tilaan, minkä agentti kertoi heti. Yksi rikkominen per komento oli selkeämpi
  hyväksyä ja seurata.
- Virheilmoitusten sanamuodot ("Password must not consist of letters only",
  "Password and password confirmation do not match") olivat agentin keksimiä,
  koska storyt eivät määrittäneet niitä. Ne näkyvät sekä testeissä että
  koodissa, joten ne pitää vaihtaa molemmista, jos haluaa toisenlaiset.
