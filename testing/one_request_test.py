import requests


r = requests.get('http://yap-place.ru/cian',
                 json={
                     "type": "flat",
                     "deal": "buy",
                     "cycle": "used",
                     "location": "Москва"})

print(r.text)
