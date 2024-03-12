import time, sys
def print_normal(teksti):
    for char in teksti:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)

def print_nopea(teksti):
    for char in teksti:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)

def print_hidas(teksti):
    for char in teksti:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)