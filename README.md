# tsoha

Tietokantasovellus, harjoitustyö

Sovellus osoitteessa: https://morning-garden-53294.herokuapp.com/ 
Login:
- Admin: admin@gmail.com / test
- Supervisor: test@gmail.com / test

Tiedetyt bugit:

Tulevat korjaukset ja bugin kokonaisuudessaan [(https://github.com/roopekole/tsoha/issues)](https://github.com/roopekole/tsoha/issues) 
- Sivutuksen ja haun kanssa yhteistominnallisuus bugi (kts. issue)
- Käyttäjä taulu ei muutu scrollattavaksi (koskee vain alle 500px levyistä näyttöä - ei paha ongelma)
- Showing 'Access denied' also when user is not logged in and tries to insert forbidden path - now returns error

(Inspiraation lähde: http://advancedkittenry.github.io/suunnittelu_ja_tyoymparisto/aiheet/Graduaiheet.html)

Sovellus oppilaitoksen lopputöiden aihepiirien hallintaan. Opiskelija hakee oman tieteen alansa tutkielman aihetta joltakin potentiaaliselta tutkielman ohjaajalta. Aiheita annettaessa pyritään siihen, ettei samanaikaisesti annettaisi samaa aihetta usealle opiskelijalle (mahdollinen poikkeus esim. samanaikainen kandityö ja gradu). Pyritään myös välttämään aiheita, joista juuri on tehty saman tasoinen tutkielma. Aihe saattaa viipyä valmisteluvaiheessa pitkään ja myös valmisteltavina olevista aiheista pitäisi saada tietoa. Rakenettavan sovelluksen tehtävänä on helpottaa oman tieteenalan lopputyön aihepiirin hakua ja antamista. Opiskelijat ja opettajat voisivat järjestelmästä tutkia, keneltä aiheita saa ja mitä aiheita kukin parhaillaan ohjaa. Samoin valmisteilla olevat aiheet saataisiin esiin. Tutkielman tekijätieto näkyisi ainakin ohjaajille ja valmiiden töiden osalta kaikille. Aiheita ja ohjaajia voisi luokitella tieteenaloittain ja aihepiireittäin.

Toimintoja:

- Kirjautuminen + rekisteröityminen (ohjaaja, admin)
- Master datan hallinnointi (admin)
- Aiheen kirjaus ja muokkaus (ohjaajalle)
- Aiheen poistaminen (vain jos sitä ei ole varattu, ohjaajalle)
- Aiheen varaus opiskelijalle (ohjaajalle)
- Käynnissä olevien aiheiden luettelo aihepiireittäin (oppilaalle)
- Valmisteilla olevien luettelo aihepiireittäin (oppilaalle)
- Valmiiden gradujen luettelo (oppilaalle)
- Luetteloiden selaus, sorttaus ja niistä etsiminen

Dokumentaatio (englanniksi)

[Käyttäjäopas (User manual)](https://github.com/roopekole/tsoha/blob/master/documentation/user_manual.md)

[Käyttötapauslistaus (Use cases)](https://github.com/roopekole/tsoha/blob/master/documentation/usecases.md)

[Asennusopas (Installation guide)](https://github.com/roopekole/tsoha/blob/master/documentation/installation_guide.md)

[Tietokantakaavio (Database chart)](https://github.com/roopekole/tsoha/blob/master/documentation/database_chart.txt)

Tsoha-projektin vaatimukset

- [x] Aiheen kuvaus (readme)
- [x] Käyttöohje
- [x] Asennusohje
- [x] Työn ja sovelluksen rajoitteet (issuet, readme, käyttötapaukset)
- [x] Työn puuttuvat ominaisuudet (issuet)
- [x] Käyttötapaukset / user storyt ja niihin liittyvät SQL-kyselyt
- [x] Tietokantarakenteen kuvaus
- [x] Tietokantataulujen normalisointi 
- [x] Tietokantakaavion sisällyttäminen dokumentaatioon
- [x] Tietokantakaavion ja todellisen tietokannan vastaavuus
- [x] CREATE TABLE -lauseet sekä indeksien lisäykset (indeksejä ei toteutettu)
- [x] Ohjelmassa ei SQL-injektiomahdollisuuksia (Polut suojattu)
- [x] isoksi kasvavissa listauksissa sivutus (Thesis listauksesta löytyy)
- [x] käyttäjien syötteet validoidaan palvelimella (ja vastaa tietokannan vaateita)
- [x] kyselyiden toteuttaminen tehokkaasti (käytössä kymmenkunta join kyselyä)
- [x] sovelluksissa käytössä ja toteutettuna monimutkaisempia yhteenvetokyselyitä (User-luokassa kaksi yhteenvetokyselyksi luokiteltua raaka-SQL -lausetta, Science-luokassa yksi kysely)
- [x] Ei rikkinäisiä linkkejä, lomakkeet toimivat kun syöte järkevä
- [x] Sovellus toimii vaikka syöte ei järkevää (validointi joko palvelimella tai selaimella)
- [x] Tiedon hakeminen
- [x] Yksi N-N assosiaatio kahden tietokohteen välillä (Thesis-Science)
- [x] Neljä tietokohdetta
- [x] Kahteen tietokohteeseen (Thesis, User) CRUD (yhden kohteen read, kohteen editointi, kohteen poisto, kohteen luonti)
- [x] Kirjautuminen ja käyttäjän yhdistäminen tietokohteeseen (käyttäjä-thesis)
