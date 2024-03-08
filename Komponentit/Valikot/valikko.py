from consolemenu import ConsoleMenu
from consolemenu.console_menu import MenuItem, ExitItem
import time


def open_menu(data):
    print(data)  # voi poistaa
    menu = ConsoleMenu("Lähimmät Lentokentät", "Valitse kenttä laskeutuaksesi:")
    # Luodaan jokaisesta datan rivistä MenuItem
    for kentta in data:
        valinta = MenuItem(f"{kentta[0]} - {kentta[1]}", should_exit=True)  # should_exit=True => poistuu menusta heti valinnan jälkeen
        menu.append_item(valinta)
    menu.show()

    # Pelaajan valinta
    valinta = menu.selected_item
    # Tarkastetaan onko kelvollinen valinta
    if valinta is None:
        print("Valinta ei kelpaa.")
        time.sleep(0.5)
        return None
    # Jos valinta == ExitItem => palautetaan None
    elif isinstance(valinta, ExitItem):
        print("Suljetaan valikko...")
        time.sleep(0.5)
        return None
    else:
        # Leikataan valinta-stringin loppuosa jotta saadaan ICAO-koodi sql-kyselyä varten
        icao_code = valinta.text.split("-")[-1].strip()
        time.sleep(0.5)
        return icao_code