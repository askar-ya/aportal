def deal_verify(value):
    """Функции для проверки валидности типа сделки"""
    if value not in ['buy', 'rent']:
        raise ValueError('invalid value in deal')


def period_verify(value, deal):
    """Функции для проверки валидности срока аренды"""
    if value is not None:
        if value not in ['days', 'lengthy']:
            raise ValueError('invalid value in period')
        elif deal == 'buy':
            raise ValueError('buy > plat does not have a field period')


def cycle_verify(value, deal):
    """Функции для проверки валидности типа(вторичка | новостройка) квартиры"""
    if value not in ['new', 'used', 'all']:
        raise ValueError('invalid value in cycle')
    elif (deal == 'rent') and (value != 'all'):
        raise ValueError('rent > plat does not have a field cycle')


def room_count_verify(value):
    """Функции для проверки валидности выборки по кол-ву комнат"""
    if value is not None:
        value = set(value)
        for checker in value:
            if checker not in ['1', '2', '3', '4', '5>', 'studio', 'clear']:
                raise ValueError('invalid value in room_count')


def square_verify(value):
    """Функции для проверки валидности фильтра площади"""
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


def price_verify(value):
    """Функции для проверки валидности фильтра цены"""
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


def type_garage_verify(value):
    """Функции для проверки валидности типа гаража"""
    if value is not None:
        if value not in ['car_place', 'garage']:
            raise ValueError('invalid value in garage_type')
