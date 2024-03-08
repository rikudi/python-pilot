import time, os, sys
def kirjoittaja_normal(teksti):
    for char in teksti:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)

def kirjoittaja_fast(teksti):
    for char in teksti:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)

def kirjoittaja_slow(teksti):
    for char in teksti:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)

#teksti = "Peli alkaa... Lentokoneesi nousee Helsinki-Vantaan lentokentältä ilmaan"
#kirjoittaja(teksti)