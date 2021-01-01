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
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TaskID

pb = Progress()
console: Console = pb.console
console.clear()


def check(target: tuple):
    with so.socket(so.AF_INET, so.SOCK_STREAM) as s:
        return target if s.connect_ex(target) == 0 else None


def scan(queue: Queue, lock: Lock, results: list):
    while True:
        r = check(queue.get())
        pb.update(TaskID(0), advance=1)
        with lock:
            if r:
                h, p = r
                try:
                    serv = so.getservbyport(p, 'tcp')
                except:
                    serv = ''
                results.append((h, p, serv))
        queue.task_done()


def main(host: str, p_start: int, p_end: int, t: int=16):
    so.setdefaulttimeout(1)
    try:
        ip = so.gethostbyname(host)
    except so.gaierror as e:
        print(host, 'not resolved.')
        sys.exit(e.errno)

    ports = range(p_start, p_end + 1)
    size = len(ports)
    queue = Queue(size)
    lock = Lock()

    results = []

    console.print(f'Scanning {size} ports on {ip} using {t} threads...')
    pb.add_task('Scan', total=size)
    pb.start()

    for port in ports:
        queue.put((ip, port))

    for _ in range(t):
        thr = Thread(target=scan, args=(queue, lock, results,))
        thr.setDaemon(True)
        thr.start()

    queue.join()
    pb.stop()
    tt = Table('port', 'service')

    for h, p, s in results:
        tt.add_row(str(p), str(s))

    console.print(tt)


if __name__ == "__main__":
    try:
        fire.Fire(main)
    except KeyboardInterrupt:
        print('Interrupted by user')
        pb.stop()

