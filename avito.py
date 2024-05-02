import re
import tls_client
import json

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def read_file(name: str):
    with open(name, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_avito_filter(location: str, type_obj: str, q: dict) -> str:
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        context = browser.new_context()

        page = context.new_page()
        page.goto(f"https://www.avito.ru/{location}/nedvizhimost")
        ts = {
            'room': 'Комната',
            'suburban': 'Дом, дача, коттедж',
            'garage': 'Гараж и машиноместо',
            'commercial': 'Коммерческая недвижимость',
            'plot': 'Земельный участок'
        }

        "выбор объекта"
        if type_obj != 'flat':
            page.locator("label").nth(2).click()
            page.wait_for_timeout(100)
            if type_obj == 'commercial':
                page.locator("div").filter(has_text=re.compile(rf'^{ts[type_obj]}$')).first.click()
            else:
                page.locator("div").filter(has_text=re.compile(rf'^{ts[type_obj]}$')).click()

        "купить - снять"
        if q['deal'] != 'buy':
            page.locator(
                "div:nth-child(2) > .search-form-widget-wrapper-Y5fVb >"
                " .desktop-1otmj24 > .input-layout-input-layout-_HVr_ >"
                " .input-layout-after-rIc8L > .desktop-1bacpxu").click()
            page.locator("div").filter(has_text=re.compile(r"^Снять$")).click()

        if type_obj == 'plot':
            if 'plot_type' in q:
                if q['plot_type'] is not None:
                    plot_t = {
                        'live': 'Поселений (ИЖС)',
                        'farm': 'Сельхозназначения (СНТ, ДНП)',
                        'fabric': 'Промназначения'
                    }
                    for sort in q['plot_type']:
                        page.get_by_role("listitem", name=plot_t[sort]).locator("label").click()

        f = 0
        if q['price'] is not None:
            page.get_by_text("Цена", exact=True).click()
            if 'period' in q:
                if q['period'] != 'days':
                    if q['price'][0] != '0':
                        page.get_by_placeholder("от").fill(q['price'][0])
                    if len(q['price']) > 1:
                        page.get_by_placeholder("до").fill(q['price'][1])
                else:
                    f += 1
                    if type_obj == 'flat':
                        page.get_by_role("button", name="Все фильтры").click()
                        if q['price'][0] != '0':
                            page.get_by_placeholder("от").first.fill(q['price'][0])
                        if len(q['price']) > 1:
                            page.get_by_placeholder("до").first.fill(q['price'][1])
                    else:
                        page.get_by_role("button", name="Все фильтры").click()
                        if q['price'][0] != '0':
                            page.get_by_placeholder("от").nth(1).fill(q['price'][0])
                        if len(q['price']) > 1:
                            page.get_by_placeholder("от").nth(1).fill(q['price'][1])
        if f == 0:
            page.get_by_role("button", name="Все фильтры").click()

        '''Квартира'''
        if type_obj == 'flat':
            '''Время постройки'''
            if q['cycle'] != 'all':
                if q['cycle'] == 'new':
                    page.locator("label").filter(has_text="Новостройка").click()
                elif q['cycle'] == 'used':
                    page.locator("label").filter(has_text="Вторичка").click()
            '''вид сделки'''
            if q['deal'] == 'buy':
                if q['square'] is not None:
                    if q['square'][0] != '0':
                        page.locator(
                            "div:nth-child(7) > .fieldset-fieldset-skPDA > div:nth-child(2) > "
                            ".fieldset-field-Fn_Rg > .row-root-t_KFV > .column-root-viFhL > div > "
                            ".styles-root-vSsLn > .group-root-DENYm > label > "
                            ".input-input-Zpzc1").first.fill(q['square'][0])

                    if len(q['square']) > 1:
                        page.locator(
                            "div:nth-child(7) > .fieldset-fieldset-skPDA > div:nth-child(2) > "
                            ".fieldset-field-Fn_Rg > .row-root-t_KFV > .column-root-viFhL > div > "
                            ".styles-root-vSsLn > .group-root-DENYm > label:nth-child(2) > "
                            ".input-input-Zpzc1").fill(q['square'][1])
            else:
                if q['square'] is not None:
                    if q['square'][0] != '0':
                        page.get_by_placeholder("от").nth(1).click()
                        page.get_by_placeholder("от").nth(1).fill(q['square'][0])
                    if len(q['square']) > 1:
                        page.get_by_placeholder("до").nth(1).click()
                        page.get_by_placeholder("до").nth(1).fill(q['square'][1])

        if 'period' in q:
            if q['period'] is not None:
                if q['period'] == 'days':
                    pr = {
                        'flat': '5257',
                        'room': '6204',
                        'suburban': '5477',
                        'commercial': ''
                    }
                    page.get_by_role("combobox").select_option(pr[type_obj])

        '''гараж'''
        if type_obj == 'garage':
            if 'type_garage' in q:
                if q['type_garage'] == 'garage':
                    page.get_by_text("Гараж").click()
                elif q['type_garage'] == 'car_place':
                    page.get_by_text("Машиноместо").click()
            if q['security']:
                sec = {
                    'buy': '10997',
                    'rent': '10998'
                }
                page.get_by_role("combobox").nth(1).select_option(sec[q['deal']])

        '''кол-во комнат'''
        if 'room_count' in q:
            if q['room_count'] is not None:
                if type_obj in ['flat', 'room', 'suburban']:
                    for check in q['room_count']:
                        room_c = {
                            '1': '1 комната',
                            '2': '2 комнаты',
                            '3': '3 комнаты',
                            '4': '4 комнаты',
                            '5>': '5 комнат и больше',
                            'studio': 'Студия',
                            'free': 'Свободная планировка',
                        }
                        page.get_by_text(room_c[check], exact=True).click()

        '''коммерческая'''
        if type_obj == 'commercial':
            if q['commercial_sort'] is not None:
                cs = {
                    'office': 'Офис',
                    'free': 'Свободного назначения',
                    'shop-place': 'Торговая площадь',
                    'storage': 'Склад',
                    'fabric': 'Производство',
                    'food': 'Общепит',
                    'hotel': 'Гостиница',
                    'auto-s': 'Автосервис',
                    'build': 'Здание целиком',
                    'kwork': 'Коворкинг',
                }
                for check in q['commercial_sort']:
                    page.get_by_text(cs[check], exact=True).click()
            if q['commercial_type'] is not None:
                ct = {
                    'business': 'Бизнес-центр',
                    'house': 'Жилой дом',
                    'mall': 'Торговый центр',
                    'government': 'Администрат. здание',
                    'other': 'Другой'
                }
                for check in q['commercial_type']:
                    page.get_by_text(ct[check], exact=True).click()

        page.wait_for_selector('.desktop-8ji0mf')
        page.query_selector('.desktop-8ji0mf').click()
        url = page.url
        print(url)
        # ---------------------
        context.close()
        browser.close()

        return url


def get_avito_page(location: str, refer: str, page: str = '1'):

    session = tls_client.Session(
        client_identifier="chrome_122",
        random_tls_extension_order=True
    )

    cookies = read_file('cookies_avito.json')
    cookies['luri'] = location

    headers = {
        'authority': 'www.avito.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
                  'avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'referer': f'https://www.avito.ru/{location}/nedvizhimost',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
    }

    params = {
        'page': page,
        'context': refer.split('?context=')[1]
    }

    response = session.get(
        refer.split('?context=')[0],
        params=params,
        cookies=cookies,
        headers=headers,
    )

    soup = BeautifulSoup(response.text, 'lxml')

    box = soup.find('div', attrs={'data-marker': 'catalog-serp'})

    items = box.findAll('div', attrs={'data-marker': 'item'})
    data = []

    for item in items:
        title_div = item.find('div', class_='iva-item-title-py3i_')
        if title_div is not None:
            description = item.find('meta', attrs={'itemprop': 'description'})
            if description is not None:
                price = item.find('strong', class_='styles-module-root-bLKnd').text
                title = title_div.find('a', attrs={'data-marker': 'item-title'})
                if title is not None:
                    pictures = item.findAll('img')
                    print(pictures)
                    for n, img in enumerate(pictures):
                        if img is not None:
                            pictures[n] = img['src']
                    out = {
                        'title': title['title'],
                        'description': description['content'],
                        'price': price,
                        'url': 'https://www.avito.ru' + title['href'],
                        'img': pictures
                    }
                    data.append(out)

    return data
