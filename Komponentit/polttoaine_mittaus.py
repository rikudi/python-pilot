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
    x = kursori.fetchone()
    x = (x[0])
    bensa_loppu = 0

    if x == 400:
        print("Varoitus! Polttoainetta jäljellä 40%.")
    elif x == 200:
        print("Varoitus! Polttoainetta jäjellä 20%")
    elif x == 0 and bensa_loppu == 0:
        print("Varoitus! Polttoaineesi on lähes loppu! Laskeudu välittömästi lähimmälle lentokentälle.")
        bensa_loppu =+ 1
    elif x == 0 and bensa_loppu == 1:
            print("Lentokoneesi putoaa.")
            bensa_loppu = 0  #Resettaa bensa_loppu mittauksen, en oo varma onko tarpeellinen
            game_over = True