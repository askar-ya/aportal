import requests
from bs4 import BeautifulSoup


def yandex_page(location: str, type_obj: str, q: dict):
    cookies = {
        'ys': 'newsca.native_cache#svt.1#def_bro.1#ead.2FECB7CF',
        'yandexuid': '7761032951644804503',
        'my': 'YwA=',
        'gdpr': '0',
        '_ym_uid': '1663058936243782939',
        'yashr': '2066826271700949369',
        'yandex_gid': '2',
        'yuidss': '7761032951644804503',
        'L': 'AQBCe2dSCg9tWFgGSE9VXmN+ag8HUwVPKyUtMhgSLhZSQwgD.1712013537.15666.325675.ce704dfa44ee08c6befe18af535e2232',
        'yandex_login': 'askaryaparov',
        'is_gdpr': '0',
        'is_gdpr_b': 'CPHKBhCF+AEoAg==',
        'sessionid2': '3:1714748924.5.0.1660165482208:2v3Wsg:4b.1.2:1|612983000.-1.2|'
                      '1939657944.47574649.2.2:47574649.3:1707740131|315217873.-1.2.2'
                      ':49916427.3:1710081909|6:10190723.887776.fakesign0000000000000000000',
        'Session_id': '3:1714756869.5.0.1660165482208:2v3Wsg:4b.1.2:1|612983000.-1.2|1939657'
                      '944.47574649.2.2:47574649.3:1707740131|315217873.-1.2.2:49916427.3:17'
                      '10081909|6:10190728.457535.U0ELSpSw790irlSTgE06mWqI00s',
        'sessar': '1.1189.CiBrfZuVbRbZ6ms5qSaSVleakZCrYXYc09A2vd-B3r941Q.LMBG73Jt-vmZ820Fo9LrQgTVcYn4OvDubEhCDPM2oEw',
        'i': 'fVUPUF/CKeC0SuBVzsNs0VTPPUsEuHk9gu2MfxhTfYYQEjmJu6u5HFhgDp+HOmsUz3KrpHsvRPD1KdmqFaTm9TBs69o=',
        'mda2_beacon': '1714756869438',
        'yandex_csyr': '1714756869',
        'isa': '4ra7iffZAdBMiHidQAaJwakYhS58Bpvibr1Th9hoAZGxPeE9P+iNvC4hmeOplSF7SlN9MxjZf5KzV2aNGBSSD2HO/oU=',
        'sae': '0:4DAA20BC-F2EF-4D36-A34E-28A362DB5711:p:24.4.1.899:w:d:RU:20220214',
        '_ym_d': '1714992617',
        '_yasc': 'PN5XbcvH5KD1ZjwLSZBh92pAx0Rq2pnP8PsmrwB8+7oYWD56pxCPtJou/DFUmrtxAa/Qrk/+BP3Rpw==',
        '_ym_isad': '2',
        'suid': '541ad048f74e38e9e88041bbddfe6a5a.c83bd9855037fa20ec29546aec174bd7',
        '_csrf_token': '232c276b82b74bf597777fa562d6347cc84fac14fcf81354',
        'from': 'search',
        'exp_uid': 'e986612b-db5a-410d-9156-0289e5691241',
        'show_egrn_reports_link': 'NO_612983000',
        'font_loaded': 'YSv1',
        'KIykI': '1',
        'yp': '1741617910.brd.0201004775#1741617910.cld.2270452#1717427337.csc.1#1715069321.duc'
              '.ru#1715012324.gpauto.59_938786:30_314997:100000:3:1715005124#1716900561.hdrc.1#'
              '2023100131.multib.1#2030111162.pcs.1#4294967295.skin.s#1739720855.stltp.serp_bk-'
              'map_1_1708184855#1730516927.szm.1:1366x768:1301x691#1715069321.uc.ru#2030116869.udn.cDpBc2thciBZYXBhcm92',
        'prev_uaas_data': '%7B%22uaasExpNames%22%3A%5B%22REALTYFRONT-16113_bring_tenant_banner%22%2C%22REALTYFRONT'
                          '-16792_show_arenda_chat_button%22%2C%22REALTYFRONT-17599_new_owner_target%22%2C%22REALT'
                          'YFRONT-19425_redesign_site_plans_modals%22%2C%22REALTYFRONT-18481_verticals_3d_tour%22'
                          '%2C%22REALTYFRONT-18486_hide_candidates_questionnaire%22%2C%22REALTYFRONT-20711_quick_'
                          'request_for_an_impression%22%2C%22REALTYFRONT-21701_owner_get_consultation_target%22%2'
                          'C%22REALTYBACK-13472_newbuilding_rate_change%22%2C%22REALTYFRONT-18560_realty_hidden_f'
                          'lat_number%22%2C%22REALTYFRONT-22002_show_podbor_pdf_for_mobile_number_banners%22%2C%22'
                          'REALTYBACK-9999_disable_paid_only%22%2C%22REALTYFRONT-22647_Arenda_highlight_tooltip_me'
                          'ssage_1%22%2C%22REALTYFRONT-20255_plus_2_0%22%2C%22REALTYFRONT-21174_hide_vas_trap%22%2'
                          'C%22REALTYFRONT-21278_hidden_price_desc%22%2C%22REALTYFRONT-21695_show_new_landing_owne'
                          'r%22%2C%22REALTYFRONT-15266_view_inventory_in_tenant_candidate_flow%22%2C%22REALTYFRONT'
                          '-21282_guaranteed_payments_banner%22%2C%22REALTYFRONT-21374_listing_video_tour_gallery%'
                          '22%2C%22REALTYFRONT-20932_without_newbuilding_carousel%22%5D%2C%22uaasUid%22%3A%2277610'
                          '32951644804503%22%7D',
        'prev_uaas_expcrypted': 'uZqytupj6yJQNUOgul5QZzTTjGZb_zx1B_JKtYfaMpnSpaPx_SCOQVj5x7XrlAZNJ2AFMk0ax-ulGmnHZd'
                                'ZOs1SWelDmk28mVFNyPmMib6_4SegmaCfejFetX2RflxQ2xAhyOMZS6M141JNn-sNK2DJixc1R4Ntmn0ZB'
                                '0G31F-Q2QHTXcgHgGrUbEX-x5BSagTOkH9QkWwZNDg5tcjXGHIeZPhOyWM4NK0DYG1_Yg2xArO9zod3SPP'
                                'YB89et6kjvWaCRjSLtzuBWe6_L_KdtBPT02o4qdd7tmoHG0C1IUgUr2JBk83CfZHNczN15mBJYjvC1qaL'
                                'C8EdG01sZD3_r6fSrlop2_xD2Mfs2pM4jkYJQOVFLtVJvkJh5g8aTGQHR4nt0K75tUzMfOdKy0KbFrw%2C%2C',
        'rgid': '417899',
        'geo_id': '2',
        'region_id': '10174',
        'from_lifetime': '1715005360237',
        '_yasc': 'XDl4Gn1ur2aGCmgVgQGcGmfi55P6U23j0AAWPka1spDcCUyYkukjW8x6bf1O2ZBtjYhJIyge/QY0Qg==',
    }

    headers = {
        'authority': 'realty.ya.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'referer': f'https://realty.ya.ru/{location}/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version-list': '"Chromium";v="122.0.6261.156", "Not(A:Brand";v="24.0.0.0", '
                                       '"YaBrowser";v="24.4.1.899", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
    }

    if q['deal'] == 'buy':
        url = f'https://realty.ya.ru/{location}/kupit/'
    else:
        url = f'https://realty.ya.ru/{location}/snyat/'

    ob_d = {
        'flat': 'kvartira/',
        'room': 'komnata/',
        'suburban': 'dom/',
        'plot': 'uchastok/',
        'garage': 'garazh/',
        'commercial': 'kommercheskaya-nedvizhimost/',

    }

    url += ob_d[type_obj]

    params = {
        'priceMax': '10000000',
    }

    if q['cycle'] != 'all':
        if q['cycle'] == 'new':
            params['newFlat'] = 'YES'
        elif q['cycle'] == 'used':
            params['newFlat'] = 'NO'

    if q['room_count'] is not None:
        params['roomsTotal'] = ['1']

    response = requests.get(url,
                            params=params, cookies=cookies, headers=headers)
    with open('yandex.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

    soup = BeautifulSoup(response.text, 'lxml')

    box = soup.findAll('li', attrs={'data-seo': 'snippet'})
    print(len(box))
    for item in box:
        for img in item.findAll('img'):
            print(f'https:{img["src"]}')


yandex_page('sankt-peterburg', 'flat', {'deal': 'buy', 'cycle': 'used', 'room_count': ['1']})
