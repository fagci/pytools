class Net:
    """Network tools"""
    @staticmethod
    def localip():
        """Get local network IP"""
        from lib.pt_ip import local_ip
        print(local_ip())

    @staticmethod
    def extip():
        """Get external network IP"""
        from lib.pt_ip import external_ip
        print(external_ip())

    @staticmethod
    def rdns(ip: str):
        """Make reverse dns request"""
        from socket import gethostbyaddr
        try:
            result = gethostbyaddr(ip)
            print('Host: %s\nAliases: %s\nIPs: %s' % result)
        except Exception as e:
            print(e)
