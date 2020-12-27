#!/usr/bin/env python
import socket as so
import fire
from concurrent.futures import ThreadPoolExecutor
from functools import partial


def scan(ip, port):
    s = so.socket(so.AF_INET, so.SOCK_STREAM)
    s.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
    try:
        if s.connect_ex((ip, port)) == 0:
            print(f'{port}: open')
        s.close()
    except so.error as e:
        print(f'{e}')
        exit(e.errno)


def main(host, port_from, port_to, t=256):
    so.setdefaulttimeout(0.75)

    try:
        ip = so.gethostbyname(host)
    except so.gaierror as e:
        print(f'{host} not resolved')
        exit(e.errno)

    with ThreadPoolExecutor(max_workers=t) as ex:
        ports = range(port_from, port_to + 1)
        fn = partial(scan, ip)
        ex.map(fn, ports)


if __name__ == "__main__":
    try:
        fire.Fire(main)
    except KeyboardInterrupt:
        print('Interrupted by user')

