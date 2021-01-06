from socket import socket


def check_port(ip: str, port: int = 21, timeout: float = 0.2) -> str:
    """Check tcp port, returns ip if connection established"""
    with socket() as sock:
        sock.settimeout(timeout)
        return ip if sock.connect_ex((ip, port)) == 0 else ''


def portchecker(port: int, timeout: float = 0.2):
    """Returns function to scan one port with fixed timeout"""
    from functools import partial
    return partial(check_port, port=port, timeout=timeout)
