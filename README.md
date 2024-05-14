# API
___
## Описание типов

| Parameter       | Type | Required | Description                                                                                                                                                                            |
|-----------------|------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| type            | str  | Yes      | Тип недвижимости может принимать следующие значения 'flat', 'room', 'suburban', 'garage', 'commercial', 'plot'                                                                         |
| location        | str  | Optional | город для запроса, по умолчанию 'all'                                                                                                                                                  |
| deal            | str  | Optional | Тип сделки (купить\снять) по умолчанию 'buy'                                                                                                                                           |
| period          | str  | Optional | период аренды, может быть 'days' или 'lengthy' Не может быть задан, если тип сделки 'buy'по умолчанию None                                                                             |
| cycle           | str  | Optional | время постройки, может быть 'new', 'used' или 'all' Не может быть задан, если тип сделки 'rent' по умолчанию 'all'                                                                     |
| room_count      | list | Optional | кол-во комнат, должны быть list элементы могут быть равны - '1', '2', '3', '4', '5>', 'studio', 'clear' по умолчанию None ('studio', 'clear' не может быть задан для комнаты в аренду) |
| square          | list | Optional | площадь квартиры, должна быть list и длиной 1 или 2 элементы должны быть str и содержать только цифры первый элемент минимальная площадь, второй максимальная по умолчанию None        |
| price           | list | Optional | цена квартиры, должна быть list и длиной 1 или 2 элементы должны быть str и содержать только цифры первый элемент минимальная цена, вторая максимальная по умолчанию None              |
| security        | bool | Optional | Наличие охраны гаража - True, False                                                                                                                                                    |
| type_garage     | list | Optional | Тип гаража, должен быть list длиной 1 или 2 элементы должны быть str и равны 'car_place', 'garage'                                                                                     |
| plot_type       | list | Optional | Тип земли, должен быть list длиной до трех со значениями 'live', 'farm', 'fabric'                                                                                                      |
| commercial_sort | list | Optional | Вид недвижимости, может содержать следующие значения 'office', 'free', 'shop-place', 'storage', 'fabric', 'food', 'hotel', 'auto-s', 'build'                                           |
| commercial_type | list | Optional | Тип здания, может содержать следующие значения 'business', 'house', 'mall', 'government', 'other'                                                                                      |

## Структура классов

+ Квартира
  <br> type должен быть - 'flat'
  <br>может содержать следующие параметры 
  <br> deal, period, cycle, room_count, square, price
  <br> пример запроса на python
  <br> Квартиры в аренду с 1ой и 2мя комнатами, площадью от 25 кв.м. и ценой до 35000р. в г. Уфа
  ```
  import requests 
  r = requests.get('http://176.9.3.252/avito',
                   data={
                       'type': 'flat',
                       'deal': 'rent',
                       'room_count': ['1', '2'],
                       'square': ['25'],
                       'price': ['0', '35000'],
                       'location': 'ufa'})
  ```
+ Комната
  <br> type должен быть - 'room'
  <br>может содержать следующие параметры 
  <br> deal, period room_count, square, price
  <br> пример запроса на python
  <br> Купить комнату, в 2ой квартире, площадью от 25 кв.м. и ценой от 4500р. до 5000р. в г. Москва
  ```
  import requests 
  r = requests.get('http://176.9.3.252/avito',
                   data={
                       'type': 'room',
                       'deal': 'buy',
                       'room_count': ['2'],
                       'square': ['25'],
                       'price': ['4500', '5000'],
                       'location': 'moskva'})
  ```
+ Дом
  <br> type должен быть - 'suburban'
  <br>может содержать следующие параметры 
  <br> deal, period room_count, square, price
  <br> пример запроса на python
  <br> Купить дом, площадью от 250 кв.м. в г. Москва
  ```
  import requests 
  r = requests.get('http://176.9.3.252/avito',
                   data={
                       'type': 'suburban',
                       'deal': 'buy',
                       'square': ['250'],
                       'location': 'moskva'})
  ```
+ Гараж
  <br> type должен быть - 'garage'
  <br>может содержать следующие параметры 
  <br> deal, type_garage, security, price
  <br> пример запроса на python
  <br> Снять место для машины, с охранной в г. Уфа
  ```
  import requests 
  r = requests.get('http://176.9.3.252/avito',
                   data={
                       'type': 'garage',
                       'deal': 'rent',
                       'type_garage': 'car_place',
                       'security': True,
                       'location': 'ufa'})
  ```
+ Земля
  <br> type должен быть - 'plot'
  <br>может содержать следующие параметры 
  <br> deal, plot_type, price
  <br> пример запроса на python
  <br> Купить землю в пром. зоне в г. Уфа
  ```
  import requests 
  r = requests.get('http://176.9.3.252/avito',
                   data={
                       'type': 'plot',
                       'deal': 'buy',
                       'plot_type': 'fabric',
                       'location': 'ufa'})
  ```

  + Коммерческая
    <br> type должен быть - 'commercial'
    <br>может содержать следующие параметры 
    <br> deal, square, commercial_sort, commercial_type, price
    <br> пример запроса на python
    <br> Снять помещение для офиса, в доме или т.ц. от 100 кв.м. в г. Москва
    ```
    import requests 
    r = requests.get('http://176.9.3.252/avito',
                     data={
                         'type': 'commercial',
                         'deal': 'rent',
                         'commercial_sort': ['office'],
                         'commercial_type': ['mall', 'house'],
                         'square': ['100'],
                         'location': 'ufa'})
    ```