import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='python_pilot',
         user='root',
         password='admin',
         autocommit=True
         )

def polttoaine_mittaus(pelaaja_id):
    global game_over
    sql = f"SELECT fuel FROM game WHERE id = '{pelaaja_id}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    x = kursori.fetchone()
    x = (x[0])

    if x == 40:
        print("Varoitus! Polttoainetta jäljellä 40%.")
    elif x == 20:
        print("Varoitus! Polttoainetta jäjellä 20%")
    elif x <= 0:
        print("Lentokoneesi putoaa.")
        game_over = True

