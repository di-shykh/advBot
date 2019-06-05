from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

import time
import random
import sys
import os
from sys import platform

import pickle

import shared_data #тут данные пользователя и объявление, которые будут общие для всех сайтов

username = shared_data.username 
email=shared_data.email
password = shared_data.password

path_to_cookies=os.path.join('scripts/cookies','cookies_irr_by.pkl')

if platform == "linux" or platform == "linux2":
  driver=webdriver.Chrome('chromedriver')
elif platform == "darwin":
  driver=webdriver.Chrome('chromedriver_mac')
elif platform == "win32":
  driver = webdriver.Chrome('chromedriver.exe')

class Account:
  def __init__(self,username,password,email):
    self.username=username
    self.password=password
    self.email=email

class IRR_Bot:
  def __init__(self,user,advertisment):
    self.user=user
    self.advertisment=advertisment
    self.driver=webdriver.Chrome()

  def closeBrowser(self):
    self.driver.quit()
  
  def login(self):
    self.driver.get('http://irr.by/')
    
    time.sleep(random.randint(1,3))
    link_to_login=self.driver.find_element_by_xpath("//a[@id='a_login']/span[text()='Вход']").click()

    time.sleep(3)
    popup_window=self.driver.find_element_by_xpath("//form[@id='loginForm']") #id='reg_block'

    email_input=popup_window.find_element_by_xpath('//input[@name="login"]')
    email_input.clear()
    email_input.send_keys(self.user.email)

    time.sleep(random.randint(1,3))
    password_input=popup_window.find_element_by_xpath("//input[@type='password'][@name='password']")
    password_input.clear()
    password_input.send_keys(self.user.password)

    remember_me=popup_window.find_element_by_xpath("//input[@type='checkbox'][@name='is_remember_me']")
    if not remember_me.is_selected():
      remember=popup_window.find_element_by_xpath("//p[@class='remember']").click()
    
    time.sleep(random.randint(1,3))
    button_enter=popup_window.find_element_by_xpath('//input[@type="submit"][@value="Вход"]')
    button_enter.click()

  def saveCookies(self):
    self.login()
    #cookies dump
    pickle.dump( self.driver.get_cookies() , open(path_to_cookies,"wb")) 
    #driver.close() 

  def loginWithCookies(self):
    self.driver.get('http://irr.by/')
    #get cookies from dump
    cookies = pickle.load(open(path_to_cookies,"rb"))
    self.driver.delete_all_cookies()#delete old cookes from browser
    for cookie in cookies:
      self.driver.add_cookie(cookie)
    time.sleep(3)
    self.driver.get('http://irr.by/account/items')

    self.closeNotificationAlert()

  def closeNotificationAlert(self):
    alert=None
    try:
      alert=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='Notification']")))
    except:
      print('no alert elements')
    finally:
      if alert:
        time.sleep(2)
        button_no=alert.find_element_by_xpath("//div[@class='Notification-buttons']/a[text()='Нет']").click()

  def addAdvertisment(self):
    self.driver.get('http://irr.by/advertSubmission/step1/')
    #button_add_advertisment=self.driver.find_element_by_xpath("//a[text()='Подать объявление']").click()
    self.fillInputs()
  
  def fillInputs(self):
    #select_region=self.driver.find_element_by_xpath("//select[@name='address_region']")
    #option_region=select_region.find_element_by_xpath("//option[contains(text(),'"+self.advertisment.location.city+"']").click() #подумать как лучше задавать область для всех областей
    div=self.driver.find_element_by_xpath("//div[@id='fr_region_chzn']")
    div.click()
    option_region=div.find_element_by_xpath("//a[contains(text(),'"+self.advertisment.location.city+"']").click()#тут падает
    time.sleep(2)
    input_city=self.driver.find_element_by_xpath("//input[@name='address_city']")
    input_city.clear()
    input_city.send_keys(self.advertisment.location.city)
    time.sleep(2)
    #select_category=self.driver.find_element_by_xpath("//select[@id='sel1']")
    #category=select_category.find_element_by_xpath("//option[contains(text(),'"+self.advertisment.category+"']").click()
    category=self.driver.find_element_by_xpath("//div[@id='sel1_chzn']/a[contains(text(),'"+self.advertisment.category+"']").click()
    time.sleep(2)
    #category2=self.driver.find_element_by_xpath("//option[contains(text(),'"+self.advertisment.category+"']")
    category2=self.driver.find_element_by_xpath("//li[contains(text(),'"+self.advertisment.category+"']").click()


if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment

    irr = IRR_Bot(user,advertisment)
    #irr.saveCookies()
    irr.loginWithCookies()
    irr.addAdvertisment()