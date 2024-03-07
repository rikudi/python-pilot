import mysql.connector

yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='flight_game',
    user='root',
    password='Lihapullat1Maria',
    autocommit=True
)

nimi = input("Anna pelinimi: ")
def mysql_insert_alkuarvot(nimi):
    sql = f"INSERT INTO game (id, fuel, location_lat, location_lon, kierrokset) VALUES ('{nimi}', 100, 60.3172, 24.963301, 0)"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

# Tarkistaa onko pelaajan nimi jo tietokannassa #
thelist = []
def mysql_id_tarkistus(nimi):
     sql = f"SELECT id FROM game WHERE EXISTS(SELECT id FROM game)"
     kursori = yhteys.cursor()
     kursori.execute(sql)
     tiedot = kursori.fetchall()
     for x in tiedot:
         thelist.append(x)
     return

mysql_id_tarkistus(nimi)
res = str(thelist)
res = res.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "")

if nimi in res:
    print(nimi, "Tietokannassa")
else:
    mysql_insert_alkuarvot(nimi)
    print(nimi, "Lisätty")

latitude = float(input("Enter latitude: "))
longitude = float(input("Enter longitude: "))
koordinaatit = latitude, longitude
def mysql_update_coordinates(nimi, latitude, longitude):
    sql = f"UPDATE game set location_lat = '{latitude}', location_lon = '{longitude}' WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

mysql_update_coordinates(nimi, latitude, longitude)
def mysql_update_polttoaine(nimi):
    sql = f"UPDATE game SET fuel = fuel - 20 WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return
mysql_update_polttoaine(nimi)

def mysql_query_tiedot(nimi):
    sql = f"SELECT location_lat, location_lon, fuel FROM game WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    mytiedot = kursori.fetchall()
    return mytiedot

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="testi")
location = geolocator.reverse(koordinaatit, language="fi")
if location == None:
    print("Olet kansainvälisessä ilmatilassa")
else:
    print("Olet maan", location.raw['address']['country'] + " ilmatilassa")

print("Koordinaatit ja bensa:")
for x in mysql_query_tiedot(nimi):
    print(x)

Ankara = (40.128101348899996, 32.995098114)

from geopy.distance import geodesic
matka = geodesic(koordinaatit, Ankara).km
print(matka, "Kilometriä ankaraan")
def mysql_query_close_airports(nimi):
    sql = f"SELECT name AS lentokentät, ident AS icao FROM airport CROSS JOIN game WHERE type IN('medium_airport', 'large_airport') AND latitude_deg BETWEEN location_lat - 3 and location_lat + 3 AND longitude_deg BETWEEN location_lon - 3 and location_lon + 3 AND game.id = '{nimi}' ORDER BY name"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    mytiedot = kursori.fetchall()
    return mytiedot
for x in mysql_query_close_airports(nimi):
    print(x)

ICAO = input("Anna ICAO koodi: ")
def mysql_update_laskeutuminen(nimi, ICAO):
    sql = f"UPDATE game CROSS JOIN airport set location_lat = latitude_deg, location_lon = longitude_deg, fuel=100 where ident = '{ICAO}' and game.id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return
mysql_update_laskeutuminen(nimi, ICAO)

def mysql_lentokenttä(ICAO):
        sql = f"SELECT name FROM airport WHERE ident = '{ICAO}'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        myresult = kursori.fetchall()
        return myresult

print("Laskeuduit lentokentälle: ", mysql_lentokenttä(ICAO), "ja tankkasit lentokoneen täyteen")
def mysql_update_kierrokset(nimi):
    sql = f"UPDATE game SET kierrokset = kierrokset + 1 WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return
mysql_update_kierrokset(nimi)