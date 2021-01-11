from ftplib import FTP


def check_anon(ip: str) -> tuple:
    """Check anonymous FTP connection, returns ip if success"""
    try:
        with FTP(ip, timeout=15.0) as ftp:
            ftp.login()
            ls = []
            ftp.dir(ls.append)
            dd = '\n'.join(ln[29:].strip() for ln in ls)
            return (True, ip, ftp.getwelcome().splitlines(False)[0], dd)
    except:
        return (False, None, None, None)
