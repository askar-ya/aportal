import json
import os
from playwright.sync_api import sync_playwright

with open('proxy.json', 'r', encoding='utf-8') as file_proxy:
    proxy_list = json.load(file_proxy)


def wright_cookies(raw_cookies: list, proxy_index: int, service: str) -> None:
    data = {}
    for cooke in raw_cookies:
        data[cooke['name']] = cooke['value']
    if os.path.exists(f'cookies/{service}') is False:
        os.mkdir(f'cookies/{service}')
    with open(f'cookies/{service}/{proxy_index}.json', 'w', encoding='utf-8') as file_cookies:
        json.dump(data, file_cookies)


with sync_playwright() as playwright:
    for proxy_id, proxy in enumerate(proxy_list['ips'][:3]):
        print(proxy_id)
        browser = playwright.chromium.launch(headless=False,
                                             proxy={
                                                 "server": proxy,
                                                 "username": proxy_list['username'],
                                                 "password": proxy_list['password']
                                             })
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://realty.ya.ru")

        page.wait_for_timeout(15000)
        wright_cookies(context.cookies(), proxy_id, 'yandex')
        page.goto("https://avito.ru/")
        page.wait_for_timeout(2000)
        wright_cookies(context.cookies(), proxy_id, 'yandex')
        page.goto("https://www.cian.ru")
        page.wait_for_timeout(2000)
        wright_cookies(context.cookies(), proxy_id, 'yandex')

    # ---------------------
    context.close()
    browser.close()
