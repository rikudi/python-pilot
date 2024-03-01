from Komponentit.Valikot.valikko import kentat_valikko
class MenuManager:
    def __init__(self):
        self.valikko_auki = False

    def valikko_kasittelija(self):
        self.valikko_auki = not self.valikko_auki

    def kentat_valikko(self, options):
        """
        Renderöi listan lentokentistä jotka pelaaja voi valita
        Args:
            options (lista): lista lentokentistä.
        """
        self.valikko_kasittelija()
        while self.valikko_auki:
            valinta = kentat_valikko(options)  # kutsutaan kentat_valikko funktio valikko.py:sta
            if valinta is not None:
                print(f"Laskeudutaan kentälle: {valinta}")
                self.valikko_kasittelija()
            else:
                print("Menu closed.")