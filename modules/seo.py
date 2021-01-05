#!/usr/bin/env python
from concurrent.futures import ThreadPoolExecutor
from csv import writer
import sys
from urllib.parse import urlparse

import bs4
import requests
from tqdm import tqdm

OK_CODES = [200]
MAX_TTFB = 180
TITLE_MIN_LENGTH = 20
TITLE_MAX_LENGTH = 70
DESCRIPTION_MIN_LENGTH = 70
DESCRIPTION_MAX_LENGTH = 200

checks = {
    'len_title': lambda t: TITLE_MIN_LENGTH < len(t) < TITLE_MAX_LENGTH,
    'len_desc': lambda d: DESCRIPTION_MIN_LENGTH < len(d) < DESCRIPTION_MAX_LENGTH,
    'ttfb': lambda t: t < MAX_TTFB,
}


class Seo:
    """SEO tools"""

    @staticmethod
    def _get_response(url):
        return requests.get(url)

    @staticmethod
    def _get_page(response):
        return bs4.BeautifulSoup(response.text, 'lxml')

    def _check(self, url):
        response = self._get_response(url)
        page = self._get_page(response)

        p_url = urlparse(url)
        path = f'{p_url.path}?{p_url.query}' if p_url.query else p_url.path

        title = page.find('title').text
        desc = page.find('meta', {'name': 'description'}).get('content')

        return {
            'path': path,
            'code': int(response.status_code in OK_CODES),
            'ttfb': int(checks['ttfb'](response.elapsed.total_seconds() * 1000)),
            'title': int(checks['len_title'](title)),
            'description': int(checks['len_desc'](desc)),
        }

    def check(self, sitemap_url, t=4, o=''):
        """Performs base technical SEO check for urls from sitemap

        sitemap_url -- url pointing to sitemap.xml
        t -- number of threads
        Keep in mind: when more threads,
        ttfb may be larger than MAX_TTFB and test will fail
        """
        sys.stderr.write('Check sitemap...\n')
        xml = self._get_page(self._get_response(sitemap_url))
        urls = [a.text for a in xml.find_all('loc')]
        total = len(urls)
        sys.stderr.write(f'found {total} urls\n')

        results = []
        with ThreadPoolExecutor(max_workers=t) as ex:
            for r in tqdm(ex.map(self._check, urls), total=total, unit='url'):
                results.append(r)

        fail = 0
        success = 0
        for r in results:
            for c in r.keys():
                if c != 'path':
                    b = r[c]
                    if b:
                        success += 1
                    else:
                        fail += 1

        sys.stderr.write(f'Success: {success}, fail: {fail}.\n')
        if o:
            with open(o, 'w') as output:
                self._write_csv(results, output)
        elif o == '-':
            output = sys.stdout
            self._write_csv(results, output)

    @staticmethod
    def _write_csv(results, output):
        w = writer(output)
        w.writerow(results[0].keys())
        for r in results:
            w.writerow(r.values())
