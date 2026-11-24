# Ohjeet agentille

- Testit ajetaan komennolla `uv run pytest`.
- Tiedostojen `src/ostos.py` ja `src/tuote.py` koodia ei muuteta.
- Testejä ei muokata, ellei käyttäjä erikseen pyydä.
- Toteuta aina mahdollisimman minimaalinen koodi, jolla testit menevät läpi. Älä toteuta tulevien askelten toiminnallisuutta valmiiksi, äläkä lisää kommentteja tai rakenteita, joita testi ei vaadi.
- Pidä kaikki testit koko ajan toimivina. Jos muutos hajottaa testit, älä etene seuraavaan askeleeseen ennen kuin kaikki testit menevät taas läpi.
- Etene TDD:n mukaisesti yksi testi kerrallaan: kirjoita testi, varmista että se epäonnistuu, toteuta minimikoodi, aja kaikki testit.
