import requests


r = requests.get('http://176.9.3.252/cian',
                 json={
                     "type": "flat",
                     "deal": "buy",
                     "cycle": "used",
                     "location": "Москва"})

print(r.text)
