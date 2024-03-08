from Komponentit.Tietokanta import sql_koodit
from Komponentit.Valikot import valikko
import time

kierros_count = 1
pelaaja_id = None
lahimmat_lentokentat = None
koordinaatit = None

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

# Peli ydin-looppi.
def game_loop():
    running = True
    game_over = False

    print("Peli alkaa... Lentokoneesi on noussut Helsinki-Vantaan lentokentältä ilmaan.\n")
    #time.sleep(2.5)
    while running:
        time.sleep(0.5)  # 0.5s tauko looppien välillä
        kierros()


# Liikuttaa pelaajaa valinnan perusteella
'''def liikuta_pelaajaa(suunta):
    global start_lat, start_lon
    print(f"Pelaaja valitsi suunnan: {suunta}")
    print("Lasketaan uudet koordinaatit...")
    sijainti = (start_lat, start_lon)
    uusi_sijainti = geodesic(kilometers=200).destination(sijainti, suunta)
    start_lat, start_lon = uusi_sijainti.latitude, uusi_sijainti.longitude
    print(f"Uudet koordinaatit: ({start_lat}, {start_lon})")'''

def kierros():
    global pelaaja_id, kierros_count, lahimmat_lentokentat, koordinaatit
    tiedot = sql_koodit.mysql_query_tiedot(pelaaja_id)                          # sql tiedot -kysely
    koordinaatit = tiedot[0][0], tiedot[0][1]                                   # longitude latitude
    lahimmat_lentokentat = sql_koodit.mysql_query_close_airports(pelaaja_id)    # päivitä lähimmät kentät -kysely
    maali_tiedot = sql_koodit.mysql_hae_maali(pelaaja_id, koordinaatit)         # hakee etäisyyden ankarasta, ilmatilan yms

    print("[SPACE]: Listaa lähimmät lentokentät [1]: Lounas [2]: Etelä [3]: Kaakko [4]: Länsi [6]: Itä [7]: Luode [8]: Pohjoinen [9]: Koillinen \n")
    syote = str(input(f"{kierros_count}. Kierros. Syötä ilmansuunta: "))
    # Jos annettu input on välilyönti => avaa valikon.
    if syote == " ":
        # Palauttaa pelaajan valitseman vaihtoehdon. Jos ei valintaa (Exit) => Kutsutaan kierros() uudestaan.
       valinta = valikko.open_menu(lahimmat_lentokentat)
       if valinta is not None:
           print("valittu kenttä johon laskeudutaan (ICAO): ", valinta)

           ## tässä kohtaa ajetaan laskeutuminen
           '''suunta = suunnat.get(syote)
           liikuta_pelaajaa(suunta)
           kierros_count += 1'''
    else:
        suunta = suunnat.get(syote)
        #liikuta_pelaajaa(suunta)
        kierros_count += 1


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
    kysy = input("Oletko valmis aloittamaan?[kyllä = ENTER]: ")
    pelaaja_id = input("Anna pelaajatunnus: ")
    pelaaja_listassa = sql_koodit.mysql_id_tarkistus(pelaaja_id)
    if pelaaja_listassa:
        print(f"Nimi jo tietokannassa, jatketaan nimellä: '{pelaaja_id}'")
    else:
        print(f"Tervetuloa pelaamaan: '{pelaaja_id}'!")
        sql_koodit.mysql_insert_alkuarvot(pelaaja_id)
    if kysy == "":
        game_loop()
    else:
        continue