#!/usr/bin/env python
"""
More user friendly threaded port scanner than previous version.
Starts immediately.
"""
from queue import Queue
import socket as so
import sys
from threading import Lock, Thread


class Scan:
    __doc__ = __doc__

    def __init__(self) -> None:
        self.queue = Queue()
        self.lock = Lock()
        self.results = []

    def _check(self, target: tuple):
        with so.socket() as socket:  # tcp by default
            return target if socket.connect_ex(target) == 0 else None

    def _scan(self):
        while True:
            try:
                result = self._check(self.queue.get())
            except OSError as e:
                print(e.strerror)
                sys.exit(e.errno)
            with self.lock:
                if result:
                    host, port = result
                    try:
                        serv = so.getservbyport(port, 'tcp')
                    except:
                        serv = ''
                    self.results.append((host, port, serv))
                    print(f'{port:<5} {serv}')
            self.queue.task_done()

    def ports(self, host: str, p_start: int, p_end: int, t: int = 16):
        so.setdefaulttimeout(1)
        try:
            ip = so.gethostbyname(host)
        except so.gaierror as e:
            print(host, 'not resolved.')
            sys.exit(e.errno)

        ports = range(max(1, p_start), min(65535, p_end) + 1)
        size = len(ports)

        sys.stderr.write(f'Scan {size} ports on {ip} with {t} threads...\n')

        for _ in range(t):
            Thread(target=self._scan, daemon=True).start()

        for port in ports:
            self.queue.put((ip, port))

        self.queue.join()
