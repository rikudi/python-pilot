#####################################################
### Pelaajan ohjaus ja toimintojen suorittaminen. ###
#####################################################

# Funktio joka ohjaa pelaajan liikkumista
def liiku_suuntaan(suunta):
    print(f"Liikuttiin suuntaan {suunta}")


#Tähän valikko funktio ja ohjeet funktio..


# Pelaajan näppäimet dictionaryssa
nappaimet = {
    "1": "Lounas",
    "2": "Etelä",
    "3": "Kaakko",
    "4": "Länsi",
    "6": "Itä",
    "7": "Luode",
    "8": "Pohjoinen",
    "9": "Koillinen",
    " ": avaa_valikko,
    "H": nayta_ohjeet
}

while True:
    syote = input("Valitse suunta [1-9], Avaa valikko [SPACE], Ohjeet [H]:") # tekstin voi fiksaa paremmaks myöhemmin
    toiminto = nappaimet.get(syote)   # Hae syötettä vastaava toiminto nappaimet dicti
    if toiminto:                      # Tarkistetaan että syöte vastaa jotain toimintoa
        if callable(toiminto):        # Tarkistetaan onko toiminto funktio callable-metodin avulla.
            toiminto()                # Jos on, kutsutaan funktiota.
        else: 
            liiku_suuntaan(toiminto)  # Jos ei, kutsutaan liiku_suuntaan-funktiota.
    else:
        print("Virheellinen syöte!")
        