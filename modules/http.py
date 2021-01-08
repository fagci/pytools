from lib.http import idna2ascii


class Http:
    """HTTP related commands"""
    @staticmethod
    def headers(url):
        from requests import get
        for key, val in iter(get(url).headers.items()):
            print('{}: {}'.format(key, val))

    @staticmethod
    def ttfb(url, c=4):
        """Measures more precisely than requests (- dns query) time to first byte for given url"""
        from time import time
        from urllib.request import build_opener, Request
        opener = build_opener()
        results = []
        for _ in range(c):
            req = Request(idna2ascii(url))
            tim = time()
            res = opener.open(req)
            res.read(1)
            ttfb = round((time() - tim) * 1000)
            results.append(ttfb)
            print('{} ms'.format(ttfb))
        print('=' * 30)
        print('min: {} max: {} mid: {}'.format(min(results),
                                               max(results), sum(results) / len(results)))
