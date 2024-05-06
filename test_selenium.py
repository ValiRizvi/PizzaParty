from selenium import webdriver 

webdriver_path = '/Users/Vali/Desktop/python/geckodriver'

browser = webdriver.Firefox(executable_path=webdriver_path)

browser.get('https://www.example.com')

