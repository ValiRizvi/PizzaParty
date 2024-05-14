from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

webdriver_path = '/Users/Vali/Desktop/python/geckodriver'

driver = webdriver.Firefox(executable_path=webdriver_path)

driver.get('https://www.dominos.ca/en/pages/order/coupon')
time.sleep(3)
driver.get('https://www.dominos.ca/en/pages/order/coupon')
driver.get('https://www.dominos.ca/en/pages/order/coupon')

element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'See local coupons')]"))
    )
element.click()

element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[3]/div/div/div[2]/form/div/div[2]/label[2]/span[1]"))
    )
element.click()

element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='cityFinder']"))
    )
element.click()

time.sleep(10)
element.send_keys('l5m0v7' + Keys.ENTER)


















