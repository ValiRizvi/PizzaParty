from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

webdriver_path = '/Users/Vali/Desktop/python/geckodriver'

driver = webdriver.Firefox(executable_path=webdriver_path)

driver.get('https://www.dominos.ca/en/pages/order/coupon')
driver.get('https://www.dominos.ca/en/pages/order/coupon')
driver.get('https://www.dominos.ca/en/pages/order/coupon')

try:
    element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'See local coupons')]"))
        )
    element.click()
except:
    driver.quit()








