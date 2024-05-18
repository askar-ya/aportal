for deal in ['buy', 'rent']:
    q = {'deal': deal}
    for type_ in ['flat', 'room', 'suburban', 'garage', 'commercial', 'plot']:
        q['type'] = type_
        for price in [['0', '4500000'], ['1000000'], [0]]:
            if price[0] != 0:
                q['price'] = price
            for square in [['35'], ['30', '65'], [0]]:
                if square[0] != 0:
                    q['square'] = square
                    print(q)