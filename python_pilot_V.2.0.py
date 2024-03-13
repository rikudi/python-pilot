import os, time
from geopy.distance import geodesic
from Komponentit.Valikot import valikko
from Komponentit.Tietokanta import palaute, sql_koodit
from Komponentit.Muut.ohjeistus import ohjeistus
from Komponentit.Muut.kirjotin import print_nopea, print_normal, print_hidas
from geopy.geocoders import Nominatim
from colorama import init, Fore, Style


# GLOBAL-MUUTTUJAT

init() #colorama init
start_lat = None
start_lon = None
kierros_count = 1
pelaaja_id = None
lahimmat_lentokentat = None
game_over = False
venaja_counter = 0
ukraina_counter = 0
saksa_counter = 0

# NÄPPÄIMET
suunnat = {
            "1": 225,       # Lounas
            "2": 180,       # Etelä
            "3": 135,       # Kaakko
            "4": 270,       # Länsi
            "6": 90,        # Itä
            "7": 315,       # Luode
            "8": 0,         # Pohjoinen
            "9": 45,        # Koillinen
            "KP1": 225,     # Lounas
            "KP2": 180,     # Etelä
            "KP3": 135,     # Kaakko
            "KP4": 270,     # Länsi
            "KP6": 90,      # Itä
            "KP7": 315,     # Luode
            "KP8": 0,       # Pohjoinen
            "KP9": 45,      # Koillinen
            " ": None       # Valikko
        }

# GAME_LOOP - Pelin ydinfunktio jota kutsutaan niin kauan kunnes game_over = TRUE
def game_loop():
    # Tietokannasta saadut arvot asetetaan global muuttujiin ja niitä päivitetään pelin aikana
    global game_over, venaja_counter, ukraina_counter, saksa_counter, start_lat, start_lon
    tiedot = sql_koodit.mysql_query_tiedot(pelaaja_id)
    start_lat, start_lon = tiedot[0][0], tiedot[0][1]

    print_normal("Peli alkaa... Lentokoneesi on noussut lentokentältä ilmaan.\n")
    time.sleep(2.5)
    while not game_over:
        kierros()
        if game_over:
            sql_koodit.mysql_game_over(pelaaja_id)
            venaja_counter = 0
            ukraina_counter = 0
            saksa_counter = 0
            print_normal("Peli päättyi! Lentokoneesi tuhoutui.")
            kysymys = input("Haluatko pelata uudestaan?[kyllä/ei]: ")
            if kysymys == "ei":
                print_normal("Näkemiin!")
                quit()
            else:
                print_hidas("Aloitetaan alusta...")
                time.sleep(1)
                game_over = False
                game_loop()

# ILMATILAN TARKISTUS JA TAPAHTUMIEN KÄSITTELY
def ilma_tilatarkistus(pelaaja_id):
    global game_over, venaja_counter, ukraina_counter, saksa_counter
    if venaja_counter >= 4 or ukraina_counter >= 2:
        print(Fore.RED, "Lentokoneesi ammuttiin alas.", Style.RESET_ALL)
        game_over = True

    lat, lon = sql_koodit.mysql_hae_koordinaatit(pelaaja_id)
    geolocator = Nominatim(user_agent="testi")
    location = geolocator.reverse((lat, lon), language="fi")

    if not game_over:
        if location is None:
            print_nopea("Olet kansainvälisessä ilmatilassa.")
            return

        elif location.raw['address']['country'] == "Venäjä":
            print(Fore.RED,
                  "\nOlet Venäjän ilmatilassa. Poistu enintään kolmen kierroksen aikana tai lentokoneesi ammutaan alas",
                  Style.RESET_ALL)
            venaja_counter += 1
            print(Fore.RED, "COUNTER", venaja_counter, Style.RESET_ALL)
            return

        elif location.raw['address']['country'] == "Ukraina":
            print(Fore.RED, "\nOlet Ukrainan ilmatilassa, poistu enintään kahden kierroksen aikana tai lentokoneesi ammutaan alas",
                  Style.RESET_ALL)
            ukraina_counter += 1
            print(Fore.RED, "COUNTER", ukraina_counter, Style.RESET_ALL)
            return

        elif location.raw['address']['country'] == "Saksa":
            print_nopea("\nOlet maan Saksa ilmatilassa")
            saksa_counter += 1
            if saksa_counter == 1:
                print_normal("\nSinulla tulee pakottava tarve saada rinkeliä, laskeudut lähimmälle lentokentälle syömään.")
                time.sleep(2)
                print_normal("\nLaskeudutaan...")
                time.sleep(2)
                print_normal("\nMasu on täynnä, kone nousee takaisin ilmaan.\n")
                time.sleep(2)
                sql_koodit.mysql_update_kierrokset(pelaaja_id)
                return
            return
        else:
            print("\nOlet maan", location.raw['address']['country'], "ilmatilassa.\n")
            return


# POLTTOAINEEN PÄIVITYS JA KÄSITTELY
def polttoaine_mittaus(pelaaja_id):
    global game_over
    fuel = sql_koodit.mysql_hae_polttoaine(pelaaja_id)
    if not game_over:
        if fuel == 40:
            print(Fore.RED, "Varoitus! Polttoainetta jäljellä 40%.", Style.RESET_ALL)
        elif fuel == 20:
            print(Fore.RED, "Varoitus! Polttoainetta jäljellä 20%.", Style.RESET_ALL)
        elif fuel <= 0:
            print(Fore.RED, "Lentokoneesi putoaa.", Style.RESET_ALL)
            game_over = True

# PELAAJAN LIIKE JA SIJAINNIN PÄIVITYS ###
def liikuta_pelaajaa(suunta):
    global start_lat, start_lon
    if not game_over:
        print_normal("\nLasketaan uudet koordinaatit...\n")
        sijainti = (start_lat, start_lon)
        uusi_sijainti = geodesic(kilometers=200).destination(sijainti, suunta)
        start_lat, start_lon = uusi_sijainti.latitude, uusi_sijainti.longitude
        sql_koodit.mysql_update_coordinates(pelaaja_id, start_lat, start_lon)

# KIERROS
def kierros():
    global pelaaja_id, kierros_count, lahimmat_lentokentat, game_over
    tiedot = sql_koodit.mysql_query_tiedot(pelaaja_id)                          # sql tiedot -kysely
    lahimmat_lentokentat = sql_koodit.mysql_query_close_airports(pelaaja_id)    # päivitä lähimmät kentät -kysely
    # Print tiedot ruudulle kierroksen alussa
    for rivit in tiedot:
        location_lat, location_lon, fuel = rivit
        print_nopea(f"\n[Sijainti]: Latitude {location_lat} | Longitude {location_lon} ")
        print_nopea(f"\n[Polttoaine]: {fuel}%\n")
    print_nopea("\n[SPACE]: Listaa lähimmät lentokentät [1]: Lounas [2]: Etelä [3]: Kaakko [4]: Länsi [6]: Itä [7]: Luode [8]: Pohjoinen [9]: Koillinen \n")
    syote = str(input(f"Syötä ilmansuunta: "))
    while syote not in suunnat:
        print("Yritä uudelleen")
        syote = str(input(f"Syötä ilmansuunta: "))
    # Jos annettu input on välilyönti => avaa valikon.
    if syote == " ":
        # Palauttaa valikosta valitun arvon muuttujaan "valinta". Jos valinta == None => Kutsutaan kierros() uudestaan.
       valinta = valikko.open_menu(lahimmat_lentokentat)
       if valinta is not None:
           if valinta == "LTAC":
               print_normal("Olet laskeutunut Ankaraan. Peli päättyy.\n")
               game_over = True
               palaute.palaute(pelaaja_id)
               sql_koodit.mysql_game_over(pelaaja_id)
               kysymys2 = input("\nHaluatko pelata uudestaan?[kyllä/ei]: ")
               if kysymys2 == "ei":
                   print("Näkemiin!")
                   time.sleep(2)
                   quit()
               else:
                   print("Aloitetaan alusta...")
                   time.sleep(5)
                   game_over = False
                   game_loop()
           print_normal(f"Valittu kenttä johon laskeudutaan (ICAO): {valinta}")
           sql_koodit.mysql_update_laskeutuminen(pelaaja_id, valinta)
           time.sleep(1)
           print_normal("\nTankataan.....")
           time.sleep(2)
           print_normal("\nLentokone nousee takaisin ilmaan.\n")
           time.sleep(2)
           os.system('cls')     # tyhjennetään konsoli
           ilma_tilatarkistus(pelaaja_id)
           sql_koodit.etaisyys_ankara(pelaaja_id)
           kierros_count += 1
    else:
        # Päivittää pelaajan uuden sijainnin ja kutsuu tarvittavat sql-kyselyt
        suunta = suunnat.get(syote)
        print("\n##########################################################################")
        liikuta_pelaajaa(suunta)
        sql_koodit.mysql_update_kierrokset(pelaaja_id)
        sql_koodit.mysql_update_polttoaine(pelaaja_id)
        ilma_tilatarkistus(pelaaja_id)
        sql_koodit.etaisyys_ankara(pelaaja_id)
        polttoaine_mittaus(pelaaja_id)

# ALOITUS
ohjeistus()

while True:
    pelaaja_id = input("Anna pelaajatunnus: ")
    while pelaaja_id == "" or pelaaja_id == " ":
        print("Tyhjää nimeä ei voi olla, syötä uusi tai olemassaoleva nimi")
        pelaaja_id = input("Anna pelaajatunnus: ")
    pelaaja_listassa = sql_koodit.mysql_id_tarkistus(pelaaja_id)
    if pelaaja_listassa:
        print(f"Nimi jo tietokannassa, jatketaan nimellä: '{pelaaja_id}'")
        time.sleep(2.5)
        os.system('cls')
        break
    else:
        print(f"Tervetuloa pelaamaan: '{pelaaja_id}'!")
        sql_koodit.mysql_insert_alkuarvot(pelaaja_id)
        os.system('cls')
        break

game_loop()