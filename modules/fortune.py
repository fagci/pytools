#!/usr/bin/env python
"""Wide IP range actions."""

from concurrent.futures import ThreadPoolExecutor
from os.path import basename
import socket as so

from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm

from lib.ip import randip
from lib.models import Fortune as FortuneModel
from lib.models import create_tables


HEADERS = {
    'User-Agent': f'fagci_pytools_fortune/1.0 (Wide range IP http checker, see https://github.com/fagcinsk/pytools/blob/main/{basename(__file__)})'
}


class Fortune:
    @staticmethod
    def _check_rnd_ip(_):
        ip = randip()
        with so.socket() as sock:
            if sock.connect_ex((ip, 80)) != 0:
                return False, ip, ''
        try:
            response = get(f'http://{ip}', HEADERS, timeout=0.25)
            bs = BeautifulSoup(response.content, 'html.parser')
            return True, ip, bs.title.string.strip()
        except Exception as e:
            return False, ip, e

    def spin(self, ip_count=1000, t=None):
        """Spins IP roulette and makes http requests
        Checks for http application title and print it if exists.
        """
        so.setdefaulttimeout(0.2)
        create_tables()
        with ThreadPoolExecutor(t) as executor:
            print('Using', getattr(executor, '_max_workers'), 'workers')
            results = []
            try:
                iterator = executor.map(self._check_rnd_ip, range(ip_count))
                for is_ok, ip, title in tqdm(iterator, unit='ip', total=ip_count):
                    if is_ok:
                        try:
                            FortuneModel.create(ip=ip, title=title)
                        except Exception as e:
                            print(e)
                        results.append((ip, title))
            except KeyboardInterrupt:
                print('Interrupted by user')

        print(len(results), 'results')
        for ip, title in results:
            print(f'{ip:<15} {title}')

    @staticmethod
    def list():
        """Get list of previous spins (ips with http title)"""
        for item in FortuneModel.select().order_by(FortuneModel.title):
            print(f'{item.ip}\t{item.title}')
