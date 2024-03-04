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
def mysql_update(nimi):
    sql = f"UPDATE game SET fuel = fuel - 20 WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

# funktio pelaajan nimen lisäämiseen tietokantaan ja pelaajalle annettaan alkuarvot tietkannas"
def mysql_insert_into(nimi):
    sql = f"INSERT INTO game (id, fuel, location_lat, location_lon, kierrokset) VALUES ('{nimi}', 100, 60.3172, 24.963301, 0)"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

# Funktio koordinaattien päivittämiseen tietokantaan #

# Funktio lähimpien lentokenttien löytämiseen tietokannasta #

# Funktio kierrosten lisäämiseen tietokantaan #

