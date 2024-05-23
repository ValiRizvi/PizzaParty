from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

webdriver_path = '/Users/Vali/Desktop/python/geckodriver'

driver = webdriver.Firefox(executable_path=webdriver_path)

# page is reloaded 3 times to ensure DOM loads
driver.get('https://www.dominos.ca/en/pages/order/coupon')
time.sleep(3)
driver.get('https://www.dominos.ca/en/pages/order/coupon')
driver.get('https://www.dominos.ca/en/pages/order/coupon')

# function to click elements
def clickElement(path:str):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"{path}"))
    )
    element.click()

# click through to location page
clickElement("//a[contains(text(),'See local coupons')]")
time.sleep(2)
clickElement("/html/body/div[3]/div[3]/div/div/div[2]/form/div/div[2]/label[2]/span[1]")

# enter postal code in map text field
element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='cityFinder']"))
    )
element.click()
time.sleep(7)
element.send_keys('L5m0v7' + Keys.ENTER)

# select nearest location for carryout
clickElement("/html/body/div[3]/div[3]/div/div/div[2]/form/div/div[4]/div[2]/div/div[2]/div/div[4]/div/div/div/button")

# wait for all coupons to load
time.sleep(3)

# collect all coupons 
elements = driver.find_elements(By.XPATH, "//*[@class='grid__cell--1/3@desktop grid__cell--1/2 local-coupon local-coupon__container js-dottedCouponBorder']")

# write all the scraped text to date.txt file for parsing
with open('data.txt', 'w') as file:
    for element in elements:
        file.writelines(element.text)

# close browser
driver.quit()




















