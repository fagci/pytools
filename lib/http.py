from bs4 import BeautifulSoup
from requests import get

HEADERS = {
    'User-Agent': f'fagci_pytools_fortune/1.0 (Wide range IP http checker, see https://github.com/fagcinsk/pytools/'
}


def check_http(ip: str, timeout: float = 0.25):
    try:
        response = get(f'http://{ip}', HEADERS, timeout=timeout)
        bs = BeautifulSoup(response.content, 'html.parser')
        return True, ip, bs.title.string.strip()
    except Exception as e:
        return False, ip, e
