from avito import get_avito_filter, get_avito_page
from yandex import get_yandex_page


class Flat:
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

    def pars_avito(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'period': self.period,
            'cycle': self.cycle,
            'room_count': self.room_count,
            'square': self.square,
            'price': self.price},
            type_obj='flat')

        data = get_avito_page(location, refer, '1')
        return data

    def pars_yandex(self, location) -> list:
        data = get_yandex_page(location=location, type_obj='flat',
                               q={
                                   'deal': self.deal,
                                   'period': self.period,
                                   'cycle': self.cycle,
                                   'room_count': self.room_count,
                                   'square': self.square,
                                   'price': self.price
                               })
        return data


class Garage:
    """Класс гараж.

        Аттрибуты:
            deal - тип сделки, может быть 'buy' или 'rent'
                   по умолчанию 'buy'
            period - период аренды, может быть 'days' или 'lengthy'
                     Не может быть задан, если тип сделки 'buy'
                     по умолчанию None
            price - цена, должна быть list и длиной 1 или 2
                     элементы должны быть str и содержать только цифры
                     первый элемент минимальная цена, вторая максимальная
                     по умолчанию None
            type_garage -
        """
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

    def pars_avito(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'type_garage': self.type_garage,
            'security': self.security,
            'price': self.price},
            type_obj='garage')

        data = get_avito_page(location, refer, '2')
        return data


class Room:
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

    def pars_avito(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'period': self.period,
            'room_count': self.room_count,
            'square': self.square,
            'price': self.price},
            type_obj='room')

        data = get_avito_page(location, refer, '2')
        return data


class Plot:
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

    def pars_avito(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'price': self.price,
            'plot_type': self.plot_type},
            type_obj='plot')

        data = get_avito_page(location, refer, '2')
        return data


class Suburban:
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

    def pars_avito(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'period': self.period,
            'room_count': self.room_count,
            'square': self.square,
            'price': self.price},
            type_obj='suburban')

        data = get_avito_page(location, refer, '2')
        return data


class Commercial:
    def __init__(self, deal: str = 'buy', square: list = None, commercial_sort: list = None,
                 commercial_type: list = None, price: list = None):
        self.deal = deal
        self.square = square
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

    def pars_avito(self, location):
        refer = get_avito_filter(location=location, q={
            'deal': self.deal,
            'price': self.price,
            'commercial_sort': self.commercial_sort,
            'commercial_type': self.commercial_type},
            type_obj='commercial')

        data = get_avito_page(location, refer, '2')
        return data
