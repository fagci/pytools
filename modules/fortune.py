#!/usr/bin/env python
"""Wide IP range actions."""

from lib.ftp import check_anon
from lib.http import check_http
from lib.ip import generate_ips
from lib.models import Fortune as FortuneModel
from lib.models import create_tables
from lib.scan import filter_ips, ips_with_port


class Fortune:
    def __init__(self, ips_count=5000, t=None) -> None:
        create_tables()
        self.ips = generate_ips(ips_count)
        self.ips_count = ips_count
        self.workers = t

    def leave_ips(self, port: int):
        print('[*] Making ips for', port, 'port')
        self.ips = list(ips_with_port(
            self.ips, port, self.workers, total=self.ips_count))
        self.ips_count = len(self.ips)
        print('Got', self.ips_count, 'ips for', port, 'port')

    def ftp(self):
        self.leave_ips(21)
        anons = list(filter_ips(self.ips, check_anon, total=self.ips_count))

        for ip in anons:
            print(ip)

    def http(self):
        self.leave_ips(80)

        results = []
        for _, ip, title in filter_ips(self.ips, check_http, self.workers, self.ips_count):
            try:
                FortuneModel.create(ip=ip, title=title)
            except Exception as e:
                print(e)
            results.append((ip, title))

        print(len(results), 'results')
        for ip, title in results:
            print(f'{ip:<15} {title}')

    @staticmethod
    def list():
        """Get list of previous spins (ips with http title)"""
        for item in FortuneModel.select().order_by(FortuneModel.title):
            print(f'{item.ip}\t{item.title}')
