import requests
import bs4
import re
import pymorphy2

# Инициализируем морфологический анализатор
morph = pymorphy2.MorphAnalyzer()

HEADERS = {
    'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415;'
              ' _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2;'
              ' __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  '(KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0'}

base_url = 'https://habr.com'
url = base_url + '/ru/all/'

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def responce_get(urls, headers):
    """Поиск статей по содержимому страницы сайта"""
    response = requests.get(url=urls, headers=headers)
    response.raise_for_status()
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    return articles


def find_link(articles, base_urls):
    """Поиск ссылок на статьи с главной страницы"""
    href = articles.find(class_='tm-article-snippet__title-link').attrs['href']
    links = base_urls + href
    return links


def keyword_search(articles, keywords):
    """Поиск ключевых слов по всему тексту статьи"""
    for article in articles:
        text_blocks = article.find(class_='tm-article-body')  # Поиск блоков текста
        text_blocks = set(text_block.text.strip() for text_block in text_blocks)  # Объединение блоков текста в массив
        for text_block in text_blocks:
            text_block = re.sub(r'[.,!?/]', ' ', text_block)  # Убираем знаки перпинания
            text_block = text_block.split()  # Разделяем строку на слова
            hub_list = []  # Создаем список записи слов в начальной форме
            for word in text_block:
                next_hub = morph.parse(word)[0].normal_form  # Приводим слова к начальной форме
                hub_list.append(next_hub)
            if set(keywords) & set(hub_list):  # Сравниваем множества найденных и ключевых слов на пересечение
                title = article.find('h1').find('span').text  # Получаем заголовок искомой статьи
                hub_datetime = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
                hub_date, hub_time = hub_datetime.split(', ')  # Получаем дату искомой статьи
                result = hub_date + ' - ' + title + ' - ' + link  # Собираем дату, заголовок и ссылку в "кучу"
                print(result)  # Выводим результат
                return result


if __name__ == '__main__':

    hubs = responce_get(url, HEADERS)   # Получаем данные с сайта
    for hub in hubs:  # Проходим по preview статей
        link = find_link(hub, base_url)  # Получаем ссылки на статьи
        hub_articles = responce_get(link, HEADERS)
        keyword_search(hub_articles, KEYWORDS)  # Проверяем содержимое статей по ключевым словам
