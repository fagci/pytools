from requests import get
from bs4 import BeautifulSoup

def yandex(query):
    r = get('https://yandex.ru/search/', {'text':query})
    soup = BeautifulSoup(r.text, 'lxml')
    res = []
    for l in soup.find_all('li', class_='serp-item'):
        result = {
            'url': l.a['href'],
            'name': l.a.text,
        }
        text = l.find('div', class_="text-container")
        if(text):
            result['text'] = text.text
        res.append(result)
    return res

