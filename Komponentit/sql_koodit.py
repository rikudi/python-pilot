# Tällä koodilla yhdistetään tietokantaan. Voisi luoda erillisen käyttäjän #
# tietokantaan peliä varten #
import mysql.connector
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='python_pilot',  # vaiha
    user='root',
    password='admin',         # vaiha
    autocommit=True
)

# Funktio polttoaineen vähentämiseen kierroksen jälkeen #
def mysql_update_polttoaine(nimi):
    sql = f"UPDATE game SET fuel = fuel - 20 WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return
#mysql_update_polttoaine(nimi)

# funktio pelaajan nimen lisäämiseen tietokantaan ja pelaajalle syötetään alkuarvot tietokantaan"

def mysql_game_over(pelaaja_tunnus):
    sql = f"UPDATE game SET fuel = 100, location_lat = 60.3172, location_lon = 24.963301, kierrokset = 0 WHERE id = '{pelaaja_tunnus}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)

def mysql_insert_alkuarvot(nimi):
    sql = f"INSERT INTO game (id, fuel, location_lat, location_lon, kierrokset) VALUES ('{nimi}', 100, 60.3172, 24.963301, 0)"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return
#mysql_insert_alkuarvot(nimi)

# Funktio koordinaattien päivittämiseen tietokantaan #
def mysql_update_coordinates(nimi, latitude, longitude):
    sql = f"UPDATE game set location_lat = '{latitude}', location_lon = '{longitude}' WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return
#mysql_update_coordinates(nimi, latitude, longitude)

# Funktio lähimpien lentokenttien löytämiseen tietokannasta #
def mysql_query_close_airports(nimi):
    sql = f"SELECT name AS lentokentät, ident AS icao FROM airport CROSS JOIN game WHERE type IN('medium_airport', 'large_airport') AND latitude_deg BETWEEN location_lat - 3 and location_lat + 3 AND longitude_deg BETWEEN location_lon - 3 and location_lon + 3 and game.id = '{nimi}' AND CHAR_LENGTH(ident)=4 ORDER BY name"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    mytiedot = kursori.fetchall()
    return mytiedot
'''for x in mysql_query_close_airports():
    print(x)'''

# Funktio kierrosten lisäämiseen tietokantaan #
def mysql_update_kierrokset(nimi):
    sql = f"UPDATE game SET kierrokset = kierrokset + 1 WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return
#mysql_update_kierrokset(nimi)

# Funktio lentokentälle laskeutumiseen ja bensan täyttämiseen#
def mysql_update_laskeutuminen(nimi, ICAO):
    sql = f"UPDATE game CROSS JOIN airport set location_lat = latitude_deg, location_lon = longitude_deg, fuel=100 where ident = '{ICAO}' and game.id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return
#mysql_update_laskeutuminen(nimi, ICAO)

# Funktio pelaajan tietojen printtaamiseen. Latitude, longitude, maa, polttoaine, etäisyys Ankaraan, #
# mahollinen lentokenttä, mahollinen tapahtuma #
def mysql_query_tiedot(nimi):
    sql = f"SELECT location_lat, location_lon, fuel FROM game WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    mytiedot = kursori.fetchall()
    return mytiedot

def mysql_hae_maali(nimi, koordinaatit):
    geolocator = Nominatim(user_agent=f"{nimi}")
    location = geolocator.reverse(koordinaatit, language="fi")
    if location == None:
        print("Olet kansainvälisessä ilmatilassa")
    else:
        print("Olet maan", location.raw['address']['country'] + " ilmatilassa")

    print("Koordinaatit ja bensa:")
    for x in mysql_query_tiedot(nimi):
        print(x)

    # koordinaatit etsitty tietokannasta ja laitettu suoraan tohon #
    Ankara = (40.128101348899996, 32.995098114)

    matka = geodesic(koordinaatit, Ankara).km
    print(matka, "Kilometriä ankaraan\n")

# Funktio nimen tarkistamiseen tietokannasta #

#thelist = []
def mysql_id_tarkistus(nimi):
    sql = f"SELECT id FROM game WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tiedot = kursori.fetchall()

    # Loopataan tiedoista saatu vastaus (pelaajan id) ja muutetaan stringiksi.
    # jos funktion parametrina saadun nimen perusteella lista on tyhjä => kyseessä uusi pelaaja
    lista = [str(rivi[0]) for rivi in tiedot]
    return lista