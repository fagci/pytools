#!/usr/bin/env python
"""
Performs base technical SEO check for urls from sitemap
"""
import sys
from csv import writer
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import bs4
import fire
import requests
from alive_progress import alive_bar

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


def get_response(url):
    return requests.get(url)


def get_page(response):
    return bs4.BeautifulSoup(response.text, 'lxml')


def check(url):
    response = get_response(url)
    page = get_page(response)

    p_url = urlparse(url)
    path = f'{p_url.path}?{p_url.query}' if p_url.query else p_url.path

    title = page.find('title').text
    desc = page.find('meta', {'name':'description'}).get('content')

    return {
        'path': path,
        'code': int(response.status_code in OK_CODES),
        'ttfb': int(checks['ttfb'](response.elapsed.total_seconds() * 1000)),
        'title': int(checks['len_title'](title)),
        'description': int(checks['len_desc'](desc)),
    }


def main(sitemap_url, t=4, o=''):
    xml = get_page(get_response(sitemap_url))
    urls = [a.text for a in xml.find_all('loc')]
    total = len(urls)

    results = []
    with ThreadPoolExecutor(max_workers=t) as ex:
        sys.stderr.write(f'found {total} urls\n')
        with alive_bar(total) as progress:
            for r in ex.map(check, urls):
                results.append(r)
                progress()

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
            write_csv(results, output)
    elif o == '-':
        output = sys.stdout
        write_csv(results, output)

def write_csv(results, output):
    w = writer(output)
    w.writerow(results[0].keys())
    for r in results:
        w.writerow(r.values())



if __name__ == "__main__":
    try:
        fire.Fire(main)
    except KeyboardInterrupt:
        print('Interrupted by user')
