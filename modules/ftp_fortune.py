from lib.ip import generate_ips
from lib.ftp import check_anon
from lib.network import portchecker


class FtpFortune:
    @staticmethod
    def spin(ip_count=10000, t=None):
        from concurrent.futures import ThreadPoolExecutor
        from tqdm import tqdm

        ips = generate_ips(ip_count)

        check_ftp = portchecker(21)

        with ThreadPoolExecutor(t) as ex:
            res = ex.map(check_ftp, ips)
            ftps = [ip for ip in tqdm(res, total=ip_count) if ip]

        ftps_count = len(ftps)
        print('Got', ftps_count, 'ips w ftp')

        with ThreadPoolExecutor() as ex:
            res = ex.map(check_anon, ftps)
            anons = [ip for ip in tqdm(res, total=ftps_count) if ip]

        for ip in anons:
            print(ip)
