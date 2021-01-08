"""IP related utilities"""


def randip():
    """Get wide range random host IP"""
    from random import randrange
    a = randrange(1, 256)  # 1..255
    b = randrange(0, 256)  # 0..255
    c = randrange(0, 256)  # 0..255
    d = randrange(1, 255)  # 1..254
    return '{}.{}.{}.{}'.format(a, b, c, d)


def generate_ips(count: int, bypass_local=True):
    """Get wide range random host IPs"""
    for _ in range(count):
        if bypass_local:
            while True:
                ip = randip()
                if ip.startswith(('10.', '172.16.', '192.168.', '127.')):
                    continue
                yield ip
                break
        else:
            yield randip()


def local_ip():
    """Get local ip"""
    from socket import socket, AF_INET, SOCK_DGRAM
    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.connect(('8.8.8.8', 80))
        return sock.getsockname()[0]
