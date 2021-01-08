#!/usr/bin/env python
"""Wide IP range actions."""

from lib.pt_ftp import check_anon
from lib.pt_http import check_http
from lib.pt_ip import generate_ips
from lib.pt_models import Fortune as FortuneModel
from lib.pt_models import create_tables
from lib.pt_scan import filter_ips, ips_with_port


class Fortune:
    def __init__(self, ips_count=5000, t=None) -> None:
        create_tables()
        self.ips_count = ips_count
        self.workers = t

    def ftp(self):
        """Gather FTP hosts with anonymous access"""
        self._generate_ips()
        self._leave_ips_with_port(21)
        self._filter_service(check_anon)

        for ip in self.ips:
            print(ip)

    def http(self):
        """Gather hosts with site on 80 port"""
        self._generate_ips()
        self._leave_ips_with_port(80)
        self._filter_service(check_http)

        for _, ip, title in self.ips:
            print(f'{ip:<15} {title}')
            try:
                FortuneModel.create(ip=ip, title=title)
            except Exception as e:
                print(e)

    @staticmethod
    def list():
        """Get list of previous spins (ips with http title)"""
        for item in FortuneModel.select().order_by(FortuneModel.title):
            print('{}\t{}'.format(item.ip, item.title))

    @staticmethod
    def ip_list(count: int = 100):
        """Generates list of random ips"""
        for ip in generate_ips(count):
            print(ip)

    def _generate_ips(self):
        print('[*] create generator of', self.ips_count, 'ips...')
        self.ips = generate_ips(self.ips_count)

    def _leave_ips_with_port(self, port: int):
        print('[*] Gathering ips with', port, 'port, using',
              (self.workers or '[default]'), 'workers...')
        self.ips = list(ips_with_port(
            self.ips, port, self.workers, total=self.ips_count))
        self.ips_count = len(self.ips)
        print('Got', self.ips_count, 'ips.')

    def _filter_service(self, fn):
        print('[*] Filtering service:', self.ips_count, 'ips...')
        self.ips = list(filter_ips(self.ips, fn, total=self.ips_count))
        self.ips_count = len(self.ips)
        print('Got', self.ips_count, 'ips.')
