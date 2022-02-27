import requests
import bs4
import re
import pymorphy2

# Инициализируем морфологический анализатор
morph = pymorphy2.MorphAnalyzer()

# Маскируемся под браузер
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
                  ' (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0'}

base_url = 'https://habr.com'
url = base_url + '/ru/all/'

# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


if __name__ == '__main__':
    response = requests.get(url=url, headers=HEADERS)  # Получаем данные с сайта
    response.raise_for_status()  # Проверяем успешность запроса
    text = response.text  # Получаем текст из данных
    soup = bs4.BeautifulSoup(text, features='html.parser')  # Парсим текст с помощью библиотеки
    articles = soup.find_all('article')  # Разбираем текст на статьи
    for article in articles:
        # Получаем содержимое заголовков и preview статей
        hubs_title = article.find_all(class_='tm-article-snippet__title tm-article-snippet__title_h2')
        hubs_body = article.find_all(class_='article-formatted-body article-formatted-body_version-2')
        hubs = hubs_title + hubs_body
        hubs = set(hub.text.strip() for hub in hubs)  # Преобразуем строки в массив слов для поиска
        for hub in hubs:
            hub = re.sub(r'[.,!?/]', ' ', hub)  # Убираем знаки перпинания
            hub = hub.split()  # Разделяем строку на слова
            hub_list = []
            for word in hub:
                next_hub = morph.parse(word)[0].normal_form  # Приводим слова к начальной форме
                hub_list.append(next_hub)
            if set(KEYWORDS) & set(hub_list):  # Сравниваем множества найденных и ключевых слов на пересечение
                href = article.find(class_='tm-article-snippet__title-link').attrs['href']
                link = base_url + href  # Получаем ссылку на статью
                title = article.find('h2').find('span').text  # Получаем заголовок искомой статьи
                hub_datetime = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
                hub_date, hub_time = hub_datetime.split(', ')  # Получаем дату искомой статьи
                result = hub_date + ' - ' + title + ' - ' + link  # Собираем дату, заголовок и ссылку в "кучу"
                print(result)  # Выводим результат
