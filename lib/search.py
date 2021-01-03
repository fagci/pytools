from requests import get
from bs4 import BeautifulSoup

def yandex(query):
    response = get('https://yandex.ru/search/', {'text':query})
    soup = BeautifulSoup(response.text, 'lxml')

    res = []

    for item in soup.find_all('li', class_='serp-item'):
        result = {
            'url': item.a['href'],
            'name': item.a.text,
        }
        text = item.find('div', class_="text-container")
        if text:
            result['text'] = text.text
        res.append(result)

    return res

