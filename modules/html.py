#!/usr/bin/env python
"""HTML utilities"""
from bs4 import BeautifulSoup
from requests import get


class Html:
    __doc__ = __doc__

    def source(self, url, selector=None):
        """Shows prettified html source,
        or some part by selector if specified

        selector -- css selector, ex.: ul>li
        """
        response = get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        if selector:
            for res in soup.select(selector):
                soup = BeautifulSoup(str(res), 'html.parser')
                print(soup.prettify())
        else:
            print(soup.prettify())
