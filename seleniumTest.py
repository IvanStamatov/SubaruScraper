from selenium import webdriver
from selenium.webdriver.support.ui import Select


# https://selenium-python.readthedocs.io/navigating.html
# home page for the search:    https://www.mobile.bg/pcgi/mobile.cgi?pubtype=1&act=2


driver = webdriver.Chrome(executable_path = "drivers/chromedriver.exe")

driver.get('https://www.mobile.bg/pcgi/mobile.cgi?pubtype=1&act=2')

# brand = select class="sw145", name="f5"
selectBrand = Select(driver.find_element_by_name('f5'))
selectBrand.select_by_visible_text("Subaru")


# model name = f6
selectModel = Select(driver.find_element_by_name('f6'))
selectModel.select_by_visible_text("Impreza")

# category name = f14
selectCategory = Select(driver.find_element_by_name('f14'))
selectCategory.select_by_visible_text("Седан")

# value = Т Ъ Р С И
buttonSearch = driver.find_element_by_xpath("//input[@value='Т Ъ Р С И']")
buttonSearch.click()

# driver.quit()