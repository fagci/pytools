#!/usr/bin/env python
import sys
from socket import socket, AF_INET, SOCK_STREAM, setdefaulttimeout, gethostbyname, gaierror

import fire


def scan(ip, port):
    with socket(AF_INET, SOCK_STREAM) as s:
        return port if s.connect_ex((ip, port)) == 0 else None

def perform_scan(ip, ports, t):
    print(f'Scanning {ip}...')
    import concurrent.futures as fut
    with fut.ThreadPoolExecutor(t) as ex:
        try:
            from functools import partial
            from tqdm import tqdm
            iterator = ex.map(partial(scan, ip), ports)
            iterator = tqdm(iterator, total=len(ports), unit='ports')
            opened_ports = [p for p in iterator if p]
        except gaierror as e:
            print('Host not resolved')
            sys.exit(e.errno)
        except KeyboardInterrupt:
            print('Interrupted by user')
            sys.exit(130)
    return opened_ports

def main(host, port_from, port_to, t=None):
    setdefaulttimeout(0.5)
    ip = gethostbyname(host)
    ports = range(port_from, port_to + 1)
    opened_ports = perform_scan(ip, ports, t)

    print('Opened ports:')
    for p in opened_ports:
        print(f'{p}')

if __name__ == "__main__":
    fire.Fire(main)

