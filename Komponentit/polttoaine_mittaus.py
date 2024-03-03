import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='python_pilot',
         user='root',
         password='alakatomunsalasanaa',
         autocommit=True
         )

def polttoaine_mittaus():
    sql = 'SELECT fuel FROM game'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    bensa_loppu = 0

    if tulos == 400:
        print("Varoitus! Polttoainetta jäljellä 40%.")
    elif tulos == 200:
        print("Varoitus! Polttoainetta jäjellä 20%")
    elif tulos == 0 and bensa_loppu == 0:
        print("Varoitus! Polttoaineesi on lähes loppu! Laskeudu välittömästi lähimmälle lentokentälle.")
        bensa_loppu =+ 1
    elif tulos == 0 and bensa_loppu == 1:
            print("Lentokoneesi putoaa.")
            bensa_loppu = 0  #Resettaa bensa_loppu mittauksen, en oo varma onko tarpeellinen
            game_over = True