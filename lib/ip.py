"""IP related utilities"""
from random import randrange as rr


def randip():
    """Get wide range random IP"""
    return f'{rr(1, 255)}.{rr(0, 255)}.{rr(0, 255)}.{rr(1,255)}'
