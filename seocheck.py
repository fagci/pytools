#!/usr/bin/env python
from concurrent.futures import ThreadPoolExecutor
import requests
import bs4
import fire
from urllib.parse import urlparse

MAX_TTFB = 180
TITLE_MIN_LENGTH = 20
TITLE_MAX_LENGTH = 60
DESCRIPTION_MIN_LENGTH = 70
DESCRIPTION_MAX_LENGTH = 160

def check_meta(page: bs4.BeautifulSoup):
    title = page.find('title').text
    description = page.find('meta', {'name':'description'}).get('content')
    t_minlen = len(title) >= TITLE_MIN_LENGTH
    t_maxlen = len(title) <= TITLE_MAX_LENGTH
    d_minlen = len(description) >= DESCRIPTION_MIN_LENGTH
    d_maxlen = len(description) <= DESCRIPTION_MAX_LENGTH

    return t_minlen and t_maxlen and d_minlen and d_maxlen

def check_ttfb(response: requests.Response):
    return response.elapsed.total_seconds() * 1000 < MAX_TTFB

def get_response(url):
    return requests.get(url)

def get_page(response):
    return bs4.BeautifulSoup(response.text, 'lxml')


def crawl(url, processed_urls:set=set()):
    if url in processed_urls:
        return {}
    processed_urls.add(url)
    response = get_response(url)
    page = get_page(response)

    ttfb = check_ttfb(response)
    meta = check_meta(page)

    pp = urlparse(url)
    path = f'{pp.path}?{pp.query}' if pp.query else pp.path

    print(f'{path}: ttfb={ttfb}, meta={meta}')

    links = page.find_all('a')
    urls = [a.get('href') for a in links if a.get('href')]
    with ThreadPoolExecutor() as ex:
        ex.map(crawl, urls)


def main(start_url):
    crawl(start_url)

if __name__ == "__main__":
    try:
        fire.Fire(main)
    except KeyboardInterrupt:
        print('Interrupted by user')
