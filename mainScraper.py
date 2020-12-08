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

# Take input from terminal. This will be the request from the portal in the future
# Have not done any formating of the result or any try/catch cases yet
carBrand = input("Марка: ") 
carModel = input("Модел: ") 
carCategory = input("Категоря: ") 




# ==== Section for only getting the link to the listings
# Selenium - when creating the chrome browser, it will be invisible
options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path = "drivers/chromedriver.exe", chrome_options=options)

# Got to the home search page of mobile.bg
driver.get('https://www.mobile.bg/pcgi/mobile.cgi?pubtype=1&act=2')

# BeautifulSoup - brand = select class="sw145", name="f5"
selectBrand = Select(driver.find_element_by_name('f5'))
selectBrand.select_by_visible_text(carBrand)

# BeautifulSoup - model name = f6
selectModel = Select(driver.find_element_by_name('f6'))
selectModel.select_by_visible_text(carModel)

# BeautifulSoup - category name = f14
selectCategory = Select(driver.find_element_by_name('f14'))
selectCategory.select_by_visible_text(carCategory)

# BeautifulSoup - value = Т Ъ Р С И
buttonSearch = driver.find_element_by_xpath("//input[@value='Т Ъ Р С И']")
buttonSearch.click()

# Get the current page as we need it to get all of the listings
listingPage = driver.current_url
print(listingPage)
driver.quit()





# ==== Function for getting all car listing from the link we got from the first section
def listingCollector(link):
    # Beautiful Soup - opens the link and extracts the HTML from it
    newUrl = link
    uClient = uReq(newUrl)
    page_html = uClient.read()
    uClient.close()
    pageSoup = soup(page_html, "html.parser")

    # Finds all A elements with the class "mmm". This depends on the site - we get it using Inspect Element and looking at the html code itself
    listingsListOld = pageSoup.find_all("a", class_="mmm")

    # For as many listings there are on the page, add each listing to a list
    for i in range(len(listingsListOld)):
        listingsList.append("https:" + listingsListOld[i].get('href'))
    
    return





# ==== Function for processing a listing and extracting details from it
def listingData(linkPage):
    newUrl = linkPage
    uClient = uReq(newUrl)
    page_html = uClient.read()
    uClient.close()
    pageSoup = soup(page_html, "html.parser")

    # Get the title of the listing 
    title = pageSoup.find_all('h1')[0].text
    

    # span id="details_price"
    price = pageSoup.find(id="details_price").text


    # td style="line-height:24px; font-size:14px; color: #444;"
    # Catching an error if there is no description
    try:
      description = pageSoup.find_all('td', attrs={'style' : 'line-height:24px; font-size:14px; color: #444;'})[0].text
      print(description)
    except IndexError:
      print("This listing does not have a description.")

    # ul class="dilarData"
    detailsUL = pageSoup.find_all("ul", {"class": "dilarData"})[0]
    detailsLI = detailsUL.find_all('li')

    # A roundabout way of getting the UL/LI elements into basic text. When implementing a DB, this will change
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
    


    # Print the collected data:
    print("Link to the web page: " + str(linkPage))
    print("Title of listing: " + title)
    print(price)
    print(stringUL)

    return





# ==== Main script section
uClient = uReq(listingPage) 
page_html = uClient.read()
uClient.close()
pageSoup = soup(page_html, "html.parser")

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

    # Get the links for all pages and store them into a list
    mainPageLinks.append(listingPage)
    for i in range(max(pageNumList) - 1):
        mainPageLinks.append("https:" + numOfPages[i].get('href'))

    # print(mainPageLinks) would look like:
    # {'page 1': 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0zjk1&f1=1', 'page 2': 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0zjk1&f1=2', 'page 3': 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=i0zjk1&f1=3'}  



# Going into every listing on every page
# for every page:
#   get all listings
num = 0
# for every page in the list , call function to collect the listings
for x in mainPageLinks:
    listingCollector(mainPageLinks[num])
    num += 1



# For each individual listing, call function to gather details from it
num1 = 0
for x in listingsList:
    # print("Listing number: " + str(num1 + 1))
    listingData(listingsList[num1])
    num1 += 1



# print("End of the script.")
