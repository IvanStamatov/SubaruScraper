from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup, element
import filters_pb2  
import requests


#query example
#https://www.auto.bg/obiavi/avtomobili-dzhipove/audi/a4/dizelov/oblast-sofiya?
# transmission=Автоматична&
# category=Комби&
# engine_power1=300&
# year1=2015&
# price1=30000&
# extri=0000000010000000000000000000000100000010000000001000010000000000000001000000000000000000000000000000&
# price=10000&
# engine_power=150&
# year=2010

# 1) Extract all pssible seach filters with bs
# 2) store filters for each website
# 3) extract and query filters to assemble the query url
# 4) Extract data form each listing recursively 

URL = 'https://www.auto.bg/search'

def url_open(URL):
    try:
        return urlopen(URL)
    except HTTPError as e:
        print(e)
        return None


def read_fliter(file):
    f = open(file, 'rb')
    filter = filters_pb2.Filters()
    filter.ParseFromString(f.read())
    f.close()

    print('categories{}'.format(filter.categories))
    print('brands{}'.format(filter.brands))
    print('models{}'.format(filter.models))
    print('sorting_types{}'.format(filter.sorting_types))
    print('types{}'.format(filter.types))
    print('condition{}'.format(filter.condition))
    print('price ranges:]\n')
    i = 0
    for price_from in filter.price._from:
        print('{} - {}\n'.format(price_from, filter.price.to[i]))
        i += 1



html = url_open(URL)
bs_objects = BeautifulSoup(html.read(), features='lxml')
select_el = bs_objects.find('form', {'name':'search'})

filter = filters_pb2.Filters()

# Scrape listing sorting opitons
sorting_types = bs_objects.find('select', {'name':'sort'}).descendants
for entry in sorting_types:
    if type(entry) is element.Tag and entry.has_attr('value'):
        key = int(entry['value'])
        filter.sorting_types[key] = entry.text

# Scrape categories
categories = bs_objects.find('select', {'name':'cat'}).descendants
for entry in categories:
    if type(entry) is element.Tag and entry.has_attr('value'):
        key = int(entry['value'])
        filter.categories[key] = entry.text 

# Scrape car brands
brands = bs_objects.find('select', {'name':'marka'}).descendants
filter.brands.extend([entry['value'] for entry in brands if type(entry) is element.Tag and entry.has_attr('value')])

# Scrape vehicle types
types = bs_objects.find('select', {'name':'marka'}).descendants
filter.types.extend([entry['value'] for entry in types if type(entry) is element.Tag and entry.has_attr('value')])


# Scrape vehicle condition checkbox values
condition = bs_objects.find('div', {'class':'condition'}).descendants
for entry in condition:
    if type(entry) is element.Tag and entry.has_attr('value'):
        key = int(entry['value'])
        filter.categories[key] = entry.text 

# Scrape price ranges
# "from" values
price_ranges = bs_objects.find('select', { 'class':'ot-do', 'id':'pr1S' }).descendants
filter.price._from.extend([int(entry['value']) for entry in price_ranges if type(entry) is element.Tag and entry.has_attr('value') and entry.text])
# "to" values
price_ranges = bs_objects.find('select', { 'class':'ot-do', 'id':'pr2S' }).descendants
filter.price.to.extend([int(entry['value']) for entry in price_ranges if type(entry) is element.Tag and entry.has_attr('value') and entry.text])

# Scrape car models
# !!! In order to scrape car modules we need to select a car brand and request the url again !!!
params = {'marka': filter.brands[5]}
rquest = requests.post(URL, data=params)
bs_objects = BeautifulSoup(rquest.text, features='lxml')
brands = bs_objects.find('select', {'name':'model'}).descendants
filter.models.extend([entry['value'] for entry in brands if type(entry) is element.Tag and entry.has_attr('value')])





#write extracted data to protobufer
f = open("AutoBgFilters.json", "wb")
f.write(filter.SerializeToString())
f.close()

#read data
read_fliter('AutoBgFilters.json')





