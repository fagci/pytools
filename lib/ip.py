from random import randrange as rr

def randip():
    return f'{rr(1, 255)}.{rr(0, 255)}.{rr(0, 255)}.{rr(1,255)}'

