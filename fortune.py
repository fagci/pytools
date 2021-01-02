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
    title = ''
    try:
        response = get(f'http://{ip}', headers, timeout=randrange(1,3))
        if response:
            bs = BeautifulSoup(response.content, 'html.parser')
            title = bs.find('title').string
        print(ip, title)
    except ConnectionError as e:
        print(ip, e.strerror or 'timeout')
    except Exception as e:
        print(ip, e)

with ThreadPoolExecutor() as executor:
    for r in executor.map(check_rnd_ip, range(1000)):
        pass
