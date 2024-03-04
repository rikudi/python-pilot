from Komponentit.Kontrolleri import pelaaja_kontrolleri
from geopy.distance import geodesic
import time

### Helsinki Vantaa koordinaatit ###
start_lat = 60.3172
start_lon = 24.963301
####################################

# Peli ydin-looppi.
def game_loop():
    running = True
    game_over = False

    print("Peli alkaa... Lentokoneesi on noussut Helsinki-Vantaan lentokentältä ilmaan.")
    time.sleep(2.5)
    print("Mihin suuntaat? Valitse yksi ilmansuunta: ")
    while running:
        time.sleep(0.5)  # 0.5s tauko looppien välillä

      # pelin logiikkaa tänne
      # vaatii varmaan jonkunlaisen kierrosfunktion

        if game_over:
            running = False

######################################################################################################################
# Käsittelee logiikkaa kun nappeja painetaan. Funktio syötetään parametrina pelaaja_kontrolleri instanssiin (rivi 41),
# jonka avulla pelaaja_kasittelija funktio kutsutaan vain kun näppäintä on painettu. (key)-parametrin tieto saadaan
# pelaaja_kontrollerin riviltä 55.
def pelaaja_kasittelija(key):
    global start_lat, start_lon       # Rivi 6, 7
    if key in kontrolleri.nappaimet:  # Jos pelaajan syöte löytyy näppäimistä -> asetetaan näppäimen arvo suunnaks
        suunta = kontrolleri.nappaimet[key]
        print(f"Pelaajan valitsema suunta asteina: ", suunta)  # voi poistaa myöhemmin

        # Päivitetään koordinaatit global muuttujiin
        start_lat, start_lon = laske_uudet_koordinaatit(start_lat, start_lon, suunta)
        print(f"Uudet koordinaatit: ({start_lat}, {start_lon})")

# Instanssi pelaaja_kontrollerista. (ohjelma alkaa kuunnella pelaajan inputtia)
kontrolleri = pelaaja_kontrolleri.PelaajaKontrolleri(pelaaja_kasittelija)

# Funktio laskee uuet koordinaatit
def laske_uudet_koordinaatit(latitude, longitude, suunta_asteina):
    print("Lasketaan uudet koordinaatit...")
    sijainti = (latitude, longitude)
    uusi_sijainti = geodesic(kilometers=200).destination(sijainti, suunta_asteina)
    return uusi_sijainti.latitude, uusi_sijainti.longitude

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
    if kysy == "":
        game_loop()
    else:
        continue