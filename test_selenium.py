from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

webdriver_path = '/Users/Vali/Desktop/python/geckodriver'

browser = webdriver.Firefox(executable_path=webdriver_path)

browser.get('https://www.google.com')

input_element = browser.find_element(By.ID, 'APjFqb')
input_element.clear()
input_element.send_keys('dominos pizza' + Keys.ENTER)

time.sleep(5)

browser.quit()

