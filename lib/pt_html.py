from lib.pt_http import idna2ascii


def get_ahrefs(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.select('a[href]'):
        href = a.get('href')
        if href:
            yield href.strip()


def get_related_ahrefs(html, url):
    from urllib.parse import urlparse
    parts = urlparse(url)
    ascii_parts = urlparse(idna2ascii(url))
    base_url = '{}://{}'.format(parts.scheme, parts.netloc)
    ascii_base_url = '{}://{}'.format(ascii_parts.scheme, ascii_parts.netloc)
    for href in get_ahrefs(html):
        if href.startswith('//'):
            href = '{}:{}'.format(parts.scheme, href)
        elif href.startswith('/'):
            href = base_url + href
        elif href.startswith('./'):
            href = url + href[1:]
        if href.startswith((base_url, ascii_base_url)):
            yield href


def get_page_ahrefs(url):
    from requests import get
    return get_related_ahrefs(get(url).content, url)
