# Python program to demonstrate
# selenium

# import webdriver
from selenium import webdriver



fireFoxOptions = webdriver.FirefoxOptions()
#fireFoxOptions.set_headless()
fireFoxOptions.headless = True

# create webdriver object
#driver = webdriver.Firefox()
driver = webdriver.Firefox(options=fireFoxOptions)
# get google.co.in
driver.get("https://google.co.in")
html_src = driver.page_source
print(html_src)
driver.quit()
print("https://google.co.in")
