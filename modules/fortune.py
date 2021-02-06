#!/usr/bin/env python
"""Wide IP range actions."""


class Fortune:
    def __init__(self, ips_count=5000, t=None) -> None:
        from lib.pt_models import create_tables
        create_tables()
        self._ips_count = ips_count
        self.workers = t or 16

    def ftp(self):
        """Gather FTP hosts with anonymous access"""
        from lib.pt_ftp import check_anon
        self._generate_ips()
        self._leave_ips_with_port(21)
        self._filter_service(check_anon)
        self._write_results(21)

    def http(self):
        """Gather hosts with site on 80 port"""
        from lib.pt_http import check_http
        self._generate_ips()
        self._leave_ips_with_port(80)
        self._filter_service(check_http)
        self._write_results(80)

    @staticmethod
    def list(**kwargs):
        """Get list of previous spins (ips with http title)"""
        from lib.pt_models import FortuneIP
        items = FortuneIP.select()
        if kwargs:
            for k, v in kwargs.items():
                items = items.where(getattr(FortuneIP, k) % v)
        for item in items.order_by(FortuneIP.created_at):
            print('{}\t{}'.format(item.ip, item.title))

    @staticmethod
    def ips(count: int = 100):
        """Generates list of random ips"""
        from lib.pt_ip import generate_ips
        for ip in generate_ips(count):
            print(ip)

    def _generate_ips(self):
        print('[*] create generator of', self._ips_count, 'ips...')
        from lib.pt_ip import generate_ips
        self._ips = generate_ips(self._ips_count)

    def _leave_ips_with_port(self, port: int):
        from lib.pt_scan import ips_with_port
        print('[*] Gathering ips with', port, 'port, using',
              self.workers, 'workers...')
        self._ips = list(ips_with_port(
            self._ips, port, self.workers, total=self._ips_count))
        self._ips_count = len(self._ips)
        print('Got', self._ips_count, 'ips.')

    def _filter_service(self, fn):
        from lib.pt_scan import filter_ips2
        print('[*] Filtering service:', self._ips_count, 'ips...')
        self._ips = list(filter_ips2(self._ips, fn, total=self._ips_count))
        self._ips_count = len(self._ips)
        print('Got', self._ips_count, 'ips.')

    def _write_results(self, port):
        from lib.pt_models import FortuneIP
        for _, ip, title, description in self._ips:
            try:
                FortuneIP.create(ip=ip, port=port, title=title,
                                 description=description)
            except Exception as e:
                print(e)
