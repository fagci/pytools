from functools import partial
from lib.ip import generate_ips
from lib.ftp import check_anon
from lib.scan import filter_ips, ips_with_port


class FtpFortune:
    @staticmethod
    def spin(ip_count=10000, t=None):
        from tqdm import tqdm

        ips = generate_ips(ip_count)

        prg = partial(tqdm, total=ip_count)
        ftps = ips_with_port(ips, 21, workers=t, result_fn=prg)

        ftps_count = len(ftps)
        print('Got', ftps_count, 'ips w ftp')

        prg = partial(tqdm, total=ftps_count)
        anons = filter_ips(ftps, check_anon, result_fn=prg)

        for ip in anons:
            print(ip)
