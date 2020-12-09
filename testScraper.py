from urllib.request import urlopen
from bs4 import BeautifulSoup

import requests

html = urlopen('https://www.mobile.bg/pcgi/mobile.cgi')

bs_objects = BeautifulSoup(html.read(), features='lxml')

# find and extract form action url
search_form = bs_objects.body.find('form', {'name':'search'})

action_url = 'http:{}'.format(search_form['action'])

# POST request to form

post_request = requests.post(action_url)

print(post_request.text)