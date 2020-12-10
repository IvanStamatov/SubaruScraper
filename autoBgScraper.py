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

URL = 'https://www.auto.bg'

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

    for entry in filter.brand:
        print( entry )



html = url_open(URL)
bs_objects = BeautifulSoup(html.read(), features='lxml')
select_el = bs_objects.find('form', {'name':'search'})

filter = filters_pb2.Filters()

# List categories
categories = bs_objects.find('select', {'name':'cat'}).descendants
for option in categories:
    if type(option) is element.Tag and 'value' in option.attrs:
        filter.type.append(option['value'])

# List car brands
brands = bs_objects.find('select', {'name':'marka'}).descendants
for option in brands:
    if type(option) is element.Tag and 'value' in option.attrs:
        filter.brand.append(option['value'])

#write extracted data to protobufer
f = open("AutoBgFilters.json", "wb")
f.write(filter.SerializeToString())
f.close()

#read data
read_fliter('AutoBgFilters.json')





