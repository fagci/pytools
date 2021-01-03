#!/usr/bin/env python
from lib.ip import randip
from bs4 import BeautifulSoup
from requests import get, ConnectionError
from random import randrange
from concurrent.futures import ThreadPoolExecutor


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def check_rnd_ip(_):
    ip = randip()
    title = '-'
    try:
        response = get(f'http://{ip}', headers, timeout=randrange(1,3))
        if response:
            bs = BeautifulSoup(response.content, 'html.parser')
            title = bs.find('title').string
        return (ip, title,)
    except ConnectionError as e:
        return (ip, e.strerror or 'timeout',)
    except Exception as e:
        return (ip, e,)

with ThreadPoolExecutor() as executor:
    for ip, title in executor.map(check_rnd_ip, range(1000)):
        print(f'{ip:<15} {title}')
