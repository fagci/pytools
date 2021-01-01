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
from tqdm import tqdm


def check(target:tuple):
    with so.socket(so.AF_INET, so.SOCK_STREAM) as s:
        return target if s.connect_ex(target) == 0 else None


def scan(queue:Queue, lock:Lock, results:list, pb:tqdm):
    while True:
        try:
            r = check(queue.get())
            with lock:
                pb.update()
                if r:
                    results.append(r)
        except:
            sys.exit()
        queue.task_done()


def main(host:str, p_start:int, p_end:int, t:int=16):
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

    pb = tqdm(total=size, unit='port')

    for _ in range(t):
        thr = Thread(target=scan, args=(queue, lock, results, pb,))
        thr.setDaemon(True)
        thr.start()

    for port in ports:
        queue.put((ip, port))

    queue.join()

    for r in results:
        print(*r, 'open')


if __name__ == "__main__":
    try:
        fire.Fire(main)
    except KeyboardInterrupt:
        print('Interrupted by user')

