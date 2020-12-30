#!/usr/bin/env python
import sys
from socket import socket, AF_INET, SOCK_STREAM, setdefaulttimeout, gethostbyname, gaierror
from functools import partial
from concurrent.futures import ThreadPoolExecutor

import fire
from tqdm import tqdm


def scan(ip, port):
    with socket(AF_INET, SOCK_STREAM) as s:
        return port if s.connect_ex((ip, port)) == 0 else None


def main(host, port_from, port_to, t=256):
    setdefaulttimeout(0.5)

    ip = gethostbyname(host)

    print(f'Scanning {ip} using {t} workers...')
    opened_ports = []
    ports = range(port_from, port_to + 1)
    with ThreadPoolExecutor(t) as ex:
        try:
            for p in tqdm(ex.map(partial(scan, ip), ports), total=len(ports), unit='ports'):
                if p:
                    opened_ports.append(p)
        except gaierror as e:
            print('Host not resolved')
            sys.exit(e.errno)
        except KeyboardInterrupt:
            print('Interrupted by user')
            sys.exit(130)
    print('Opened ports:')
    for p in opened_ports:
        print(f'{p}')

if __name__ == "__main__":
    fire.Fire(main)

