#!/usr/bin/env python
from bs4 import BeautifulSoup
import fire
from requests import get


def main(url, selector=None):
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    if selector:
        for res in soup.select(selector):
            soup = BeautifulSoup(str(res), 'html.parser')
            print(soup.prettify())
    else:
        print(soup.prettify())


if __name__ == "__main__":
    fire.Fire(main)
