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
    " ": 'avaa_valikko',
    "H": 'nayta_ohjeet'
}

# funktio joka käsittelee valikon avaamista ja sulkua
def avaa_valikko():
    print("valikko avattu")

# funktio joka käsittelee ohjeiden näyttämistä
def nayta_ohjeet():
    print("ohjevalikko avattu")


# testi funktio joka liikuttaa pelaajaa etelään lähtöpisteestä päätepisteeseen tietyn matkan verran (200km)
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
    try:
        k = key.char.upper()  # single-char keys
    except:
        k = key.name  # other keys
    if k in nappaimet:  # mapataan nappaimet dictionarysta
        # self.keys.append(k)  # store it in global-like variable
        value = nappaimet[k]
        print('Painettu: ' + value)
        liiku_suuntaan(value)

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()