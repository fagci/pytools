#!/usr/bin/env python
from concurrent.futures import ThreadPoolExecutor
from csv import writer
import sys
from urllib.parse import urlparse

import bs4
import requests
from requests.models import Response
from tqdm import tqdm

OK_CODES = [200]
MAX_TTFB = 180
TITLE_MIN_LENGTH = 20
TITLE_MAX_LENGTH = 70
DESCRIPTION_MIN_LENGTH = 70
DESCRIPTION_MAX_LENGTH = 200


class Seo:
    """SEO tools"""

    def check(self, sitemap_url, t=4, o=''):
        """Performs base technical SEO check for urls from sitemap

        sitemap_url -- url pointing to sitemap.xml
        t -- number of threads
        Keep in mind: when more threads,
        ttfb may be larger than MAX_TTFB and test will fail
        """
        self.checks = {}
        for func in dir(self):
            if func.startswith('check_'):
                fn = getattr(self, func)
                if callable(fn):
                    self.checks[func[6:]] = fn

        sys.stderr.write('Check sitemap...\n')
        xml = self._get_page(self._get_response(sitemap_url))
        urls = [a.text for a in xml.find_all('loc')]
        total = len(urls)
        sys.stderr.write(f'found {total} urls\n')

        results = []
        with ThreadPoolExecutor(max_workers=t) as ex:
            for r in tqdm(ex.map(self._check, urls), total=total, unit='url'):
                results.append(r)
                # print(r.get('path'))
                # for k, v in r.items():
                #     if k == 'path':
                #         continue
                #     print(f'  {k}: {v}')

        if o:
            with open(o, 'w') as output:
                self._write_csv(results, output)
        elif o == '-':
            output = sys.stdout
            self._write_csv(results, output)

    # checks

    @staticmethod
    def check_code(r: Response, _):
        """Response code must be ok"""
        return r.status_code in OK_CODES

    @staticmethod
    def check_ttfb(r: Response, _):
        """Time to first byte must be small"""
        return r.elapsed.total_seconds() * 1000 < MAX_TTFB

    @staticmethod
    def check_len_title(_, p):
        """Title length of page will be in range"""
        return TITLE_MIN_LENGTH < len(p.title.text) < TITLE_MAX_LENGTH

    @staticmethod
    def check_len_desc(_, p):
        """Description length of page will be in range"""
        d = p.find('meta', {'name': 'description'}).get('content')
        return DESCRIPTION_MIN_LENGTH < len(d) < DESCRIPTION_MAX_LENGTH

    # /checks

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

        result = {
            'path': path,
        }

        for check_name, fn in self.checks.items():
            result[check_name] = int(fn(response, page))

        return result

    @staticmethod
    def _write_csv(results, output):
        w = writer(output)
        w.writerow(results[0].keys())
        for r in results:
            w.writerow(r.values())
