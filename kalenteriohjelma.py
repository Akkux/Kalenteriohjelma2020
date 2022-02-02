#Kalenteriohjelma
#Akseli Nuutila 2020

import calendar
import json
import datetime
from lukujärjestys import *

def valinta():
#Valinta-metodi tarjoaa käyttäjälle eri toimintoja ja suorittaa seuraavan metodin
#käyttäjän syötteen mukaan.
    print("-----------------------------------------------")
    print("Mitä haluat tehdä seuraavaksi?")
    x = input("""('L') Luo ja muokkaa tapahtumia\n('P') Poista tapahtumia 
('H') Hae tapahtumatietoja\nValinta: """)
    #Tarkistetaan käyttäjän syöte ja siirrytään seuraavaan metodiin.
    if x == "L":
        lisääTapahtumia()
    elif x == "H":
        haeTietoa()
    elif x == "P":
        poistaPäivä()
    #Jos syöte on jotain muuta kuin sallitut vaihtoehdot, ilmoitetaan virheestä
    #ja suoritetaan valinta-metodi uudestaan.
    else:
        print("Virheelinen syöte. Anna syötteeksi 'L', 'P' tai 'H'.")
        valinta()
        

def haeTietoa():
#Metodi kerää käyttäjältä tiedon, mistä vuodesta ja kuukaudesta tapahtumatietoja haetaan.
#Metodi myös tulostaa kuvan sen kuukauden kalenterista.
    print("Syötä kokonaislukuina vuosi ja kuukausi.")
    vuosi = input("Vuosi: ")
    #Tarkistetaan onko syötetty vuosi kokonaisluku ja ilmoitetaan jos tapahtuu virhe.
    try:
        int(vuosi)
    except:
        print("Virhe. Syötit jotain muuta kuin kokonaislukuja.")
        haeTietoa()
        
    kuukausi = input("Kuukausi: ")
    #Tarkistetaan onko syötetty kuukausi kokonaisluku ja ilmoitetaan jos tapahtuu virhe.
    try:
        int(kuukausi)
    except:
        print("Virhe. Syötit jotain muuta kuin kokonaislukuja.")
        haeTietoa()
    #Kuukausi voi olla vain väliltä 1-12.
    if int(kuukausi) < 1 or int(kuukausi) > 12:
        print("Virheellinen syöte. Anna kuukauden numero väliltä 1-12.")
        haeTietoa()
    print()
    #Tulostetaan kuva käyttäjän valitseman kuukauden kalenterista.
    print(calendar.month(int(vuosi), int(kuukausi)))
    #Siirrytään tulostaTiedot-metodiin, joka tulostaa kuukauden tapahtumatiedot.
    tulostaTiedot(vuosi, kuukausi)
    #Siirrytään takaisin valinta-metodiin
    valinta()
    

def tulostaTiedot(vuosi, kuukausi):
#Metodi lukee JSON-tiedostosta tiettyyn vuoteen ja kuukauteen tallennetut tapahtumatiedot
#ja tulostaa ne käyttäjän nähtäväksi. Metodi myös ilmoittaa jos tapahtumia ei ole. 
    try:
    #Kokeillaan avata kalenteri.json-tiedosto.
        with open("kalenteri.json", "r") as f:
            hajautustaulu = json.load(f)
        if hajautustaulu[vuosi][kuukausi] == {}:
            print("Ei tapahtumia tässä kuussa.")
        #Jos kalenterin kuukauteen on merkattu tapahtumia,
        #tulostetaan ne kaikki käyttäjän nähtäväksi.
        else:
            for i in sorted(hajautustaulu[vuosi][kuukausi]):
                print()
                print(i+". päivä")
                for j in hajautustaulu[vuosi][kuukausi][i]:
                    print("  Tapahtuma:",j)
                    if hajautustaulu[vuosi][kuukausi][i][j] != [""]:
                        print("  Lisätiedot:")
                        for k in hajautustaulu[vuosi][kuukausi][i][j]:
                            print("   -",k)
                    print()
    except:
        print("Ei tapahtumia tässä kuussa.")
    finally:
        print()
        

def lisääLisätietoja(h, vuosi, kuukausi, päivä, tapahtuma):
#Metodi antaa käyttäjän lisätä lisätietoja jo olemassa olevaan tapahtumaan
#tai kirjoittaa tapahtuman lisätiedot kokonaan uudestaan.
    x = (input("""('L') Kirjoita uusia lisätietoja olemassaolevaan tapahtumaan '"""+tapahtuma+"""' 
('K') kirjoita kokonaan uudet lisätiedot
Valinta: """))
    if x == "L":
        print("Lisää tietoja tapahtumaan '"+tapahtuma+"'.")
        #Kerätään käyttäjältä uusia lisätietoja.
        lisätiedot = input("Syötä lisätieto/tiedot pilkuilla erotettuina: ")
        lista = h[vuosi][kuukausi][päivä][tapahtuma]
        #Lisätään uudet lisätiedot listaan, joka sisältää tapahtuman lisätiedot.
        for item in lisätiedot.split(","):
            lista.append(item)
        #Tallennetaan muutokset ja siirrytään takaisin valinta-metodiin.
        with open("kalenteri.json", "w") as f:
            json.dump(h,f)
        print("Tallennettu.")
        valinta()
    #Jos käyttäjä haluaa korvata lisätiedot uusilla, siirrytään takaisin lisääTapahtumia-metodiin.
    elif x == "K":
        pass
    #Jos syöte on jotain muuta kuin sallitut kirjaimet, aloitetaan metodin suoritus uudestaan.
    else:
        print("Virheelinen syöte. Anna syötteeksi 'L' tai 'K'.")
        lisääLisätietoja(h, vuosi, kuukausi, päivä, tapahtuma)
        
    
def lisääTapahtumia():
#Metodi kerää käyttäjältä tiedon, mihin vuoteen, kuukauteen ja päivään uusi tapahtuma lisätään.
#Metodi tallentaa muutokset JSON-tiedostoon.
    #Annetaan muuttujan h arvoksi kalenteri.json-tiedoston sisältämä hajautustaulu
    #tai pelkkä tyhjä hajautustaulu, jos kalenteri.json-tiedostoa ei ole vielä luotu.
    try:
        with open("kalenteri.json", "r") as f:
            h = json.load(f)
    except:
        h = {}

    #Kerätään käyttäjältä vuosi, kuukausi ja päivä ja tarkistetaan
    #että syötteet ovat kokonaislukuja sallituilta väleiltä.
    #Virheen sattuessa aloitetaan metodin suoritus uudestaan.
    print("Syötä kokonaislukuina vuosi, kuukausi ja päivä.")
    vuosi = str(input("Vuosi: "))
    try:
        int(vuosi)
    except:
        print("Virhe. Syötit jotain muuta kuin kokonaislukuja.")
        lisääTapahtumia()
        
    kuukausi = str(input("Kuukausi: "))
    try:
        int(kuukausi)
    except:
        print("Virhe. Syötit jotain muuta kuin kokonaislukuja.")
        lisääTapahtumia()       
    if int(kuukausi) < 1 or int(kuukausi) > 12:
        print("Virheellinen syöte. Anna kuukauden numero väliltä 1-12.")
        lisääTapahtumia()
        
    päivä = str(input("Päivä: "))
    try:
        int(päivä)
    except:
        print("Virhe. Syötit jotain muuta kuin kokonaislukuja.")
        lisääTapahtumia()
    #Päivälle sallittu kokonaislukuväli riippuu kuukaudesta.
    if int(kuukausi) in [1,3,5,7,8,10,12] and (int(päivä) < 1 or int(päivä) > 31):
        print("Virheellinen syöte. Anna päivän numero väliltä 1-31.")
        lisääTapahtumia()
    if int(kuukausi) in [4,6,9,11] and (int(päivä) < 1 or int(päivä) > 30):
        print("Virheellinen syöte. Anna päivän numero väliltä 1-30.")
        lisääTapahtumia()
    if int(kuukausi) == 2 and (int(päivä) < 1 or int(päivä) > 29):
        print("Virheellinen syöte. Anna päivän numero väliltä 1-29.")
        lisääTapahtumia()
        
    tapahtuma = input("Syötä tapahtuma: ")
    #Jos syötetty tapahtuma on jo olemassa kyseisessä päivässä, siirrytään metodiin "lisääLisätietoja"
    #Muussa tapauksessa vaihe ylitetään.
    try:
        if tapahtuma in h[vuosi][kuukausi][päivä]:
            lisääLisätietoja(h, vuosi, kuukausi, päivä, tapahtuma)
    except Exception as virhe:
        pass

    #Käyttäjä voi lisätä tapahtumaan haluamansa määrän lisätietoja. Syötteen voi myös jättää tyhjäksi.
    lisätiedot = input("""Syötä tapahtumaan liittyvä muistutus/muistutukset pilkuilla erotettuina:
""")
    lisätietolista = []
    #Lisätiedot kerätään lisätietolistaan ja asetetaan moniulotteiseen hajautustauluun avaimen
    #h[vuosi][kuukausi][päivä][tapahtuma] arvoksi.
    for item in lisätiedot.split(","):
        lisätietolista.append(item)

    #Jos hajautustaulussa h on jo käyttäjän tämän metodin alussa syöttämät vuosi, kuukausi ja päivä,
    #lisätään päivään uusi tapahtuma, eikä kirjoiteta aiemmin merkittyjen tapahtumien päälle.
    if vuosi in h and kuukausi in h[vuosi] and päivä in h[vuosi][kuukausi]:
        h[vuosi][kuukausi][päivä][tapahtuma] = lisätietolista

    #Jos hajautustaulussa h on jo käyttäjän tämän metodin alussa syöttämät vuosi ja kuukausi,
    #lisätään kuukauteen uusi päivä, eikä kirjoiteta aiemmin merkittyjen päivien päälle.        
    elif vuosi in h and kuukausi in h[vuosi]:
        h[vuosi][kuukausi][päivä] = {
            tapahtuma: lisätietolista
            }
    #Jos hajautustaulussa h on jo käyttäjän tämän metodin alussa syöttämät vuosi,
    #lisätään vuoteen uusi kuukausi, eikä kirjoiteta aiemmin merkittyjen kuukausien päälle.
    elif vuosi in h:
        h[vuosi][kuukausi] = {
                päivä: {
                    tapahtuma: lisätietolista
                    }
                }
    #Muussa tapaukessa tehdään hajautustauluun h uusi vuosi-avain ja sen sisältämät muut tiedot.
    #Kun kalenteriin lisätään ensimmäinen tapahtuma, luodaan siis kalenteri.json-tiedostoon moniulotteinen
    #hajautustaulu h, joka koostuu vuosi-hajautustauluista, joissa on kuukausi-hajautustauluja, joissa on
    #päivä-hajautustauluja, joissa on tapahtuma-avaimia, joissa on lisätietoja listamuodossa.
    else:
        h[vuosi] = {
            kuukausi: {
                päivä: {
                    tapahtuma: lisätietolista
                    }
                }
            }

    #Tallennetaan muutokset ja siirrytään takaisin valinta-metodiin.
    with open("kalenteri.json", "w") as f:
        json.dump(h,f)
    print("Tallennettu.")
    valinta()
    

def poistaPäivä():
#Metodi poistaa JSON-tiedostosta käyttäjän valitseman päivän kaikki tapahtumatiedot.
    #Avataan kalenteri.json-tiedosto ja ilmoitetaan virheestä jos tiedostoa ei ole olemassa.
    try:      
        with open("kalenteri.json", "r") as f:
            hajautustaulu = json.load(f)
    except:
        print("Virhe. Kalenterissa ei ole vielä mitään poistettavaa")
        valinta()

    #Kerätään tiedot poistettavasta päivästä käyttäjän syötteenä.  
    print("Syötä päivämäärä, jonka merkinnät haluat poistaa.")
    vuosi = input("Vuosi: ")
    kuukausi = input("Kuukausi: ")
    päivä = input("Päivä: ")

    #Poistetaan hajautustaulusta käyttäjän syöttämän päivän sisältö.
    #Ilmoitetaan virheestä ja palataan takaisin valinta-metodiin, jos
    #hajautustaulussa ei ole kyseistä päivää.
    try:
        del hajautustaulu[str(vuosi)][str(kuukausi)][str(päivä)]
    except:
        print("Virhe. Tarkista, että kirjoitit päivän numeron oikein.")
        print("Et voi poistaa päivää, jossa ei ole yhtään tapahtumaa.")
        valinta()

    #Tallennetaan muutokset ja siirrytään takaisin valinta-metodiin.    
    with open("kalenteri.json", "w") as f:
        json.dump(hajautustaulu,f)
    print("Poistettu.")
    valinta()
    

def viikonpäivä(y):
#Metodi saa todelliseksi arvokseen viikonpäivää vastaavan numeron
#ja palautaa viikonpäivän nimen merkkijonona
    if y == 0:
        return "maanantai"
    if y == 1:
        return "tiistai"
    if y == 2:
        return "keskiviikko"
    if y == 3:
        return "torstai"
    if y == 4:
        return "perjantai"
    if y == 5:
        return "lauantai"
    if y == 6:
        return "sunnuntai"
    

def aloitus():
#Metodi suoritetaan aina ensimmäisenä kun ohjelma souritetaan
#ja se tulostaa ruudulle senhetkisen kuukauden tiedot.
    #Selvitetään ohjelman avaushetken päivämäärä ja aika datetime-kirjaston avulla.
    #Asetetaan muuttujaan x merkkijono joka on siis muotoa 'vvvv-kk-pp xx:xx:xx.xxxxxx'.
    x = str(datetime.datetime.now())
    #Asetetaan muuttujaan y viikonpäivän numero seuraavan lauseen avulla.
    y = datetime.datetime.now().weekday()
    #Asetetaan tunti muuttujaan käynnistyshetken tunti hakemalla x-merkkijonosta oikeat merkit.
    #Tervehditään käyttäjää kellonaikaan sopivalla tavalla.
    tunti = int(x[11:13])
    if tunti >= 5 and tunti < 12:
        print("Hyvää huomenta käyttäjä.")
    elif tunti >= 12 and tunti < 18:
        print("Hyvää päivää käyttäjä.")
    elif tunti >= 18 and tunti < 24:
        print("Hyvää iltaa käyttäjä.")
    else:
        print("Nyt nukkumaan käyttäjä!")

    #Tulostetaan päivämäärä ja kellonaika nappaamalla x-merkkijonosta oikeat numerot.
    print("Päivämäärä: {} {}.{}.{}".format(viikonpäivä(y), x[8:10], x[5:7], x[0:4]))
    print("Kellonaika:", x[11:16])
    print()
    #Määritellään muuttujien vuosi ja kuukausi arvot x-merkkijonon avulla.
    vuosi = x[0:4]
    kuukausi = x[5:7]
    #Tulostetaan kuva kuukauden kalenterista calendar-kirjaston avulla.
    print(calendar.month(int(vuosi), int(kuukausi)))
    #Tulostetaan myös kuukauden tapahtumat tulostaTiedot-metodin avulla
    tulostaTiedot(vuosi, kuukausi)
    #Tulostetaan lukujärjestys.
    tulostus()

    valinta()


#Aloitetaan ohjelman suoritus
aloitus()

