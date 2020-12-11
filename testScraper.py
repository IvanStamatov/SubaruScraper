from urllib.request import urlopen
from bs4 import BeautifulSoup, element

import requests

html = urlopen('https://www.mobile.bg/pcgi/mobile.cgi')

bs_objects = BeautifulSoup(html.read(), features='lxml')

# find and extract form action url
search_button = bs_objects.body.find('input', {'type':'button'})
action_url = 'http:{}'.format(search_button['onclick'])

# find all car brands form select element and put them in list
brand_list = []
for brand in  bs_objects.body.find('select', {'name':'marka'}).children:
    if type(brand) is element.Tag:
        brand_list.append( brand['value'] )


user_input_marka = input('izberi marka: ')
brand_idx = brand_list.index(user_input_marka)
params = { 'marka': brand_list[brand_idx] }


# POST request to form with params
post_request = requests.post(action_url, data=params)
print(post_request.text)