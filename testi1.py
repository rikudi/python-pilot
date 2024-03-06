import mysql.connector

yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='flight_game',
    user='root',
    password='Lihapullat1Maria',
    autocommit=True
)

nimi = "Testi"
latitude = float(input("Enter latitude: "))
longitude = float(input("Enter longitude: "))
koordinaatit = latitude, longitude

def mysql_update_coordinates(nimi, latitude, longitude):
    sql = f"UPDATE game set location_lat = '{latitude}', location_lon = '{longitude}' WHERE id = '{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

mysql_update_coordinates(nimi, latitude, longitude)

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