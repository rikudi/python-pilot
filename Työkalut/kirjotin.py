import time, sys
def normal(teksti):
    for char in teksti:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)

def fast(teksti):
    for char in teksti:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)

def slow(teksti):
    for char in teksti:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)