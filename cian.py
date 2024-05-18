import requests
import json
from bs4 import BeautifulSoup


def get_cian_page(location: str, type_obj: str, q: dict):
    with open('cookies_cian.json', 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    with open('dict_cities.json', 'r', encoding='utf-8') as f:
        city = json.load(f)[location]['cian']
    print(city)
    headers = {
        'authority': 'spb.cian.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/'
                  'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'max-age=0',
        'referer': f'https://{city['sub']}.cian.ru/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
    }

    params = {
        'currency': '2',
        'engine_version': '2',
        'region': city['reg']
    }

    # тип сделки
    if q['deal'] == 'buy':
        params['deal_type'] = 'sale'
    else:
        params['deal_type'] = 'rent'

    if type_obj == 'flat':
        params['offer_type'] = 'flat'
        if 'cycle' in q:
            if q['cycle'] == 'new':
                params['object_type[0]'] = '2'
            elif q['cycle'] == 'used':
                params['object_type[0]'] = '1'

    elif type_obj == 'room':
        params['offer_type'] = 'flat'
        params['room0'] = '1'

    elif type_obj == 'suburban':
        params['offer_type'] = 'suburban'
        params['object_type[0]'] = '1'
        params['object_type[1]'] = '2'
        params['object_type[2]'] = '4'

    elif type_obj == 'plot':
        params['offer_type'] = 'suburban'
        params['object_type[0]'] = '3'
        if q['plot_type'] is not None:
            pt = {
                'live': '2',
                'farm': '4',
                'fabric': '3'
            }
            for n, type_ in enumerate(q['plot_type']):
                params[f'land_status[{n}]'] = pt[type_]

    elif type_obj == 'commercial':
        params['offer_type'] = 'offices'
        if q['commercial_sort'] is not None:
            cs = {
                'office': '1',
                'free': '4',
                'shop-place': '2',
                'storage': '3',
                'fabric': '6',
                'food': '5',
                'hotel': 'has_hotel',
                'auto-s': '7',
                'build': '8'
            }
            for n, sort in enumerate(q['commercial_sort']):
                if sort != 'hotel':
                    params[f'object_type[{n}]'] = cs[sort]
                else:
                    params['has_hotel'] = '1'

        if q['commercial_type'] is not None:
            ct = {
                'government': '14',
                'business': '1',
                'mall': '2',
                'house': '27',
                'other': '5'
            }
            for n, sort in enumerate(q['commercial_type']):
                params[f'object_type[{n}]'] = ct[sort]

    # фильтр цены
    if q['price'] is not None:
        if q['price'][0] != '0':
            params['minprice'] = q['price'][0]
        if len(q['price']) > 1:
            params['maxprice'] = q['price'][1]

    # фильтр количества комнат
    if 'room_count' in q:
        if q['room_count'] is not None:
            for count in q['room_count']:
                if count in ['1', '2', '3', '4', '5>']:
                    if count != '5>':
                        params[f'room{count}'] = '1'
                    else:
                        params[f'room5'] = '1'
                        params[f'room6'] = '1'
                elif count == 'clear':
                    params[f'room7'] = '1'
                elif count == 'studio':
                    params[f'room9'] = '1'

    # фильтр площади
    if 'square' in q:
        if q['square'] is not None:
            params['minarea'] = q['square'][0]
            if len(q['square']) > 1:
                params['maxarea'] = q['square'][1]

    response = requests.get(f'https://{city['sub']}.cian.ru/cat.php',
                            params=params,  headers=headers, cookies=cookies)

    soup = BeautifulSoup(response.text, 'lxml')

    data = []
    items = soup.findAll('article', attrs={'data-name': 'CardComponent'})
    for item in items:
        title = item.find('div', attrs={'data-name': 'GeneralInfoSectionRowComponent'})
        url = title.find('a')['href']
        price = item.find('span', attrs={'data-mark': 'MainPrice'}).text
        description = item.find('div', attrs={'data-name': 'Description'}).text
        img_box = item.find('div', attrs={'data-name': 'Gallery'})
        imgs = img_box.findAll('img')
        pictures = []
        for img in imgs:
            pictures.append(img['src'])
        out = {'title': title.text, 'description': description, 'price': price,
               'url': url, 'img': pictures}
        data.append(out)
    return data

