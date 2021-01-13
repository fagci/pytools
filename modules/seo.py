OK_CODES = [200]
MAX_TTFB = 180
TITLE_MIN_LENGTH = 20
TITLE_MAX_LENGTH = 70
DESCRIPTION_MIN_LENGTH = 70
DESCRIPTION_MAX_LENGTH = 200


class Seo:
    """SEO tools"""

    def all(self, url: str, t: int = 4, o=''):
        url = url.rstrip('/')
        robots_url = f'{url}/robots.txt'
        sitemap_url = f'{url}/sitemap.xml'
        if self._get_response(robots_url).status_code == 200:
            print('robots.txt exists')
        if self._get_response(sitemap_url).status_code == 200:
            print('sitemap.xml exists, running checks...')
            self.sitemap(sitemap_url, t, o)

    def sitemap(self, sitemap_url, t=4, o=''):
        """Performs base technical SEO check for urls from sitemap

        sitemap_url -- url pointing to sitemap.xml
        t -- number of threads
        Keep in mind: when more threads,
        ttfb may be larger than MAX_TTFB and test will fail
        """
        self.checks = {}
        for func in dir(self):
            if func.startswith('_check_'):
                fn = getattr(self, func)
                if callable(fn):
                    self.checks[func[6:]] = fn
                    print(fn.__doc__.format(**globals()))

        import sys
        sys.stderr.write('Check sitemap...\n')
        xml = self._get_page(self._get_response(sitemap_url))
        urls = [a.text for a in xml.find_all('loc')]
        total = len(urls)
        sys.stderr.write(f'found {total} urls\n')
        from tqdm import tqdm
        from concurrent.futures import ThreadPoolExecutor
        from urllib.parse import urlparse
        from lib.pt_models import SEOSession, SEOCheckResult, create_tables

        create_tables()

        parsed_url = urlparse(sitemap_url)
        base_url = '{}://{}'.format(parsed_url.scheme, parsed_url.netloc)
        seo_session = SEOSession.create(
            base_url=base_url, options={'workers': t})

        results = []
        with ThreadPoolExecutor(max_workers=t) as ex:
            for r in tqdm(ex.map(self._check, urls), total=total, unit='url'):
                results.append(r)
                SEOCheckResult.create(session=seo_session, **r)

        if o:
            with open(o, 'w') as output:
                self._write_csv(results, output)
        elif o == '-':
            output = sys.stdout
            self._write_csv(results, output)

    # checks

    @staticmethod
    def _check_code(r, _):
        """Response code must be in {OK_CODES}"""
        return {'code_ok': r.status_code in OK_CODES, 'code': r.status_code}

    @staticmethod
    def _check_ttfb(r, _):
        """Time to first byte must be < {MAX_TTFB}"""
        ttfb = int(r.elapsed.total_seconds() * 1000)
        return {'ttfb_ok': ttfb < MAX_TTFB, 'ttfb': ttfb}

    @staticmethod
    def _check_len_title(_, p):
        """Title length must be {TITLE_MIN_LENGTH} < x < {TITLE_MAX_LENGTH}"""
        title_tag = p.title
        title = title_tag.text if title_tag else ''
        tlen = len(title)
        return {
            'title_ok': TITLE_MIN_LENGTH < tlen < TITLE_MAX_LENGTH,
            'title_len': tlen,
            'title_text': title
        }

    @staticmethod
    def _check_len_desc(_, p):
        """Description length must be {DESCRIPTION_MIN_LENGTH} < x < {DESCRIPTION_MAX_LENGTH}"""
        desc_tag = p.find('meta', {'name': 'description'})
        d = desc_tag.get('content') if desc_tag else ''
        dlen = len(d)
        return {
            'desc_ok': DESCRIPTION_MIN_LENGTH < dlen < DESCRIPTION_MAX_LENGTH,
            'desc_len': dlen,
            'desc_text': d
        }

    @staticmethod
    def _check_headings(_, p):
        """Validate html"""
        from re import compile
        headings = []
        for h in p.find_all(compile('^h[1-6]$')):
            tag = h.name
            headings.append('{}{}: {}'.format('  '*int(tag[1:]), tag, h.text))

        return {
            'headings': '\n'.join(headings),
        }

    @staticmethod
    def _check_validity(_, p):
        """Validate html"""
        return {
            'validation': '',
        }

    # /checks

    @staticmethod
    def _get_response(url):
        import requests
        return requests.get(url)

    @staticmethod
    def _get_page(response):
        from bs4 import BeautifulSoup
        return BeautifulSoup(response.text, 'lxml')

    def _check(self, url):
        from urllib.parse import urlparse
        response = self._get_response(url)
        page = self._get_page(response)

        p_url = urlparse(url)
        path = f'{p_url.path}?{p_url.query}' if p_url.query else p_url.path

        result = {
            'url': path,
        }

        for _, fn in self.checks.items():
            result = {**result, **fn(response, page)}

        return result

    @staticmethod
    def _write_csv(results, output):
        from csv import writer
        w = writer(output)
        w.writerow(results[0].keys())
        for r in results:
            w.writerow(r.values())
