"""IP related utilities"""


def randip():
    """Get wide range random IP"""
    from random import randrange as rr
    return f'{rr(1, 255)}.{rr(0, 255)}.{rr(0, 255)}.{rr(1,255)}'


def local_ip():
    """Get local ip"""
    from socket import socket, AF_INET, SOCK_DGRAM
    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.connect(('8.8.8.8', 80))
        return sock.getsockname()[0]
