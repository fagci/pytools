#!/usr/bin/env python
"""
Retrieves ipv4 dns nameservers,
and get fastest (<100ms) for your location/network.

By fagci (github.com/fagcinsk)
"""
from re import compile
from concurrent.futures import ThreadPoolExecutor as TPE
from time import time

from requests import get
from dns.resolver import Answer, Resolver
from tqdm import tqdm


ipv4_re = compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


def get_nameservers() -> list:
    url = 'https://public-dns.info/nameservers.csv'
    lines = get(url).text.splitlines(False)
    col_names = lines[0].split(',')
    """
    ip_address
    name
    as_number
    as_org
    country_code
    city
    version
    error
    dnssec
    reliability
    checked_at
    created_at
    """
    items = []
    for line in lines[1:]:
        row = dict(zip(col_names,line.split(',')))
        ip = row['ip_address']
        if not ipv4_re.match(ip):
            continue
        if row.get('reliability') != '1.00':
            continue
        items.append(row)
    return items


def check(nameserver):
    resolver = Resolver(configure=False)
    resolver.nameservers = [nameserver['ip_address']]
    try:
        t = time()
        res:Answer = resolver.resolve('ya.ru', lifetime=0.1)
        if len(res.rrset) > 0:
            nameserver['time'] = round((time() - t) * 1000)
    except:
        pass
    return nameserver


def get_list():
    nameservers = get_nameservers()
    with TPE() as executor:
        results = []
        for res in tqdm(executor.map(check, nameservers), total=len(nameservers)):
            tim = res.get('time')
            if tim:
                results.append(res)

    for res in sorted(results,key=lambda row: row['time']):
        ip = res.get('ip_address')
        name = res.get('name') or '-'
        tim = res.get('time') or '-'
        print(f'{ip:<15} {tim:>3} ms {name}')


def main():
    get_list()


if __name__ == "__main__":
    main()
