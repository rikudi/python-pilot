from geopy.geocoders import Nominatim
import mysql.connector
from Komponentit import sql_koodit

yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='python_pilot',
    user='root',
    password='alakatomunsalasanaa',
    autocommit=True
)


def ilma_tilatarkistus(pelaaja_id):
    global game_over, venaja_counter, ukraina_counter
    if venaja_counter >= 4 or ukraina_counter >= 2:
        print("Lentokoneesi ammuttiin alas.")
        game_over = True

    sql = f"SELECT location_lat, location_lon FROM game WHERE id = '{pelaaja_id}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    x = kursori.fetchone()
    lat, lon = x

    geolocator = Nominatim(user_agent="testi")
    location = geolocator.reverse((lat, lon), language="fi")

    if location is None:
        print("Olet kansainvälisessä ilmatilassa.")
        return

    elif location.raw['address']['country'] == "Venäjä":
        print("Olet Venäjän ilmatilassa. Poistu enintään kolmen kierroksen aikana tai lentokoneesi ammutaan alas")
        venaja_counter += 1
        print("COUNTER",venaja_counter)
        return

    elif location.raw['address']['country'] == "Ukraina":
        print("Olet Ukrainan ilmatilassa, poistu enintään kahden kierroksen aikana tai lentokoneesi ammutaan alas")
        ukraina_counter += 1
        return

    elif location.raw['address']['country'] == "Saksa":
        print("Olet Saksan ilmatilassa. Sinulla tulee pakottava tarve saada rinkeliä, laskeudut lähimmälle lentokentälle syömään.")
        sql_koodit.mysql_update_kierrokset(pelaaja_id)
        return

    else:
        print("Olet maan", location.raw['address']['country'], "ilmatilassa.")
        return