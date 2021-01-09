class Net:
    """Network tools"""
    @staticmethod
    def localip():
        """Get local network IP"""
        from lib.pt_ip import local_ip
        print(local_ip())
