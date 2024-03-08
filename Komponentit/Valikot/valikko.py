from consolemenu import ConsoleMenu
from consolemenu.console_menu import MenuItem, ExitItem
import time


def open_menu(data):
    print(data)
    menu = ConsoleMenu("Lähimmät Lentokentät", "Valitse kenttä laskeutuaksesi:")
    # luodaan jokaisesta rivistä MenuItem. MenuItem saa argumentiksi ICAO koodin joka ajetaan sql-kyselyssä
    for kentta in data:
        valinta = MenuItem(f"{kentta[0]} - {kentta[1]}", should_exit=True)  # should_exit=True => poistuu menusta heti valinnan jälkeen
        menu.append_item(valinta)
    menu.show()

    # pelaajan valinta
    valinta = menu.selected_item
    # jos valinta == ExitItem => return None
    if valinta is None:
        print("Valinta ei kelpaa.")
        time.sleep(0.5)
        return None
    elif isinstance(valinta, ExitItem):
        print("Suljetaan valikko...")
        time.sleep(0.5)
        return None
    else:
        icao_code = valinta.text.split("-")[-1].strip()  # Leikataan stringin loppuosa jotta saadaan ICAO-koodi
        time.sleep(0.5)
        return icao_code