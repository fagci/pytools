class Http:
    """HTTP related commands"""
    @staticmethod
    def server(ip='127.0.0.1', port=8080):
        import http.server
        import socketserver
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer((ip, port), Handler) as httpd:
            print("serving at port", port)
            httpd.serve_forever()

    @staticmethod
    def headers(url):
        from requests import get
        for key, val in iter(get(url).headers.items()):
            print('{}: {}'.format(key, val))

    @staticmethod
    def ttfb(url, c=4):
        """Measures more precisely than requests (- dns query) time to first byte for given url"""
        from statistics import mean
        from lib.pt_http import get_ttfb

        results = []
        for _ in range(c):
            ttfb = get_ttfb(url)
            results.append(ttfb)
            print('{} ms'.format(ttfb))
        print('=' * 30)
        print('min: {} max: {} mid: {}'.format(min(results),
                                               max(results), mean(results)))
