#!/usr/bin/env python
import fire
import socket as so
from alive_progress import alive_bar
from functools import partial
from concurrent.futures import ThreadPoolExecutor


def scan(ip, port):
    r = False
    try:
        s = so.socket(so.AF_INET, so.SOCK_STREAM)
        s.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
        r = s.connect_ex((ip, port)) == 0
        s.close()
        return (port, r,)
    except so.timeout:
        pass
    except so.error as e:
        print(f'{e}')
        exit(e.errno)
    finally:
        return (port, r,)


def main(host, port_from, port_to, t=256):
    so.setdefaulttimeout(0.5)

    ip = so.gethostbyname(host)

    print(f'Scanning {ip} using {t} workers...')
    result = {}
    with ThreadPoolExecutor(t) as ex:
        ports = range(port_from, port_to + 1)
        with alive_bar(len(ports), bar='smooth', spinner='dots_reverse') as bar:
            for p, s in ex.map(partial(scan, ip), ports):
                result[p] = s
                bar()
    for p, s in result.items():
        if s:
            print(f'{p}: open')

if __name__ == "__main__":
    try:
        fire.Fire(main)
    except so.gaierror as e:
        print(f'Host not resolved')
        exit(e.errno)
    except KeyboardInterrupt:
        print('Interrupted by user')
        exit(130)

