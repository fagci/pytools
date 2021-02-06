from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

HEADERS = {
    'User-Agent': f'fagci_pytools/1.0 (see https://github.com/fagcinsk/pytools/'
}


def check_http(ip: str, timeout: float = 0.25):
    try:
        url = f'http://{ip}'
        req = Request(url)
        for hk, hv in HEADERS.items():
            req.add_header(hk, hv)
        with urlopen(req, timeout=timeout) as f:
            bs = BeautifulSoup(f.read(1024).decode(), 'html.parser')
            return True, ip, bs.title.string.strip(), ''
    except Exception as e:
        return False, ip, e, ''


def idna2ascii(url):
    """Converts unicode url to ascii"""
    from urllib.parse import quote, urlsplit, urlunsplit
    parts = urlsplit(url)
    return urlunsplit((
        parts.scheme,
        parts.netloc.encode('idna').decode('ascii'),
        quote(parts.path),
        quote(parts.query, '='),
        quote(parts.fragment),
    ))


def get_ttfb(url):
    """Get time to first byte for url in ms"""
    from time import time
    from urllib.request import build_opener, Request
    opener = build_opener()
    req = Request(idna2ascii(url))
    tim = time()
    res = opener.open(req)
    res.read(1)
    return round((time() - tim) * 1000)
