# Plan:
# go to moble.bg and search for subaru impreza (make an object for the search)
# check how many pages there are and get the links for each page
# go into the first page and get every listing
# Export each listing into a database
# Compare the listing to the existing ones in the database
#     if it is the same, then do not add it
# 
# Database: SQLite
# Web App: Flask
# Need to check where to host it
# 
# 
# 
# 
# 

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options




listingsList = []
listingsListOld = []

indexInc0 = 0
indexInc1 = 1 
detailsDic = {}

carBrand = input("Марка: ") 
carModel = input("Модел: ") 
carCategory = input("Категоря: ") 

options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path = "drivers/chromedriver.exe", chrome_options=options)

driver.get('https://www.mobile.bg/pcgi/mobile.cgi?pubtype=1&act=2')

# brand = select class="sw145", name="f5"
selectBrand = Select(driver.find_element_by_name('f5'))
selectBrand.select_by_visible_text(carBrand)


# model name = f6
selectModel = Select(driver.find_element_by_name('f6'))
selectModel.select_by_visible_text(carModel)

# category name = f14
selectCategory = Select(driver.find_element_by_name('f14'))
selectCategory.select_by_visible_text(carCategory)

# value = Т Ъ Р С И
buttonSearch = driver.find_element_by_xpath("//input[@value='Т Ъ Р С И']")
buttonSearch.click()

listingPage = driver.current_url
print(listingPage)
driver.quit()




def listingCollector(link):
    newUrl = link
    uClient = uReq(newUrl)
    page_html = uClient.read()
    uClient.close()
    pageSoup = soup(page_html, "html.parser")


    listingsListOld = pageSoup.find_all("a", class_="mmm")
    # print("The number of listings are: " + str(len(listingsListOld)))

    for i in range(len(listingsListOld)):
        listingsList.append("https:" + listingsListOld[i].get('href'))
    # print(listingsList)
    
    return


def listingData(linkPage):
    newUrl = linkPage
    uClient = uReq(newUrl)
    page_html = uClient.read()
    uClient.close()
    pageSoup = soup(page_html, "html.parser")

    


    title = pageSoup.find_all('h1')[0].text
    
    

    # span id="details_price"
    price = pageSoup.find(id="details_price").text


    # td style="line-height:24px; font-size:14px; color: #444;"
    try:
      description = pageSoup.find_all('td', attrs={'style' : 'line-height:24px; font-size:14px; color: #444;'})[0].text
      print(description)
    except IndexError:
      print("This listing does not have a description.")

    # ul class="dilarData"
    detailsUL = pageSoup.find_all("ul", {"class": "dilarData"})[0]
    

    detailsLI = detailsUL.find_all('li')

    indexInc0 = 0
    indexInc1 = 1 
    detailsDict = {}
    stringUL = ""
    for i in detailsLI:
        detailsDict[detailsLI[indexInc0].text] = detailsLI[indexInc1].text
        indexInc0 += 2
        indexInc1 += 2
        if indexInc1 > len(detailsLI):
          break

    for key, value in detailsDict.items():
        stringUL += key + " : " +  value + "\n"



    print("Link to the web page: " + str(linkPage))
    print("Title of listing: " + title)
    print(price)
    
    print(stringUL)



    return



















# url with a single page: https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0zolk&f1=1
# url with 3 pages: https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0zjk1&f1=1

uClient = uReq(listingPage) #downloads the webpages to a variable
page_html = uClient.read()
uClient.close()
pageSoup = soup(page_html, "html.parser")




# ===== Checking how many pages there are =====
# the page ulr does not change besides the number at the end:
# https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0ziek&f1=1
# https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0ziek&f1=2
# The first page will always be class="pageNumbersSelect"
# Subsequent pages will be class="pageNumbers"
#    So check how many instances there are of the class . The number of total pages = 1 + number of class instances
# There are two contianers that show the number of pages - scraping gets both of them
numOfPages = pageSoup.find_all('a', class_ = "pageNumbers")
pageNumList = []
mainPageLinks = []

if not numOfPages:
    # print("there is only a single page")
    mainPageLinks.append(listingPage)
else:
    for i in range(len(numOfPages)):
        pageNumList.append(int(numOfPages[i].text))
        i += 1
    # print("The number of pages is : " + str(max(pageNumList)))

    mainPageLinks.append(listingPage)
    for i in range(max(pageNumList) - 1):
        mainPageLinks.append("https:" + numOfPages[i].get('href'))

    # print(mainPageLinks)
    # {'page 1': 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0zjk1&f1=1', 'page 2': 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0zjk1&f1=2', 'page 3': 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0zjk1&f1=3'}  



# Going into every listing on every page
# for every page:
#   get all listings
#       call function to go into every listing and gather data
#           export data 

# print(mainPageLinks)

num = 0
# for every page in the dic , call function to collect the listings
for x in mainPageLinks:
    # print("Current page is : " + mainPageLinks[num])
    listingCollector(mainPageLinks[num])
    num += 1

# print("The number of listings are: " + str(len(listingsList)))
# print(*listingsList, sep = "\n")

num1 = 0
for x in listingsList:
    print("Listing number: " + str(num1 + 1))
    listingData(listingsList[num1])
    num1 += 1

# listingData(listingsList[0])


print("End of the script.")
