#!/usr/bin/env python
"""Wide IP range actions."""

from lib.ftp import check_anon
from lib.http import check_http
from lib.ip import generate_ips
from lib.models import Fortune as FortuneModel
from lib.models import create_tables
from lib.scan import filter_ips, ips_with_port


class Fortune:
    @staticmethod
    def ftp(ip_count=10000, t=None):
        ips = generate_ips(ip_count)

        ftps = list(ips_with_port(ips, 21, workers=t, total=ip_count))

        ftps_count = len(ftps)
        print('Got', ftps_count, 'ips w ftp')

        anons = list(filter_ips(ftps, check_anon, total=ftps_count))

        for ip in anons:
            print(ip)

    @staticmethod
    def http(ip_count=1000, t=None):
        """Spins IP roulette and makes http requests
        Checks for http application title and print it if exists.
        """
        create_tables()

        ips = generate_ips(ip_count)
        ips = list(ips_with_port(ips, 80, workers=t, total=ip_count))

        results = []
        for _, ip, title in filter_ips(ips, check_http, t, ip_count):
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
