from pynput import keyboard
from Komponentit.Valikot import valikko_manageri

'''
Erillinen luokka pelaajan liikkeelle ja syötteille.
"self" käytetään parametrina kun luodaan instansseja luokan funktiohin muualta koodista.
Esim. Game.py:stä luodaan instanssi tähän luokkaan, jotta pelaajan syötteitä voidaan kuunnella.
'''
class PelaajaKontrolleri:
   # __init__ funktio kutsutaan automaattisesti kun luokasta tehdään instanssi
    def __init__(self, syote):
        self.nappaimet = {
            "1": 225,       # Lounas
            "2": 180,       # Etelä
            "3": 135,       # Kaakko
            "4": 270,       # Länsi
            "6": 90,        # Itä
            "7": 315,       # Luode
            "8": 0,         # Pohjoinen
            "9": 45,        # Koillinen
            "H": 'nayta_ohjeet',
            "KP1": 225,     # Lounas
            "KP2": 180,     # Etelä
            "KP3": 135,     # Kaakko
            "KP4": 270,     # Länsi
            "KP6": 90,      # Itä
            "KP7": 315,     # Luode
            "KP8": 0,       # Pohjoinen
            "KP9": 45,      # Koillinen
        }
        self.valikko_manageri = valikko_manageri.ValikkoManageri()
        self.kentat = ['Kenttä 1', 'Kenttä 2', 'Kenttä 3']
        self.syote_callback = syote
        self.listener = keyboard.Listener(on_release=self.on_release)
        self.listener.start()

    def nayta_ohjeet(self):  # kesken
        print("ohjevalikko avattu")


    # kuuntelee käyttäjän syötteitä
    def on_release(self, key):
        if key == keyboard.Key.space:                               # kutsuu valikon käsittelijä funktiota
            if not self.valikko_manageri.valikko_auki:              # jos valikko ei ole auki
                self.valikko_manageri.kentat_valikko(self.kentat)   # self.kentat on esimerkki-dataa -> Rivi 23
            else:
                self.valikko_manageri.valikko_kasittelija()

        try:
            k = key.char.upper()
        except AttributeError:
            k = key.name

        if k in self.nappaimet:          # looppaa nappaimet-sanakirjan läpi ja tarkistaa löytyykö syötettä vastaava arvo
            self.syote_callback(k)          # callback-funktio mikä kutsutaan game.py