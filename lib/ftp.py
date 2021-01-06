from ftplib import FTP


def check_anon(ip: str) -> str:
    """Check anonymous FTP connection, returns ip if success"""
    try:
        with FTP(ip, timeout=15.0) as ftp:
            ftp.login()
            return ip
    except:
        return ''
