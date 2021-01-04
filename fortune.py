#!/usr/bin/env python
"""
Wide IP range http checker.
Checks for http application title and print it if exists.
"""
from os.path import basename
from concurrent.futures import ThreadPoolExecutor

from lib.ip import randip
from requests import get, ConnectionError
from bs4 import BeautifulSoup
import fire
from tqdm import tqdm

from lib.models import Fortune, create_tables


headers = {
        'User-Agent': f'fagci_pytools_fortune/1.0 (Wide range IP http checker, see https://github.com/fagcinsk/pytools/blob/main/{basename(__file__)})'
}


def check_rnd_ip(_):
    ip = randip()
    try:
        response = get(f'http://{ip}', headers, timeout=0.3)
        if response:
            bs = BeautifulSoup(response.content, 'lxml')
            title = bs.find('title').string
            return (True, ip, title.strip(),)
        else:
            return (False, ip, '-',)
    except ConnectionError as e:
        return (False, ip, e.strerror or 'timeout',)
    except Exception as e:
        return (False, ip, e,)


def main(ip_count=1000, t=None):
    create_tables()
    with ThreadPoolExecutor(t) as executor:
        results = []
        try:
            for is_ok, ip, title in tqdm(executor.map(check_rnd_ip, range(ip_count)), unit='ip', total=ip_count):
                if is_ok:
                    try:
                        Fortune.create(ip=ip, title=title)
                    except Exception as e:
                        print(e)
                    results.append((ip, title))
        except KeyboardInterrupt:
            print('Interrupted by user')

    print(len(results), 'results')
    for ip, title in results:
        print(f'{ip:<15} {title}')


def list_items():
    for item in Fortune.select().order_by(Fortune.created_at):
        print(f'{item.ip:<15} {item.title}')


if __name__ == "__main__":
    fire.Fire({
        'spin': main,
        'list': list_items,
    })

