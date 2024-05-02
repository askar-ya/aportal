from models import Flat, Room, Suburban, Garage, Commercial, Plot

from flask import Flask, request

app = Flask(__name__)


@app.route('/avito')
def avito():
    r = request.form
    deal = 'buy'
    period = None
    cycle = 'all'
    room_count = None
    square = None
    price = None
    type_garage = None
    security = False
    commercial_sort = None
    commercial_type = None
    plot_type = None
    location = 'all'
    if 'deal' in r:
        deal = r['deal']
    if 'deal' in r:
        deal = r['deal']
    if 'period' in r:
        period = r['period']
    if 'cycle' in r:
        cycle = r['cycle']
    if 'room_count' in r:
        room_count = r['room_count']
    if 'square' in r:
        square = r['square']
    if 'price' in r:
        price = r['price']
    if 'type_garage' in r:
        type_garage = r['type_garage']
    if 'security' in r:
        security = r['security']
    if 'commercial_sort' in r:
        commercial_sort = r['commercial_sort']
    if 'commercial_type' in r:
        commercial_type = r['commercial_type']
    if 'plot_type' in r:
        plot_type = r['plot_type']

    try:
        if r['type'] == 'flat':
            plat = Flat(deal, period, cycle, room_count, square,
                        price)
            return plat.pars_avito(location=location)
        elif r['type'] == 'room':
            room = Room(deal, period, room_count, square, price)
            return room.pars_avito(location=location)
        elif r['type'] == 'garage':
            garage = Garage(deal, type_garage, security, price)
            return garage.pars_avito(location=location)
        elif r['type'] == 'suburban':
            suburban = Suburban(deal, period, room_count, square, price)
            return suburban.pars_avito(location=location)
        elif r['type'] == 'commercial':
            commercial = Commercial(deal, commercial_sort, commercial_type, price)
            return commercial.pars_avito(location=location)
        elif r['type'] == 'plot':
            plot = Plot(deal, plot_type, price)
            return plot.pars_avito(location=location)

    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
