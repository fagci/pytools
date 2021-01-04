#!/usr/bin/env python
"""
Wide IP range http checker.
Checks for http application title and print it if exists.
"""
from concurrent.futures import ThreadPoolExecutor
from os.path import basename

from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm

from lib.ip import randip
from lib.models import Fortune as FortuneModel
from lib.models import create_tables


headers = {
    'User-Agent': f'fagci_pytools_fortune/1.0 (Wide range IP http checker, see https://github.com/fagcinsk/pytools/blob/main/{basename(__file__)})'
}


class Fortune:
    def _check_rnd_ip(self, _):
        ip = randip()
        try:
            response = get(f'http://{ip}', headers, timeout=0.3)
            if response:
                bs = BeautifulSoup(response.content, 'lxml')
                title = bs.find('title').string
                return (True, ip, title.strip(),)
            return (False, ip, '-',)
        except ConnectionError as e:
            return (False, ip, e.strerror or 'timeout',)
        except Exception as e:
            return (False, ip, e,)

    def spin(self, ip_count=1000, t=None):
        create_tables()
        with ThreadPoolExecutor(t) as executor:
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

    def list(self):
        for item in FortuneModel.select().order_by(FortuneModel.title):
            print(f'{item.ip}\t{item.title}')
