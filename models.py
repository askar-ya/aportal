from verify_parms import (deal_verify, period_verify, cycle_verify,
                          square_verify, room_count_verify, price_verify, type_garage_verify)


class Flat:
    """Класс квартиры.

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
        deal_verify(value)
        self._deal = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        period_verify(value, self.deal)
        self._period = value

    @property
    def cycle(self):
        return self._cycle

    @cycle.setter
    def cycle(self, value):
        cycle_verify(value, self.deal)
        self._cycle = value

    @property
    def room_count(self):
        return self._room_count

    @room_count.setter
    def room_count(self, value):
        room_count_verify(value)
        self._room_count = value

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        square_verify(value)
        self._square = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        price_verify(value)
        self._price = value

    def to_form(self):
        q = {
            'deal': self.deal,
            'period': self.period,
            'cycle': self.cycle,
            'room_count': self.room_count,
            'square': self.square,
            'price': self.price,
            'object_type': 'flat'
        }
        return q


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
        deal_verify(value)
        self._deal = value

    @property
    def type_garage(self):
        return self._type_garage

    @type_garage.setter
    def type_garage(self, value):
        type_garage_verify(value)
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
        price_verify(value)
        self._price = value

    def to_form(self):
        q = {
            'deal': self.deal,
            'type_garage': self.type_garage,
            'security': self.security,
            'price': self.price,
            'object_type': 'garage'
        }
        return q


class Room:
    """Класс комнаты.

        Аттрибуты:
            deal - тип сделки, может быть 'buy' или 'rent'
                   по умолчанию 'buy'
            period - период аренды, может быть 'days' или 'lengthy'
                     Не может быть задан, если тип сделки 'buy'
                     по умолчанию None
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
        deal_verify(value)
        self._deal = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        period_verify(value, self.deal)
        self._period = value

    @property
    def room_count(self):
        return self._room_count

    @room_count.setter
    def room_count(self, value):
        room_count_verify(value)
        self._room_count = value

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        square_verify(value)
        self._square = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        price_verify(value)
        self._price = value

    def to_form(self):
        q = {
            'deal': self.deal,
            'period': self.period,
            'room_count': self.room_count,
            'square': self.square,
            'price': self.price,
            'object_type': 'room'}
        return q


class Plot:
    def __init__(self, deal: str = 'buy', plot_type: list = None, square: list = None, price: list = None):

        self.deal = deal
        self.plot_type = plot_type
        self.square = square
        self.price = price

    @property
    def deal(self):
        return self._deal

    @deal.setter
    def deal(self, value):
        deal_verify(value)
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
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        square_verify(value)
        self._square = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        price_verify(value)
        self._price = value

    def to_form(self):
        q = {
            'deal': self.deal,
            'price': self.price,
            'plot_type': self.plot_type,
            'object_type': 'plot'
        }
        return q


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
        deal_verify(value)
        self._deal = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        period_verify(value, self.deal)
        self._period = value

    @property
    def room_count(self):
        return self._room_count

    @room_count.setter
    def room_count(self, value):
        room_count_verify(value)
        self._room_count = value

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        square_verify(value)
        self._square = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        price_verify(value)
        self._price = value

    def to_from(self):
        q = {
            'deal': self.deal,
            'period': self.period,
            'room_count': self.room_count,
            'square': self.square,
            'price': self.price,
            'object_type': 'suburban'
        }
        return q


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
        deal_verify(value)
        self._deal = value

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        square_verify(value)
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
        price_verify(value)
        self._price = value

    def to_form(self):
        q = {
            'deal': self.deal,
            'price': self.price,
            'commercial_sort': self.commercial_sort,
            'commercial_type': self.commercial_type,
            'object_type': 'commercial'}
        return q
