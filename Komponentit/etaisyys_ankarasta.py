import mysql.connector
from geopy.distance import great_circle


yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='python_pilot',
         user='root',
         password='admin',
         autocommit=True
         )


def etaisyys_ankara(pelaaja_id):
    sql = f"SELECT location_lat, location_lon FROM game WHERE id = '{pelaaja_id}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()

    nykyinen_sijainti = (tulos[0][0], tulos[0][1])
    ankara = (40.128101348899996, 32.995098114)
    print("Etäisyys määränpäästä:", round(great_circle(nykyinen_sijainti,ankara).kilometers),"km")