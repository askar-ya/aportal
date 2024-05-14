import json
import requests
import re
from bs4 import BeautifulSoup


def get_yandex_page(location: str, type_obj: str, q: dict) -> list:
    with open('cookies_yandex.json', 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    with open('dict_cities.json', 'r', encoding='utf-8') as f:
        city = json.load(f)[location]['ya']
    headers = {
        'authority': 'realty.ya.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'referer': f'https://realty.ya.ru/{city}/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version-list': '"Chromium";v="122.0.6261.156", "Not(A:Brand";v="24.0.0.0", '
                                       '"YaBrowser";v="24.4.1.899", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
    }

    # тип сделки
    if q['deal'] == 'buy':
        url = f'https://realty.ya.ru/{city}/kupit/'
    else:
        url = f'https://realty.ya.ru/{city}/snyat/'

    # типы объектов яндекс-realty
    ob_d = {
        'flat': 'kvartira/',
        'room': 'komnata/',
        'suburban': 'dom/',
        'plot': 'uchastok/',
        'garage': 'garazh/',
        'commercial': 'kommercheskaya-nedvizhimost/'
    }

    # выбираем тип объекта
    url += ob_d[type_obj]

    # создаем словарь параметров
    params = {}

    # фильтр цены
    if q['price'] is not None:
        if q['price'][0] != '0':
            params['priceMin'] = q['price'][0]
        if len(q['price']) > 1:
            params['priceMax'] = q['price'][1]

    # указатель новостройки
    if 'cycle' in q:
        if q['cycle'] != 'all':
            if q['cycle'] == 'new':
                params['newFlat'] = 'YES'
            elif q['cycle'] == 'used':
                params['newFlat'] = 'NO'

    # указатель срока аренды
    if 'period' in q:
        if q['period'] is not None:
            if q['period'] == 'days':
                params['rentTime'] = 'SHORT'

    # фильтр площади
    if 'square' in q:
        if q['square'] is not None:
            params['areaMin'] = q['square'][0]
            if len(q['square']) > 1:
                params['areaMax'] = q['square'][1]

    # фильтр количества комнат
    if 'room_count' in q:
        if q['room_count'] is not None:
            if type_obj != 'suburban':
                rc = {
                    'studio': 'STUDIO',
                    '1': '1',
                    '2': '2',
                    '3': '3',
                    '4': 'PLUS_4',
                    '5>': 'PLUS_4'
                }
                room_count = []
                for count in q['room_count']:
                    if count != 'clear':
                        room_count.append(rc[count])
                    elif (type_obj != 'room') and (count != '1'):
                        room_count.append(rc[count])
                    else:
                        room_count.append(rc[count])
                if len(room_count) > 0:
                    params['roomsTotal'] = room_count

    # указатель типа гаража
    if 'type_garage' in q:
        if q['type_garage'] is not None:
            tg = {
                'car_place': 'PARKING_PLACE',
                'garage': 'GARAGE'
            }
            type_garage = []
            for count in q['type_garage']:
                type_garage.append(tg[count])
            params['garageType'] = type_garage

    # указатель охраны гаража
    if 'security' in q:
        if q['security'] is True:
            params['includeTag'] = '1794389'

    # тип земли
    if 'plot_type' in q:
        if q['plot_type'] is not None:
            pt = {
                'live': 'GARDEN',
                'farm': 'FARM'
            }
            plot_type = []
            for count in q['plot_type']:
                if count != 'fabric':
                    plot_type.append(pt[count])
            params['lotType'] = plot_type

    # тип ком недвижимости
    if 'commercial_type' in q:
        if q['commercial_type'] is not None:
            ct = {
                'business': 'BUSINESS_CENTER',
                'house': 'DETACHED_BUILDING',
                'mall': 'SHOPPING_CENTER',
                'government': '',
                'other': ''
            }
            commercial_type = []
            for ctype in q['plot_type']:
                if ctype not in ['government', 'other']:
                    commercial_type.append(ct[ctype])
            params['commercialBuildingType'] = commercial_type

    # направление ком недвижимости
    if 'commercial_sort' in q:
        if q['commercial_sort'] is not None:
            cs = {
                'office': 'OFFICE',
                'free': 'FREE_PURPOSE',
                'shop-place': 'RETAIL',
                'storage': 'WAREHOUSE',
                'fabric': 'MANUFACTURING',
                'food': 'PUBLIC_CATERING',
                'hotel': 'HOTEL',
                'auto-s': 'AUTO_REPAIR'
            }
            commercial_sort = []
            for ctype in q['plot_type']:
                if ctype not in ['build', 'kwork']:
                    commercial_sort.append(cs[ctype])
            params['commercialType'] = commercial_sort

    # выполняем запрос
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    # получаем все объекты
    soup = BeautifulSoup(response.text, 'lxml')
    box = soup.findAll('li', attrs={'data-seo': 'snippet'})
    data = []
    for item in box:
        link = 'https://realty.ya.ru' + item.find('a', attrs={'target': '_blank'})['href']
        price = item.find('span', class_='price').text.replace('\xa0', '')
        description = item.find('p', class_=re.compile('_description')).text
        title = item.find('span', class_=re.compile('_title')).text
        pictures = []
        for img in item.findAll('img'):
            pictures.append(f'https:{img["src"]}')
        out = {'title': title, 'description': description, 'price': price,
               'url': link, 'img': pictures}
        data.append(out)

    return data
