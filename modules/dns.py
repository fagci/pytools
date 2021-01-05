#!/usr/bin/env python
from concurrent.futures import ThreadPoolExecutor
from re import compile
from time import time

from dns.resolver import Answer, Resolver
from requests import get
from tqdm import tqdm


ipv4_re = compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


class Dns:
    """Perform DNS related actions"""

    def __init__(self):
        self.ns_source = 'https://public-dns.info/nameservers.csv'

    def _check(self, nameserver):
        """Check NS for condition timeout"""

        resolver = Resolver(configure=False)
        resolver.nameservers = [nameserver['ip_address']]

        t = time()
        try:
            res: Answer = resolver.resolve(
                self.domain_to_resolve, lifetime=self.max_s)
            if res.rrset:
                nameserver['time'] = round((time() - t) * 1000)
        except:
            pass

        return nameserver

    def fastest(self, max_ms: int = 100, domain='ya.ru'):
        """Retrieves ipv4 dns nameservers,
        and get fastest (<100ms by default)
        for your location/network."""

        self.max_s = float(max_ms) / 1000.0
        self.domain_to_resolve = domain

        nameservers = self._get_nameservers()

        with ThreadPoolExecutor() as executor:
            results = []
            for res in tqdm(executor.map(self._check, nameservers), total=len(nameservers)):
                if res.get('time'):
                    results.append(res)

        for res in sorted(results, key=lambda row: row['time']):
            ip = res.get('ip_address')
            name = res.get('name') or '-'
            tim = res.get('time') or '-'
            print(f'{ip:<15} {tim:>3} ms {name}')

    def _get_nameservers(self) -> list:
        """Retrieves nameservers info from source

        Keys:
        ip_address, name, as_number, as_org,
        country_code, city, version, error, dnssec,
        reliability, checked_at, created_at"""

        lines = get(self.ns_source).text.splitlines(False)
        col_names = lines[0].split(',')

        items = []
        is_ipv4 = ipv4_re.match
        for line in lines[1:]:
            row = dict(zip(col_names, line.split(',')))
            ip = row['ip_address']
            if is_ipv4(ip) and row.get('reliability') == '1.00':
                items.append(row)

        return items
