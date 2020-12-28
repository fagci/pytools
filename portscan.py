#!/usr/bin/env python
import fire
import socket as so
from functools import partial
from concurrent.futures import ThreadPoolExecutor


def scan(ip, port):
    s = so.socket(so.AF_INET, so.SOCK_STREAM)
    s.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
    if s.connect_ex((ip, port)) == 0:
        print(f'{port}: open')
    s.close()


def main(host, port_from, port_to, t=256):
    so.setdefaulttimeout(0.75)

    ip = so.gethostbyname(host)

    print(f'Scanning {ip} using {t} workers...')
    with ThreadPoolExecutor(t) as ex:
        ports = range(port_from, port_to + 1)
        ex.map(partial(scan, ip), ports)


if __name__ == "__main__":
    try:
        fire.Fire(main)
    except so.gaierror as e:
        print(f'Host not resolved')
        exit(e.errno)
    except so.error as e:
        print(f'{e}')
        exit(e.errno)
    except KeyboardInterrupt:
        print('Interrupted by user')
        exit(130)

