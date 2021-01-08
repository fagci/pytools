from lib.ip import local_ip


class Net:
    """Network tools"""
    @staticmethod
    def localip():
        """Get local network IP"""
        print(local_ip())
