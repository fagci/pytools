#!/usr/bin/env python
import socket as so
import sys

from lib.pt_module import ToolframeModule


class Scan(ToolframeModule):
    """Various network scanners"""

    def __init__(self):
        from threading import Lock
        from queue import Queue
        super().__init__()
        self._queue = Queue()
        self._lock = Lock()
        self._results = []

    def ports(self, host: str, p_start: int, p_end: int, t: int = 16):
        """Threaded port scanner

        host -- host name or ip address
        p_start -- port to scan from
        p_end -- port to scan to (inclusive)
        t -- number of threads
        """
        from threading import Thread
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
            self._queue.put((ip, port))

        self._queue.join()

    @staticmethod
    def _check_port(target: tuple):
        with so.socket() as socket:  # tcp by default
            return target if socket.connect_ex(target) == 0 else None

    def _scan(self):
        while True:
            try:
                result = self._check_port(self._queue.get())
            except OSError as e:
                print(e.strerror)
                sys.exit(e.errno)
            with self._lock:
                if result:
                    host, port = result
                    try:
                        serv = so.getservbyport(port, 'tcp')
                    except:
                        serv = ''
                    self._results.append((host, port, serv))
                    print(f'{port:<5} {serv}')
            self._queue.task_done()
