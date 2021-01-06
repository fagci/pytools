"""IP related utilities"""


def randip():
    """Get wide range random IP"""
    from random import randrange
    a = randrange(1, 255)
    b = randrange(0, 255)
    c = randrange(0, 255)
    d = randrange(1, 255)
    return '{}.{}.{}.{}'.format(a, b, c, d)


def generate_ips(count: int):
    """Get wide range random IPs"""
    for _ in range(count):
        yield randip()


def local_ip():
    """Get local ip"""
    from socket import socket, AF_INET, SOCK_DGRAM
    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.connect(('8.8.8.8', 80))
        return sock.getsockname()[0]
