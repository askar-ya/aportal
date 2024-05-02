from avito_class import FlatAvito

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

    if r['type'] == 'flat':
        try:
            plat = FlatAvito(deal, period, cycle, room_count, square,
                             price)
            return plat.pars(location=location)
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    app.run(debug=True)
