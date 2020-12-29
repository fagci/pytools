#!/usr/bin/env python
import sys
import socket as so
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import fire
from alive_progress import alive_bar


def scan(ip, port):
    try:
        s = so.socket(so.AF_INET, so.SOCK_STREAM)
        s.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
        r = s.connect_ex((ip, port)) == 0
        s.close()
    except so.error as e:
        r = False
        print(e)
        sys.exit(e.errno)
    return (port, r,)


def main(host, port_from, port_to, t=256):
    so.setdefaulttimeout(0.5)

    ip = so.gethostbyname(host)

    print(f'Scanning {ip} using {t} workers...')
    result = {}
    ports = range(port_from, port_to + 1)
    with alive_bar(len(ports)) as progress:
        with ThreadPoolExecutor(t) as ex:
            try:
                for p, s in ex.map(partial(scan, ip), ports):
                    result[p] = s
                    progress()
            except so.gaierror as e:
                print('Host not resolved')
                sys.exit(e.errno)
            except KeyboardInterrupt:
                print('Interrupted by user')
                ex.shutdown()
                exit(130)
    for p, s in result.items():
        if s:
            print(f'{p}: open')

if __name__ == "__main__":
    fire.Fire(main)

