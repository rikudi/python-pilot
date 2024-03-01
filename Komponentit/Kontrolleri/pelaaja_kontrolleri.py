from pynput import keyboard
from Komponentit.Valikot import valikko_manageri

'''
Erillinen luokka pelaajan liikkeelle ja syötteille.
"self" käytetään parametrina kun luodaan instansseja luokan funktiohin muualta koodista.
Esim. Game.py:stä luodaan instanssi tähän luokkaan, jotta pelaajan syötteitä voidaan kuunnella.
'''
class PelaajaKontrolleri:
   # __init__ funktio kutsutaan automaattisesti kun luokasta tehdään instanssi
    def __init__(self):
        self.nappaimet = {
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

        self.kentat = ['Kenttä 1', 'Kenttä 2', 'Kenttä 3']
        self.menu_manager = valikko_manageri.MenuManager()  # luodaan instanssi MenuManagerista
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener.join()

    def nayta_ohjeet(self):                # kesken
        print("ohjevalikko avattu")

    def liiku_suuntaan(self, bearing):     # kesken
        print("liikutaan suuntaan: " + bearing)


    # kuuntelee käyttäjän syötteitä
    def on_press(self, key):
        if key == keyboard.Key.esc:
            print("Esc painettu")
            return False
        if key == keyboard.Key.space:                           # kutsuu valikon käsittelijä funktiota
            if not self.menu_manager.valikko_auki:              # jos valikko ei ole auki
                self.menu_manager.kentat_valikko(self.kentat)   # self.kentat on esimerkki-dataa -> Rivi 23
            else:
                self.menu_manager.valikko_kasittelija() #
        try:
            k = key.char.upper()
        except AttributeError:
            k = key.name
        if k in self.nappaimet:          # looppaa nappaimet-sanakirjan läpi ja tarkistaa löytyykö syötettä vastaava arvo
            value = self.nappaimet[k]
            print('Painettu: ' + value)  # voi poistaa myöhemmin
            self.liiku_suuntaan(value)   # jos löytyy syötettä vastaava luku -> kutsutaan liike funktiota
