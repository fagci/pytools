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
                if ip.startswith((
                    '10.',
                    '169.254.',
                    '172.16.',
                    '172.17.',
                    '172.18.',
                    '172.19.',
                    '172.20.',
                    '172.21.',
                    '172.22.',
                    '172.23.',
                    '172.24.',
                    '172.25.',
                    '172.26.',
                    '172.27.',
                    '172.28.',
                    '172.29.',
                    '172.30.',
                    '172.31.',
                    '192.168.',
                    '127.'
                )):
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
