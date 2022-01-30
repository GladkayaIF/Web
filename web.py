import requests
import bs4
import re

HEADERS = {'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
          'Accept-Language': 'ru-RU,ru;q=0.9',
          'Sec-Fetch-Dest': 'document',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-Site': 'same-origin',
          'Sec-Fetch-User': '?1',
          'Cache-Control': 'max-age=0',
          'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
          'sec-ch-ua-mobile': '?0'
}
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'воздух','LINQ']

response = requests.get('https://habr.com/ru/all/', headers=HEADERS)
response.raise_for_status()
soup = bs4.BeautifulSoup(response.text, features='html.parser')

articles = soup.find_all('article')
pattern = r"[!*.,(),?/\\@#$%\^&-_+=\[\]{}<>:;\"']"

temp_words = []
for key in KEYWORDS:
    temp_words.append(key.lower())
key_words = set(temp_words)


for article in articles:
    title = article.find('h2')
    meta = article.find('div')

    article_date = meta.find_all('span', class_="tm-article-snippet__datetime-published")
    datetime_pub = [ad.find('time').text for ad in article_date]

    article_title = {}
    article_title = set(re.sub(pattern,r"",title.text.lower()).split(' '))

    article_body = meta.find_all('div', class_="article-formatted-body article-formatted-body_version-2")

    article_str = ''
    for ab in article_body:
         article_str = str(ab.text)

    article_text = {}
    article_text = set(re.sub(pattern, r"", article_str.lower()).split(' '))

    if (key_words & article_title) or (key_words & article_text):
        a_tag = title.find('a')
        href = a_tag.attrs['href']
        url = 'https://habr.com' + href
        result = datetime_pub[0]+' '+title.text+' '+url
        print(result)
        print('----')

