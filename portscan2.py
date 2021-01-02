#!/usr/bin/env python
"""
More user friendly threaded port scanner than previous version.
Starts immediately.
"""
import sys
import socket as so
from queue import Queue
from threading import Thread, Lock

import fire


def check(target: tuple):
    with so.socket() as socket: #tcp by default
        return target if socket.connect_ex(target) == 0 else None


def scan(queue: Queue, lock: Lock, results: list):
    while True:
        try:
            result = check(queue.get())
        except OSError as e:
            print(e.strerror)
            sys.exit(e.errno)
        with lock:
            if result:
                host, port = result
                try:
                    serv = so.getservbyport(port, 'tcp')
                except:
                    serv = ''
                results.append((host, port, serv))
                print(f'{port:<5} {serv}')
        queue.task_done()


def main(host: str, p_start: int, p_end: int, t: int=16):
    so.setdefaulttimeout(1)
    try:
        ip = so.gethostbyname(host)
    except so.gaierror as e:
        print(host, 'not resolved.')
        sys.exit(e.errno)

    ports = range(max(1, p_start), min(65535, p_end) + 1)
    size = len(ports)
    queue = Queue(size)
    lock = Lock()

    results = []

    sys.stderr.write(f'Scan {size} ports on {ip} with {t} threads...\n')

    args = (queue, lock, results,)

    for _ in range(t):
        Thread(target=scan, daemon=True, args=args).start()

    for port in ports:
        queue.put((ip, port))

    queue.join()

if __name__ == "__main__":
    try:
        fire.Fire(main)
    except KeyboardInterrupt:
        print('Interrupted by user')

