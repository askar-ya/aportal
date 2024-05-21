from models import Flat
from avito import get_avito_filter, get_avito_page

flat = Flat(deal='buy')
r = flat.to_form()
print(r)

print(get_avito_page('Москва',
                     get_avito_filter('Москва',
                                      'flat',
                                      r
                                      )
                     )
      )
