#!/usr/bin/env python
"""
Wide IP range http checker.
Checks for http application title and print it if exists.
"""
from os.path import basename
from random import randrange
from concurrent.futures import ThreadPoolExecutor

from lib.ip import randip
from requests import get, ConnectionError
from bs4 import BeautifulSoup
import fire
from tqdm import tqdm


headers = {
        'User-Agent': f'fagci_pytools_fortune/1.0 (Wide range IP http checker, see https://github.com/fagcinsk/pytools/blob/main/{basename(__file__)})'
}


def check_rnd_ip(_):
    ip = randip()
    try:
        response = get(f'http://{ip}', headers, timeout=0.5)
        if response:
            bs = BeautifulSoup(response.content, 'html.parser')
            title = bs.find('title').string
            return (True, ip, title.strip(),)
        else:
            return (False, ip, '-',)
    except ConnectionError as e:
        return (False, ip, e.strerror or 'timeout',)
    except Exception as e:
        return (False, ip, e,)


def main(ip_count=1000, t=None):
    with ThreadPoolExecutor(t) as executor:
        results = []
        try:
            for is_ok, ip, title in tqdm(executor.map(check_rnd_ip, range(ip_count)), unit='ip', total=ip_count):
                if is_ok:
                    results.append((ip, title))
        except KeyboardInterrupt:
            print('Interrupted by user')

    print(len(results), 'results')
    for ip, title in results:
        print(f'{ip:<15} {title}')


if __name__ == "__main__":
    fire.Fire(main)

