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
        browser = playwright.firefox.launch(headless=False)
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
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

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


class FlatAvito:
    """Класс квартиры авито.

    Аттрибуты:
        deal - тип сделки, может быть 'buy' или 'rent'
               по умолчанию 'buy'
        period - период аренды, может быть 'days' или 'lengthy'
                 Не может быть задан, если тип сделки 'buy'
                 по умолчанию None
        cycle - время постройки, может быть 'new', 'used' или 'all'
                Не может быть задан, если тип сделки 'rent'
                по умолчанию 'all'
        room_count - кол-во комнат, должны быть list
                     элементы могут быть равны - '1', '2', '3', '4', '5>', 'studio', 'clear'
                     по умолчанию None
        square - площадь квартиры, должна быть list и длиной 1 или 2
                 элементы должны быть str и содержать только цифры
                 первый элемент минимальная площадь, второй максимальная
                 по умолчанию None
        price - цена квартиры, должна быть list и длиной 1 или 2
                 элементы должны быть str и содержать только цифры
                 первый элемент минимальная цена, вторая максимальная
                 по умолчанию None
    """

    def __init__(self, deal: str = 'buy', period: str = None, cycle: str = 'all',
                 room_count: list = None, square: list = None, price: list = None):

        self.deal = deal
        self.period = period
        self.cycle = cycle
        self.room_count = room_count
        self.square = square
        self.price = price

    @property
    def deal(self):
        return self._deal

    @deal.setter
    def deal(self, value):
        if value not in ['buy', 'rent']:
            raise ValueError('invalid value in deal')
        self._deal = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        if value is not None:
            if value not in ['days', 'lengthy']:
                raise ValueError('invalid value in period')
            elif self.deal == 'buy':
                raise ValueError('buy > plat does not have a field period')
        self._period = value

    @property
    def cycle(self):
        return self._cycle

    @cycle.setter
    def cycle(self, value):
        if value not in ['new', 'used', 'all']:
            raise ValueError('invalid value in cycle')
        elif (self.deal == 'rent') and (value != 'all'):
            raise ValueError('rent > plat does not have a field cycle')
        self._cycle = value

    @property
    def room_count(self):
        return self._room_count

    @room_count.setter
    def room_count(self, value):
        if value is not None:
            value = set(value)
            for checker in value:
                if checker not in ['1', '2', '3', '4', '5>', 'studio', 'clear']:
                    raise ValueError('invalid value in room_count')
        self._room_count = value

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        if value is not None:
            square = value
            if (len(square) > 0) and (len(square) <= 2):
                first_m = square[0]
                try:
                    first_m = int(first_m)
                    if first_m < 0:
                        raise ValueError('the square element cannot be negative')
                except ValueError:
                    raise ValueError('the square element must include a number in string')

                if len(square) > 1:
                    second_m = square[1]
                    try:
                        second_m = int(second_m)
                        if second_m < 0:
                            raise ValueError('the square element cannot be negative')
                        elif second_m < first_m:
                            raise ValueError('second square element cannot be less than first_m')
                    except ValueError:
                        raise ValueError('the square element must include a number in string')

            else:
                raise ValueError('the list square cannot be longer than 2 and not less than 1')
        self._square = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is not None:
            price = value
            if (len(price) > 0) and (len(price) <= 2):
                first_m = price[0]
                try:
                    first_m = int(first_m)
                    if first_m < 0:
                        raise ValueError('the price element cannot be negative')
                except ValueError:
                    raise ValueError('the square element must include a number in string')

                if len(price) > 1:
                    second_m = price[1]
                    try:
                        second_m = int(second_m)
                        if second_m < 0:
                            raise ValueError('the price element cannot be negative')
                        elif second_m < first_m:
                            raise ValueError('second price element cannot be less than first_m')
                    except ValueError:
                        raise ValueError('the price element must include a number in string')
            else:
                raise ValueError('the list price cannot be longer than 2 and not less than 1')
        self._price = value

    def pars(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'period': self.period,
            'cycle': self.cycle,
            'room_count': self.room_count,
            'square': self.square,
            'price': self.price},
            type_obj='flat')

        data = get_avito_page(location, refer, '2')
        return data


class GarageAvito:
    def __init__(self, deal: str = 'buy', type_garage: list = None,
                 security: bool = False, price: list = None):
        self.deal = deal
        self.type_garage = type_garage
        self.security = security
        self.price = price

    @property
    def deal(self):
        return self._deal

    @deal.setter
    def deal(self, value):
        if value not in ['buy', 'rent']:
            raise ValueError('invalid value in deal')
        self._deal = value

    @property
    def type_garage(self):
        return self._type_garage

    @type_garage.setter
    def type_garage(self, value):
        if value is not None:
            if value not in ['car_place', 'garage']:
                raise ValueError('invalid value in garage_type')
        self._type_garage = value

    @property
    def security(self):
        return self._security

    @security.setter
    def security(self, value):
        if value not in [True, False]:
            raise ValueError('invalid value in security')
        self._security = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is not None:
            price = value
            if (len(price) > 0) and (len(price) <= 2):
                first_m = price[0]
                try:
                    first_m = int(first_m)
                    if first_m < 0:
                        raise ValueError('the price element cannot be negative')
                except ValueError:
                    raise ValueError('the square element must include a number in string')

                if len(price) > 1:
                    second_m = price[1]
                    try:
                        second_m = int(second_m)
                        if second_m < 0:
                            raise ValueError('the price element cannot be negative')
                        elif second_m < first_m:
                            raise ValueError('second price element cannot be less than first_m')
                    except ValueError:
                        raise ValueError('the price element must include a number in string')
            else:
                raise ValueError('the list price cannot be longer than 2 and not less than 1')
        self._price = value

    def pars(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'type_garage': self.type_garage,
            'security': self.security,
            'price': self.price},
            type_obj='garage')

        data = get_avito_page(location, refer, '2')
        return data


class RoomAvito:
    def __init__(self, deal: str = 'buy', period: str = None,
                 room_count: list = None, square: list = None, price: list = None):

        self.deal = deal
        self.period = period
        self.room_count = room_count
        self.square = square
        self.price = price

    @property
    def deal(self):
        return self._deal

    @deal.setter
    def deal(self, value):
        if value not in ['buy', 'rent']:
            raise ValueError('invalid value in deal')
        self._deal = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        if value is not None:
            if value not in ['days', 'lengthy']:
                raise ValueError('invalid value in period')
            elif self.deal == 'buy':
                raise ValueError('buy > plat does not have a field period')
        self._period = value

    @property
    def room_count(self):
        return self._room_count

    @room_count.setter
    def room_count(self, value):
        if value is not None:
            value = set(value)
            for checker in value:
                if checker not in ['1', '2', '3', '4', '5>', 'clear']:
                    raise ValueError('invalid value in room_count')
        self._room_count = value

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        if value is not None:
            square = value
            if (len(square) > 0) and (len(square) <= 2):
                first_m = square[0]
                try:
                    first_m = int(first_m)
                    if first_m < 0:
                        raise ValueError('the square element cannot be negative')
                except ValueError:
                    raise ValueError('the square element must include a number in string')

                if len(square) > 1:
                    second_m = square[1]
                    try:
                        second_m = int(second_m)
                        if second_m < 0:
                            raise ValueError('the square element cannot be negative')
                        elif second_m < first_m:
                            raise ValueError('second square element cannot be less than first_m')
                    except ValueError:
                        raise ValueError('the square element must include a number in string')

            else:
                raise ValueError('the list square cannot be longer than 2 and not less than 1')
        self._square = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is not None:
            price = value
            if (len(price) > 0) and (len(price) <= 2):
                first_m = price[0]
                try:
                    first_m = int(first_m)
                    if first_m < 0:
                        raise ValueError('the price element cannot be negative')
                except ValueError:
                    raise ValueError('the square element must include a number in string')

                if len(price) > 1:
                    second_m = price[1]
                    try:
                        second_m = int(second_m)
                        if second_m < 0:
                            raise ValueError('the price element cannot be negative')
                        elif second_m < first_m:
                            raise ValueError('second price element cannot be less than first_m')
                    except ValueError:
                        raise ValueError('the price element must include a number in string')
            else:
                raise ValueError('the list price cannot be longer than 2 and not less than 1')
        self._price = value

    def pars(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'period': self.period,
            'room_count': self.room_count,
            'square': self.square,
            'price': self.price},
            type_obj='room')

        data = get_avito_page(location, refer, '2')
        return data


class PlotAvito:
    def __init__(self, deal: str = 'buy', plot_type: list = None, price: list = None):
        self.deal = deal
        self.plot_type = plot_type
        self.price = price

    @property
    def deal(self):
        return self._deal

    @deal.setter
    def deal(self, value):
        if value not in ['buy', 'rent']:
            raise ValueError('invalid value in deal')
        self._deal = value

    @property
    def plot_type(self):
        return self._plot_type

    @plot_type.setter
    def plot_type(self, value):
        if value is not None:
            if value not in ['live', 'farm', 'fabric']:
                raise ValueError('invalid value in plot_type')
        self._plot_type = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is not None:
            price = value
            if (len(price) > 0) and (len(price) <= 2):
                first_m = price[0]
                try:
                    first_m = int(first_m)
                    if first_m < 0:
                        raise ValueError('the price element cannot be negative')
                except ValueError:
                    raise ValueError('the square element must include a number in string')

                if len(price) > 1:
                    second_m = price[1]
                    try:
                        second_m = int(second_m)
                        if second_m < 0:
                            raise ValueError('the price element cannot be negative')
                        elif second_m < first_m:
                            raise ValueError('second price element cannot be less than first_m')
                    except ValueError:
                        raise ValueError('the price element must include a number in string')
            else:
                raise ValueError('the list price cannot be longer than 2 and not less than 1')
        self._price = value

    def pars(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'price': self.price,
            'plot_type': self.plot_type},
            type_obj='plot')

        data = get_avito_page(location, refer, '2')
        return data


class SuburbanAvito:
    def __init__(self, deal: str = 'buy', period: str = None,
                 room_count: list = None, square: list = None, price: list = None):

        self.deal = deal
        self.period = period
        self.room_count = room_count
        self.square = square
        self.price = price

    @property
    def deal(self):
        return self._deal

    @deal.setter
    def deal(self, value):
        if value not in ['buy', 'rent']:
            raise ValueError('invalid value in deal')
        self._deal = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        if value is not None:
            if value not in ['days', 'lengthy']:
                raise ValueError('invalid value in period')
            elif self.deal == 'buy':
                raise ValueError('buy > plat does not have a field period')
        self._period = value

    @property
    def room_count(self):
        return self._room_count

    @room_count.setter
    def room_count(self, value):
        if value is not None:
            value = set(value)
            for checker in value:
                if checker not in ['1', '2', '3', '4', '5>', 'clear']:
                    raise ValueError('invalid value in room_count')
        self._room_count = value

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        if value is not None:
            square = value
            if (len(square) > 0) and (len(square) <= 2):
                first_m = square[0]
                try:
                    first_m = int(first_m)
                    if first_m < 0:
                        raise ValueError('the square element cannot be negative')
                except ValueError:
                    raise ValueError('the square element must include a number in string')

                if len(square) > 1:
                    second_m = square[1]
                    try:
                        second_m = int(second_m)
                        if second_m < 0:
                            raise ValueError('the square element cannot be negative')
                        elif second_m < first_m:
                            raise ValueError('second square element cannot be less than first_m')
                    except ValueError:
                        raise ValueError('the square element must include a number in string')

            else:
                raise ValueError('the list square cannot be longer than 2 and not less than 1')
        self._square = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is not None:
            price = value
            if (len(price) > 0) and (len(price) <= 2):
                first_m = price[0]
                try:
                    first_m = int(first_m)
                    if first_m < 0:
                        raise ValueError('the price element cannot be negative')
                except ValueError:
                    raise ValueError('the square element must include a number in string')

                if len(price) > 1:
                    second_m = price[1]
                    try:
                        second_m = int(second_m)
                        if second_m < 0:
                            raise ValueError('the price element cannot be negative')
                        elif second_m < first_m:
                            raise ValueError('second price element cannot be less than first_m')
                    except ValueError:
                        raise ValueError('the price element must include a number in string')
            else:
                raise ValueError('the list price cannot be longer than 2 and not less than 1')
        self._price = value

    def pars(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'period': self.period,
            'room_count': self.room_count,
            'square': self.square,
            'price': self.price},
            type_obj='suburban')

        data = get_avito_page(location, refer, '2')
        return data


class CommercialAvito:
    def __init__(self, deal: str = 'buy', commercial_sort: list = None,
                 commercial_type: list = None, price: list = None):
        self.deal = deal
        self.commercial_sort = commercial_sort
        self.commercial_type = commercial_type
        self.price = price

    @property
    def deal(self):
        return self._deal

    @deal.setter
    def deal(self, value):
        if value not in ['buy', 'rent']:
            raise ValueError('invalid value in deal')
        self._deal = value

    @property
    def commercial_sort(self):
        return self._commercial_sort

    @commercial_sort.setter
    def commercial_sort(self, value):
        if value is not None:
            for check in value:
                if check not in ['office', 'free', 'shop-place', 'storage', 'fabric',
                                 'food', 'hotel', 'auto-s', 'build', 'kwork']:
                    raise ValueError('invalid value in commercial_sort')
        self._commercial_sort = value

    @property
    def commercial_type(self):
        return self._commercial_type

    @commercial_type.setter
    def commercial_type(self, value):
        if value is not None:
            for check in value:
                if check not in ['business', 'house', 'mall', 'government', 'other']:
                    raise ValueError('invalid value in commercial_type')
        self._commercial_type = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is not None:
            price = value
            if (len(price) > 0) and (len(price) <= 2):
                first_m = price[0]
                try:
                    first_m = int(first_m)
                    if first_m < 0:
                        raise ValueError('the price element cannot be negative')
                except ValueError:
                    raise ValueError('the square element must include a number in string')

                if len(price) > 1:
                    second_m = price[1]
                    try:
                        second_m = int(second_m)
                        if second_m < 0:
                            raise ValueError('the price element cannot be negative')
                        elif second_m < first_m:
                            raise ValueError('second price element cannot be less than first_m')
                    except ValueError:
                        raise ValueError('the price element must include a number in string')
            else:
                raise ValueError('the list price cannot be longer than 2 and not less than 1')
        self._price = value

    def pars(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'price': self.price,
            'commercial_sort': self.commercial_sort,
            'commercial_type': self.commercial_type},
            type_obj='commercial')

        data = get_avito_page(location, refer, '2')
        return data
