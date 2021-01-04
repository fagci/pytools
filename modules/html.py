#!/usr/bin/env python
from bs4 import BeautifulSoup
from requests import get


class Html:
    def source(self, url, selector=None):
        response = get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        if selector:
            for res in soup.select(selector):
                soup = BeautifulSoup(str(res), 'html.parser')
                print(soup.prettify())
        else:
            print(soup.prettify())
