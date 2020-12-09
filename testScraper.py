from urllib.request import urlopen
from bs4 import BeautifulSoup, element

import requests

html = urlopen('https://www.mobile.bg/pcgi/mobile.cgi')

bs_objects = BeautifulSoup(html.read(), features='lxml')

# find and extract form action url
search_form = bs_objects.body.find('form', {'name':'search'})
action_url = 'http:{}'.format(search_form['action'])

# find all car brands form select element and put them in list
brand_list = []
for brand in  bs_objects.body.find('select', {'name':'marka'}).children:
    if type(brand) is element.Tag:
        brand_list.append( brand['value'] )


user_input_marka = input('izberi marka: ')
brand_idx = brand_list.index(user_input_marka)
params = { 'marka': str(brand_idx) }


# POST request to form with params
post_request = requests.post(action_url)
print(post_request.text)