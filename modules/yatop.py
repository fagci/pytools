class Yatop:
    def __init__(self):
        from os import getenv
        from dotenv import load_dotenv
        from yandex_search import Yandex

        load_dotenv()

        self._searcher = Yandex(getenv('YA_API_USER'), getenv('YA_API_KEY'))

    def run(self, domain, query):

        from lib.pt_http import idna2ascii

        domain_ascii = idna2ascii(domain)
        position: str = '-'
        total = 0
        for page in range(2):
            results = self._searcher.search(query, page).items
            total += len(results)

            for pos, item in enumerate(results, start=1):
                if item['url'].startswith(domain_ascii):
                    position = str(pos)
                    break

            if position != '-':
                break

        print('{}, "{}" => {}/{}'.format(domain, query, position, total))
