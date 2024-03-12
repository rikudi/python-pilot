from Työkalut import kirjotin
def ohjeistus():
    ohje = """
Tervetuloa pelaamaan Python Pilottia!
Pelin tavoitteena on saapua Ankaran lentokentälle mahdollisimman vähin siirroin, lähtöpaikkasi on Helsinki-Vantaan lentokenttä. 
Yhdellä siirrolla lentokone liikkuu 200km haluttuun ilmansuuntaan.
Lentokone on täysin tankattu pelin alussa, jolla voit kulkea maksimissaan 1000 kilometriä. Aina kun laskeudut lähimmälle lentokentälle,
lentokoneen tankki täytetään 100 %.

Pelin näppäimet :
Num 1: Lounas
Num 2: Etelä
Num 3: Kaakko
Num 4: Länsi
Num 6: Itä
Num 7: Luode
Num 8: Pohjoinen
Num 9: Koillinen
SPACE: Avaa valikon, jossa on viisi lähintä lentokenttää. Kentät on numeroitu 1–5. Painamalla halutun lentokentän numeroa, kone laskeutuu
sinne.
H: ohjeet ja opasteet
"""
    kirjotin.print_nopea(ohje)