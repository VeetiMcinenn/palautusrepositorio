Minkälaisen ohjetiedoston agentti generoi, ja mitä jouduit korjaamaan?

Projektissa ei ollut ohjetiedostoa storyjen toteutuksen aikana. Generoin CLAUDE.md:n /init-komennolla vasta raporttia varten. Siitä tuli lyhyt, kaksiosainen: Commands (sovelluksen käynnistys porttiin 5000, testien ajo kokonaisuutena, yhden suiten ja yhden testin ajo, HEADLESS-muuttuja) ja Architecture (kolmikerroksinen rakenne app.py → user_service → user_repository, virheviestien kulku flash-viesteinä, AppLibrary.py:n tapa nollata tila /tests/reset-reitin kautta). Tärkein kohta on varoitus porttiristiriidasta: index.py käynnistää sovelluksen porttiin 5001, testit odottavat 5000:aa. Juuri tähän agentti itse kompastui.

Korjattavaa ei juuri ollut, koska tiedosto perustuu koodiin, jonka agentti oli juuri lukenut. Tarkistin kaksi väitettä erikseen: pre-commit-hookin pylint-ajo (totta, näkyi commitin tulosteessa) ja netstat-komento Windowsilla (toimii). Tiedosto on englanniksi, vaikka koodin kommentit ovat suomeksi; jätin sen niin.

Noudattiko agentti pyyntöä kirjoittaa testit ennen toteutusta?

Kyllä, kummassakin storyssa ilman muistuttamista. Järjestys oli: lisää testit → aja → raportoi hajonneet → toteuta → aja uudelleen. Story 1:ssä hajosi kaksi hylkäystestiä, story 2:ssa yksi. Hyväksymistestit menivät läpi jo ennen toteutusta, mikä on oikein: ne vartioivat, ettei tarkistus hylkää liikaa.

Kuinka paljon jouduit ohjaamaan agenttia matkan varrella?

Vähän, kahdessa kohdassa. Ensimmäisellä ajolla hajosi myös kaksi vanhaa tehtävän 7 testiä. Agentti huomasi, että portissa 5000 pyöri vanha, validoimaton kopio sovelluksesta edellisestä sessiosta, eikä tappanut sitä omin päin vaan kysyi. Valitsin vanhan prosessin lopettamisen ja käynnistyksen flask run --port 5000 -komennolla, jolloin koodiin ei koskettu. Toinen kohta: keskeytin komennon, joka niputti kolme rikkomista yhteen. Keskeytys jätti tiedoston rikottuun tilaan, minkä agentti kertoi heti; sen jälkeen rikkomiset ajettiin yksi kerrallaan. git diff näytti, että agentti muutti vain kahta tiedostoa eikä koskenut mihinkään ylimääräiseen.

Hajosivatko testit, kun rikoit toteutuksen tarkoituksella?

Kyllä, kaikilla kolmella kerralla:

Rikkominen	Hajonneet testit
isalpha()-tarkistus pois	2 (kallekalle, KalleKalle)
Vahvistuksen tarkistus pois	1 (eroavat salasanat)
Hylätään vain pienet kirjaimet	1 (KalleKalle)
Kolmas oli opettavaisin: se osoitti, ettei "KalleKalle"-testi ole turha kopio, vaan nappaa liian kapean toteutuksen. Lopuksi koko sarja ajettiin palautetulla koodilla: 15/15 läpi.

Mitä uutta opit?

Testit testaavat sitä, mikä vastaa portissa, ei sitä mitä editorissa on auki. Unohtunut vanha prosessi tekee tuloksista valetta ilman virheilmoitusta.
Punainen vaihe on diagnostiikkaa: se, mitkä testit hajoavat, paljasti ympäristöongelman, joka olisi muuten jäänyt huomaamatta.
Yhteen kriteeriin kohdistuva mutaatio (islower()) kertoo testien laadusta; koko tarkistuksen poisto kertoo vain, että testit ovat olemassa.
Virheilmoitusten tekstit ovat osa sopimusta: ne elävät sekä testeissä että koodissa ja muutetaan yhdessä.
Agentin pysähtyminen kysymään oli arvokkaampaa kuin nopeus. Se olisi voinut "korjata" portin muokkaamalla index.py:tä tai tappamalla prosessin, ja kumpikaan ei ollut pyydetty muutos.