from flask import Flask, request
from models import Flat, Room, Suburban, Garage, Commercial, Plot
from avito import get_avito_filter, get_avito_page
from yandex import get_yandex_page
from cian import get_cian_page


app = Flask(__name__)


def request_handler(parameters: dict):
    if 'type' not in parameters:
        return 'the object type is not specified'
    elif parameters['type'] not in ['flat', 'room', 'garage', 'suburban', 'commercial', 'plot']:
        return 'the object type is not specified correctly'
    elif parameters['type'] == 'flat':
        r_object = Flat()
    elif parameters['type'] == 'room':
        r_object = Room()
    elif parameters['type'] == 'garage':
        r_object = Garage()
    elif parameters['type'] == 'suburban':
        r_object = Suburban()
    elif parameters['type'] == 'commercial':
        r_object = Commercial()
    else:
        r_object = Plot()

    try:
        if 'deal' in parameters:
            r_object.deal = parameters['deal']
        if 'period' in parameters:
            r_object.period = parameters['period']
        if 'cycle' in parameters:
            r_object.cycle = parameters['cycle']
        if 'room_count' in parameters:
            r_object.room_count = parameters['room_count']
        if 'square' in parameters:
            r_object.square = parameters['square']
        if 'price' in parameters:
            r_object.price = parameters['price']
        if 'type_garage' in parameters:
            r_object.type_garage = parameters['type_garage']
        if 'security' in parameters:
            r_object.security = parameters['security']
        if 'commercial_sort' in parameters:
            r_object.commercial_sort = parameters['commercial_sort']
        if 'commercial_type' in parameters:
            r_object.commercial_type = parameters['commercial_type']
        if 'plot_type' in parameters:
            r_object.plot_type = parameters['plot_type']
        return r_object
    except Exception as e:
        return str(e)


@app.route('/avito')
def avito():
    r = request.json
    if 'location' in r:
        location = r['location']
    else:
        location = 'all'
    search_object = request_handler(r)
    if type(search_object) is not str:
        q = search_object.to_form()
        filter_ = get_avito_filter(location, q['object_type'], q)
        data = get_avito_page(location, filter_)
        return data
    else:
        return search_object


@app.route('/yandex')
def yandex():
    r = request.json
    if 'location' in r:
        location = r['location']
    else:
        location = 'all'
    search_object = request_handler(r)
    if type(search_object) is not str:
        q = search_object.to_form()
        data = get_yandex_page(location, q['object_type'], q)
        return data
    else:
        return search_object


@app.route('/cian')
def cian():
    r = request.json
    if 'location' in r:
        location = r['location']
    else:
        location = 'all'
    search_object = request_handler(r)
    if type(search_object) is not str:
        q = search_object.to_form()
        data = get_cian_page(location, q['object_type'], q)
        return data
    else:
        return search_object


if __name__ == '__main__':
    app.run(debug=True)
