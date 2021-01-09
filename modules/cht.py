class Cht:
    @staticmethod
    def run(*args):
        """Get cheat, example: python named tuple"""
        from requests import get
        from urllib.parse import quote
        BASE_URL = 'http://cht.sh'

        url = '{}/{}'.format(BASE_URL, args[0])

        sq = quote('+'.join(args[1:]))

        if sq:
            url += '/{}'.format(sq)

        print(get(url).text)
