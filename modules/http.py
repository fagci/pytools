from lib.http import get_ttfb


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
        results = []
        for _ in range(c):
            ttfb = get_ttfb(url)
            results.append(ttfb)
            print('{} ms'.format(ttfb))
        print('=' * 30)
        print('min: {} max: {} mid: {}'.format(min(results),
                                               max(results), sum(results) / len(results)))
