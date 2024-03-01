# Tällä koodilla yhdistetään tietokantaan. Voisi luoda erillisen käyttäjän #
# tietokantaan peliä varten #
import mysql.connector
yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='flight_game',
    user='root',
    password='Lihapullat1Maria',
    autocommit=True
)
