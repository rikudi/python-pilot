# Tällä koodilla yhdistetään tietokantaan. Voisi luoda erillisen käyttäjän #
# tietokantaan peliä varten #
import mysql.connector
yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='flight_game',
    user='root',
    password='JokuSalasana',
    autocommit=True
)

# Funktio polttoaineen vähentämiseen kierroksen jälkeen #
def mysql_update_polttoaine(nimi):
    sql = f"UPDATE game SET fuel = fuel - 20 WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

# funktio pelaajan nimen lisäämiseen tietokantaan ja pelaajalle syötetään alkuarvot tietokantaan"
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
def mysql_query_close_airports():
    sql = f"SELECT name, ident FROM airport CROSS JOIN game WHERE type IN('medium_airport', 'large_airport') AND latitude_deg BETWEEN location_lat - 3 and location_lat + 3 AND longitude_deg BETWEEN location_lon - 3 and location_lon + 3 ORDER BY name"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

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

