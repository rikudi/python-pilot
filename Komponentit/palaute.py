import mysql.connector


yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='python_pilot',
         user='root',
         password='alakatomunsalasanaa',
         autocommit=True
         )
'''
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

'''


def palaute(pelaaja_id):
    sql = f"SELECT kierrokset FROM game WHERE id = '{pelaaja_id}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    x = (tulos[0])

    kilometrit = x * 200
    if kilometrit <= 2600:
        print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli erinomainen!")
    elif 2600 < kilometrit <= 3200:
        print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli hyvä!")
    elif 3200 < kilometrit <= 4000:
        print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli tyydyttävä!")
    else:
        print("Matkasi pituus oli", kilometrit, "km! Suorituksesi oli huono!")

'''
    while True:
        uusi_peli = input("Haluatko pelata uudestaan (kyllä/ei): ").lower()
        if uusi_peli == "kyllä":
            ohjeistus()
            # Ohjeistukseen lisätään vielä pelaaja syöttämään pelitunnus
            # Tietokanta resetointi mysql_insert_into(nimi)
        elif uusi_peli == "ei":
            quit()
        else:
            print("Tarkista syöte.")
'''