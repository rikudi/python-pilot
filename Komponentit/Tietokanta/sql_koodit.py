# Tällä koodilla yhdistetään tietokantaan. Voisi luoda erillisen käyttäjän #
# tietokantaan peliä varten #
import mysql.connector
from geopy.distance import great_circle
yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='python_pilot',  # vaiha
    user='root',
    password='alakatomunsalasanaa',         # vaiha
    autocommit=True
)

# Funktio polttoaineen vähentämiseen kierroksen jälkeen #
def mysql_update_polttoaine(nimi):
    sql = f"UPDATE game SET fuel = fuel - 20 WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

# Funktio pelaajan nimen lisäämiseen tietokantaan ja pelaajalle syötetään alkuarvot tietokantaan"
def mysql_game_over(pelaaja_tunnus):
    sql = f"UPDATE game SET fuel = 100, location_lat = 60.3172, location_lon = 24.963301, kierrokset = 0 WHERE id = '{pelaaja_tunnus}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)

# Funktio joka tallentaa uuden pelaajan alkutilastot tietokantaan
def mysql_insert_alkuarvot(nimi):
    sql = f"INSERT INTO game (id, fuel, location_lat, location_lon, kierrokset) VALUES ('{nimi}', 100, 60.3172, 24.963301, 0)"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

# Funktio koordinaattien päivittämiseen tietokantaan #
def mysql_update_coordinates(nimi, latitude, longitude):
    sql = f"UPDATE game set location_lat = '{latitude}', location_lon = '{longitude}' WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

# Funktio lähimpien lentokenttien löytämiseen tietokannasta #
def mysql_query_close_airports(nimi):
    sql = f"SELECT name AS lentokentät, ident AS icao FROM airport CROSS JOIN game WHERE type IN('medium_airport', 'large_airport') AND latitude_deg BETWEEN location_lat - 3 and location_lat + 3 AND longitude_deg BETWEEN location_lon - 3 and location_lon + 3 and game.id = '{nimi}' AND CHAR_LENGTH(ident)=4 ORDER BY name"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    mytiedot = kursori.fetchall()
    return mytiedot

# Funktio kierrosten lisäämiseen tietokantaan #
def mysql_update_kierrokset(nimi):
    sql = f"UPDATE game SET kierrokset = kierrokset + 1 WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

# Funktio lentokentälle laskeutumiseen ja bensan täyttämiseen#
def mysql_update_laskeutuminen(nimi, ICAO):
    sql = f"UPDATE game CROSS JOIN airport set location_lat = latitude_deg, location_lon = longitude_deg, fuel=100 where ident = '{ICAO}' and game.id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

# Funktio pelaajan tietojen printtaamiseen. Latitude, longitude, maa, polttoaine, etäisyys Ankaraan, #
# mahollinen lentokenttä, mahollinen tapahtuma #
def mysql_query_tiedot(nimi):
    sql = f"SELECT location_lat, location_lon, fuel FROM game WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    mytiedot = kursori.fetchall()
    return mytiedot

# Funktio nimen tarkistamiseen tietokannasta #
def mysql_id_tarkistus(nimi):
    sql = f"SELECT id FROM game WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tiedot = kursori.fetchall()

    # Loopataan tiedoista saatu vastaus (pelaajan id) ja muutetaan stringiksi.
    # jos funktion parametrina saadun nimen perusteella lista on tyhjä => kyseessä uusi pelaaja
    lista = [str(rivi[0]) for rivi in tiedot]
    return lista

def mysql_hae_koordinaatit(nimi):
    sql = f"SELECT location_lat, location_lon FROM game WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    x = kursori.fetchone()
    lat, lon = x
    return lat, lon

def mysql_hae_polttoaine(nimi):
    sql = f"SELECT fuel FROM game WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    x = kursori.fetchone()
    x = (x[0])
    return x

# Funktio joka laskee etäisyyden Ankaran lentokentän ja pelaajan välillä
def etaisyys_ankara(pelaaja_id):
    sql = f"SELECT location_lat, location_lon FROM game WHERE id = '{pelaaja_id}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()

    nykyinen_sijainti = (tulos[0][0], tulos[0][1])
    ankara = (40.128101348899996, 32.995098114)
    print("\nEtäisyys määränpäästä:", round(great_circle(nykyinen_sijainti,ankara).kilometers),"km")

def palaute(pelaaja_id):
    sql = f"SELECT kierrokset, high_score FROM game WHERE id = '{pelaaja_id}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    kierrokset = (tulos[0])
    high_score = (tulos[1])
    kilometrit = kierrokset * 200

    if high_score == 0 or high_score > kierrokset:
        print("Uusi ennätys!")
        if kilometrit <= 2600:
            print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli erinomainen!")
        elif 2600 < kilometrit <= 3200:
            print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli hyvä!")
        elif 3200 < kilometrit <= 4000:
            print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli tyydyttävä!")
        else:
            print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli huono!")

        sql_high_score = f"UPDATE game SET high_score = {kierrokset} WHERE id = '{pelaaja_id}'"
        kursori = yhteys.cursor()
        kursori.execute(sql_high_score)

    elif high_score < kierrokset:
        if kilometrit <= 2600:
            print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli erinomainen!")
        elif 2600 < kilometrit <= 3200:
            print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli hyvä!")
        elif 3200 < kilometrit <= 4000:
            print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli tyydyttävä!")
        else:
            print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli huono!")
