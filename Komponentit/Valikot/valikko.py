'''
Oma komponetti itse valikon toiminnalle. Valikon avaaminen, sulku ja muu toiminta valikko_managerissa.
Valikko_manageri kutsuu aina kentat_valikko funktiota täältä.
'''

# Täällä ei toimi pynput, eli käyttäjän pitää painaa enteriä ku tekee valinnan. Pitää fiksaa.
def kentat_valikko(options):
    print("Lähimmät lentokentät. Laskeudu tankkaamaan?")
    for i, option in enumerate(options, start=1):
        print(f'{i}. {option}')

    valinta = int(input('Valitse kenttä: '))
    if 1 <= valinta <= len(options):
        return options[valinta - 1]
    else:
        print('Virheellinen syöte')
        return None