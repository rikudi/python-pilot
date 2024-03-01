from pynput import keyboard
from geopy.distance import geodesic
from geopy.point import Point

nappaimet = {
    "1": "Lounas",
    "2": "Etelä",
    "3": "Kaakko",
    "4": "Länsi",
    "6": "Itä",
    "7": "Luode",
    "8": "Pohjoinen",
    "9": "Koillinen",
    "H": 'nayta_ohjeet'
}

# funktio joka käsittelee valikon avaamista ja sulkua
def valikko_kasittelija():
    print("valikko avattu")


# funktio joka käsittelee ohjeiden näyttämistä
def nayta_ohjeet():
    print("ohjevalikko avattu")


# testi funktio joka liikuttaa pelaajaa lähtöpisteestä päätepisteeseen tietyn matkan verran (200km)
def liiku_suuntaan(bearing):
    print("liikutaan suuntaan: " + bearing)
    '''distance = 200
    lat = "30"
    lon = "45"
    start_location = Point(lat, lon)
    destination = geodesic(kilometers=distance).destination(start_point, bearing)'''

def on_press(key):
    if key == keyboard.Key.esc:
        print("Esc painettu")
        return False  # stop listener
    if key == keyboard.Key.space:
        valikko_kasittelija() # jos space painetaan, kutsu valikko_kasittelija()
    try:
        k = key.char.upper()
    except:
        k = key.name
    if k in nappaimet:  # mapataan nappaimet dictionarysta
        value = nappaimet[k]
        print('Painettu: ' + value)
        liiku_suuntaan(value)

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
