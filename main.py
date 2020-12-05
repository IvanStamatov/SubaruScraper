from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import smtplib
from email.message import EmailMessage

# video for the push notification: https://www.youtube.com/watch?v=B1IsCbXp0uE

# so you can call them with just "soup" and "uReq"

# https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=hn2haq&f1=1
# ----- Resources -----
# https://www.youtube.com/watch?v=XQgXKtPSzUI 
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all


#   The Plan:
#   - go through the main page 
#   - get a link for every car listing
#   - visit every link and get the page info we need
#   - store that page info
#   - after getting through all of the links, send an email with the stored info
#   ghjhgjgh
#   
#   
#   
#   
#   
#   
#   
#   




def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    
    user = "stamybot@gmail.com"
    password = "liybehfxfchnmidr"

    msg['from'] = user

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()


my_ulr = 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=hn2haq&f1=1'

uClient = uReq(my_ulr) #downloads the webpages to a variable
page_html = uClient.read()
uClient.close()

print("Got the main page downloaded.")

page_soup = soup(page_html, "html.parser")



containers = page_soup.find_all("a", class_="mmm")

linksList = []
indexIncr = 0

for carLink in containers:
  linksList.append("https:" + containers[indexIncr]['href'])
  # print("Car " + str(indexIncr) + " is : " + containers[indexIncr].text)
  # print("The link for it is: " + containers[indexIncr]['href'] + "\n" )
  indexIncr += 1


print("the number of obqvi is: " + str(len(linksList)))





print("Got the links from the main page. \n    Going into the first link...\n")

indexIncr = 0
detailsDict = {}

indexInc0 = 0
indexInc1 = 1

mainStringWall = "Start of the message.\n"

for i in linksList:
    carTitle = carPrice = carLocation = carDescription = None

    newUrl = linksList[indexIncr]
    uClient = uReq(newUrl)
    page_html = uClient.read()
    uClient.close()

    indexIncr += 1
    
    #print("Showing detials for car Number: " + str(indexIncr))
    mainStringWall += "Showing detials for car Number: " + str(indexIncr) + "\n"

    pageSoup = soup(page_html, "html.parser")

    carTitle = pageSoup.h1.string

    carPrice = pageSoup.find_all('strong', attrs={'style': 'color: #09f;'})[0].text
    
    carLocation = pageSoup.find_all('div', attrs={'style' : 'padding-left:0px;width:144px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom:5px;'})[0].text

    # ul class is named dilarData
    carDetailsUL = pageSoup.find_all('ul', class_="dilarData")[0]
    carDetailsLI = carDetailsUL.find_all('li')
    for i in carDetailsLI:
        #print(carDetailsLI[indexIncrIns0].text + " : " + carDetailsLI[indexIncrIns1].text)
        #indexIncrIns1 += 1
        #indexIncrIns0 += 1
        #print(str(indexInc0) + " : " + str(indexInc1))
        detailsDict[carDetailsLI[indexInc0].text] = carDetailsLI[indexInc1].text
        indexInc0 += 2
        indexInc1 += 2
        if indexInc1 > len(carDetailsLI):
          break
        
    indexInc0 = 0
    indexInc1 = 1 

    try:
      carDescription = pageSoup.find_all('td', attrs={'style' : 'line-height:24px; font-size:14px; color: #444;'})[0].text
    except IndexError:
      print("This obqva does not have a description.")

    # print("Title: " + str(carTitle) + "\nPrice: " + str(carPrice) + "\nLocation: " + str(carLocation) )
    mainStringWall += "Title: " + str(carTitle) + "\nPrice: " + str(carPrice) + "\nLocation: " + str(carLocation) + "\n"
    for key, value in detailsDict.items():
        mainStringWall += key + " : " +  value + "\n"
    
    # print("Description: " + str(carDescription) + "\n\n++++++++++\n")
    mainStringWall += "Description: " + str(carDescription) + "\n\n++++++++++\n\n"


if __name__ == "__main__":
    email_alert("Test notification email", mainStringWall, "ivan.t.stamatov@gmail.com")

#print(mainStringWall)

print("done")

    