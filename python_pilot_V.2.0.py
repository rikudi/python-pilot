from geopy.distance import geodesic
from Komponentit import sql_koodit
from Komponentit.Valikot import valikko
from Komponentit import etaisyys_ankarasta, polttoaine_mittaus, palaute
import time
import mysql.connector
from geopy.geocoders import Nominatim

yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='python_pilot',
    user='root',
    password='admin',
    autocommit=True
)

start_lat = None
start_lon = None
kierros_count = 1
pelaaja_id = None
lahimmat_lentokentat = None
game_over = False
venaja_counter = 0
ukraina_counter = 0
saksa_counter = 0


suunnat = {
            "1": 225,       # Lounas
            "2": 180,       # Etelä
            "3": 135,       # Kaakko
            "4": 270,       # Länsi
            "6": 90,        # Itä
            "7": 315,       # Luode
            "8": 0,         # Pohjoinen
            "9": 45,        # Koillinen
            "H": 'nayta_ohjeet',
            "KP1": 225,     # Lounas
            "KP2": 180,     # Etelä
            "KP3": 135,     # Kaakko
            "KP4": 270,     # Länsi
            "KP6": 90,      # Itä
            "KP7": 315,     # Luode
            "KP8": 0,       # Pohjoinen
            "KP9": 45,      # Koillinen
        }

def ilma_tilatarkistus(pelaaja_id):
    global game_over, venaja_counter, ukraina_counter, saksa_counter
    if venaja_counter >= 4 or ukraina_counter >= 2:
        print("Lentokoneesi ammuttiin alas.")
        game_over = True

    sql = f"SELECT location_lat, location_lon FROM game WHERE id = '{pelaaja_id}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    x = kursori.fetchone()
    lat, lon = x

    geolocator = Nominatim(user_agent="testi")
    location = geolocator.reverse((lat, lon), language="fi")

    if location is None:
        print("Olet kansainvälisessä ilmatilassa.")
        return

    elif location.raw['address']['country'] == "Venäjä":
        print("Olet Venäjän ilmatilassa. Poistu enintään kolmen kierroksen aikana tai lentokoneesi ammutaan alas")
        venaja_counter += 1
        print("COUNTER",venaja_counter)
        return

    elif location.raw['address']['country'] == "Ukraina":
        print("Olet Ukrainan ilmatilassa, poistu enintään kahden kierroksen aikana tai lentokoneesi ammutaan alas")
        ukraina_counter += 1
        print("COUNTER",ukraina_counter)
        return

    elif location.raw['address']['country'] == "Saksa":
        print("Olet maan Saksa ilmatilassa")
        saksa_counter += 1
        if saksa_counter == 1:
            print("Sinulla tulee pakottava tarve saada rinkeliä, laskeudut lähimmälle lentokentälle syömään.")
            print("Laskeudutaan...")
            time.sleep(2)
            print("Masu on täynnä, kone nousee takaisin ilmaan.")
            time.sleep(2)
            sql_koodit.mysql_update_kierrokset(pelaaja_id)
            return
        return

    else:
        print("Olet maan", location.raw['address']['country'], "ilmatilassa.")
        return
def polttoaine_mittaus(pelaaja_id):
    global game_over
    sql = f"SELECT fuel FROM game WHERE id = '{pelaaja_id}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    x = kursori.fetchone()
    x = (x[0])

    if x == 40:
        print("Varoitus! Polttoainetta jäljellä 40%.")
    elif x == 20:
        print("Varoitus! Polttoainetta jäjellä 20%")
    elif x <= 0:
        print("Polttoaine loppui! Lentokoneesi putoaa alas.\n")
        game_over = True
# Peli ydin-looppi.
def game_loop():
    global game_over, venaja_counter, ukraina_counter, start_lat, start_lon
    tiedot = sql_koodit.mysql_query_tiedot(pelaaja_id)
    start_lat, start_lon = tiedot[0][0], tiedot[0][1]

    print("Peli alkaa... Lentokoneesi on noussut lentokentältä ilmaan.\n")
    #time.sleep(2.5)
    while not game_over:

        time.sleep(1)  # 0.5s tauko looppien välillä
        kierros()
        if game_over:
            sql_koodit.mysql_game_over(pelaaja_id)
            print("Peli päättyi! Lentokoneesi tuhoutui.")
            kysymys = input("Haluatko pelata uudestaan?[kyllä/ei]: ")
            if kysymys == "ei":
                print("Näkemiin!")
                quit()
            else:
                print("Aloitetaan alusta...")
                time.sleep(1)
                game_over = False
                game_loop()

# Liikuttaa pelaajaa valinnan perusteella
def liikuta_pelaajaa(suunta):
    global start_lat, start_lon
    print("Lasketaan uudet koordinaatit...\n")
    sijainti = (start_lat, start_lon)
    uusi_sijainti = geodesic(kilometers=200).destination(sijainti, suunta)
    start_lat, start_lon = uusi_sijainti.latitude, uusi_sijainti.longitude
    sql_koodit.mysql_update_coordinates(pelaaja_id, start_lat, start_lon)

def kierros():
    global pelaaja_id, kierros_count, lahimmat_lentokentat, game_over
    tiedot = sql_koodit.mysql_query_tiedot(pelaaja_id)                          # sql tiedot -kysely
    lahimmat_lentokentat = sql_koodit.mysql_query_close_airports(pelaaja_id)    # päivitä lähimmät kentät -kysely
    # Print tiedot ruudulle kierroksen alussa
    for rivit in tiedot:
        location_lat, location_lon, fuel = rivit
        print(f"Sijainti: Latitude {location_lat} ja Longitude {location_lon}")
        print(f"Polttoaine: {fuel} \n")
    print("[SPACE]: Listaa lähimmät lentokentät [1]: Lounas [2]: Etelä [3]: Kaakko [4]: Länsi [6]: Itä [7]: Luode [8]: Pohjoinen [9]: Koillinen \n")
    syote = str(input(f"Syötä ilmansuunta: "))
    while syote != "1" and syote != "2" and syote != "3" and syote != "4" and syote != "5" and syote != "6" and syote != "7" and syote != "8" and syote != "9" and syote != " ":
        print("Yritä uudelleen")
        syote = str(input(f"{kierros_count}. Kierros. Syötä ilmansuunta: "))
    # Jos annettu input on välilyönti => avaa valikon.
    if syote == " ":
        # Palauttaa pelaajan valitseman vaihtoehdon. Jos ei valintaa (Exit) => Kutsutaan kierros() uudestaan.
       valinta = valikko.open_menu(lahimmat_lentokentat)
       if valinta is not None:
           if valinta == "LTAC":
               print("Olet laskeutunut Ankaraan. Peli päättyy.")
               game_over = True
               palaute.palaute(pelaaja_id)
               sql_koodit.mysql_game_over(pelaaja_id)
               kysymys2 = input("Haluatko pelata uudestaan?[kyllä/ei]: ")
               if kysymys2 == "ei":
                   print("Näkemiin!")
                   quit()
               else:
                   print("Aloitetaan alusta...")
                   time.sleep(5)
                   game_over = False
                   game_loop()

           print("Valittu kenttä johon laskeudutaan (ICAO): ", valinta)
           sql_koodit.mysql_update_laskeutuminen(pelaaja_id, valinta)
           time.sleep(1)
           print("Tankataan.....")
           time.sleep(2)
           print("Lentokone nousee takaisin ilmaan.")
           ilma_tilatarkistus(pelaaja_id)
           etaisyys_ankarasta.etaisyys_ankara(pelaaja_id)
           kierros_count += 1



    else:
        suunta = suunnat.get(syote)
        liikuta_pelaajaa(suunta)
        sql_koodit.mysql_update_kierrokset(pelaaja_id)
        sql_koodit.mysql_update_polttoaine(pelaaja_id)
        ilma_tilatarkistus(pelaaja_id)
        etaisyys_ankarasta.etaisyys_ankara(pelaaja_id)
        polttoaine_mittaus(pelaaja_id)


def ohjeistus():
    ohje = """
Tervetuloa pelaamaan Python Pilottia!
Pelin tavoitteena on saapua Ankaran lentokentälle mahdollisimman vähin siirroin, lähtöpaikkasi on Helsinki-Vantaan lentokenttä. 
Yhdellä siirrolla lentokone liikkuu 200km haluttuun ilmansuuntaan.
Lentokone on täysin tankattu pelin alussa, jolla voit kulkea maksimissaan 1000 kilometriä. Aina kun laskeudut lähimmälle lentokentälle,
lentokoneen tankki täytetään 100 %.

Pelin näppäimet :
Num 1: Lounas
Num 2: Etelä
Num 3: Kaakko
Num 4: Länsi
Num 6: Itä
Num 7: Luode
Num 8: Pohjoinen
Num 9: Koillinen
SPACE: Avaa valikon, jossa on viisi lähintä lentokenttää. Kentät on numeroitu 1–5. Painamalla halutun lentokentän numeroa, kone laskeutuu
sinne.
H: ohjeet ja opasteet

"""
    print(ohje)

ohjeistus()

while True:
    pelaaja_id = input("Anna pelaajatunnus: ")
    while pelaaja_id == "" or pelaaja_id == " ":
        print("Tyhjää nimeä ei voi olla, syötä uusi tai olemassaoleva nimi")
        pelaaja_id = input("Anna pelaajatunnus: ")
    pelaaja_listassa = sql_koodit.mysql_id_tarkistus(pelaaja_id)
    if pelaaja_listassa:
        print(f"Nimi jo tietokannassa, jatketaan nimellä: '{pelaaja_id}'")
        break
    else:
        print(f"Tervetuloa pelaamaan: '{pelaaja_id}'!")
        sql_koodit.mysql_insert_alkuarvot(pelaaja_id)
        break


game_loop()