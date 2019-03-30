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

username = "di49di49" 
email="****" #убрала,чтобы не светить ящик и пароль
password = "*****" #убрала,чтобы не светить ящик и пароль

path_to_cookies=os.path.join('cookies','cookies_oo_by.pkl')

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

class OO_Bot:
  def __init__(self,user,advertisment):
    self.user=user
    self.advertisment=advertisment
    self.driver=webdriver.Chrome()

  def closeBrowser(self):
    self.driver.close()
  
  def login(self):
    self.driver.get('http://oo.by/login.html')

    time.sleep(random.randint(1,3))
    username_input=self.driver.find_element_by_xpath('//input[@name="username"]')
    username_input.clear()
    username_input.send_keys(self.user.username)

    time.sleep(random.randint(1,3))
    password_input=self.driver.find_element_by_xpath('//input[@name="password"]')
    password_input.clear()
    password_input.send_keys(self.user.password)
    
    time.sleep(random.randint(1,3))
    button_enter=self.driver.find_element_by_xpath('//button[@type="submit"][@name="Login"]')
    time.sleep(random.randint(2,5))
    button_enter.click()

  def saveCookies(self):
    self.login()
    #cookies dump
    pickle.dump( self.driver.get_cookies() , open(path_to_cookies,"wb")) 
    #driver.close() 

  def loginWithCookies(self):
    self.driver.get('http://oo.by/')
    #get cookies from dump
    cookies = pickle.load(open(path_to_cookies,"rb"))
    self.driver.delete_all_cookies()#delete old cookes from browser
    for cookie in cookies:
      self.driver.add_cookie(cookie)
      if cookie.get('name')=='PHPSESSID':
        session_id=cookie.get('value')
    time.sleep(3)
    self.driver.get('http://oo.by/index.php?phpSESSID='+session_id)

  def addAdvertisment(self):
    self.driver.get('http://oo.by/newad.php')

    time.sleep(2)
    category_click=self.driver.find_element_by_xpath('//select[@name="category"]').click()
    category=self.driver.find_element_by_xpath('//select[@name="category"]')
    for option in category.find_elements_by_tag_name('option'):
      if 'Животные' in option.text:
        option.click() 
        break
    submit_button=self.driver.find_element_by_xpath("//button[@type='submit'][@name='Choose_categ']").click()

    self.fillAdvertismentInputs()

    next_step_button=self.driver.find_element_by_xpath("//button[@type='submit'][@name='Submit']").click()

    self.addImages()

    next_step_button2=self.driver.find_element_by_xpath("//button[@type='submit'][@name='Add_photos']").click()
    time.sleep(random.randint(3,5))

    approve_button=self.driver.find_element_by_xpath("//button[@type='submit'][@name='Approve']").click()

  def deleteAdvertisment(self):
    row=self.findAdvertisment()
    if row:
      delete_buuton=row.find_element_by_xpath('//img[@name="Удалить"]').click()
      time.sleep(random.randint(3,5))
      alert=self.driver.switch_to_alert()
      alert.accept()

  def findAdvertisment(self):
    self.driver.get('http://oo.by/browse_listings.php')
    table_with_vertisment=self.driver.find_element_by_tag_name('table')
    rows=table_with_vertisment.find_elements_by_tag_name('tr')
    for row in rows:
      cells=row.find_elements_by_tag_name('td')
      for cell in cells:
        if self.advertisment.title in cell.text:
          return row
  
  def editAdvertismentText(self):
    row=self.findAdvertisment()
    if row:
      cells=row.find_elements_by_tag_name('td')
      edit_button=row.find_element_by_xpath('//img[@name="Редактировать объявление"]').click()
      time.sleep(random.randint(3,5))
      self.fillAdvertismentInputs()
      submit_button=self.driver.find_element_by_xpath("//button[@type='submit'][@name='Submit']").click()

  def editAdvertismentImages(self):
    row=self.findAdvertisment()
    if row:
      cells=row.find_elements_by_tag_name('td')
      edit_button=row.find_element_by_xpath('//img[@name="Редактировать фотографии"]').click()
      self.deleteOldImages()
      self.addImages()

  def viewAds(self):
    self.driver.get('http://oo.by/useraccount.php')
    time.sleep(random.randint(3,5))
    self.driver.get('http://oo.by/browse_listings.php')
    time.sleep(random.randint(3,5))

  def deleteOldImages(self):
    delete_buttons=self.driver.find_elements_by_class_name('delete')
    for button in delete_buttons:
      button.click()

  def addImages(self):
    for image in self.advertisment.images:
      time.sleep(random.randint(1,3))
      add_file_button=self.driver.find_element_by_xpath('//input[@type="file"][@id="myUploadFile"]')
      add_file_button.clear()
      add_file_button.send_keys(os.path.abspath(image))

  def fillAdvertismentInputs(self):
    title_input=self.driver.find_element_by_name('title')
    title_input.clear()
    title_input.send_keys(self.advertisment.title)

    time.sleep(2)
    text_input=self.driver.find_element_by_xpath('//textarea[@name="description"]')
    text_input.clear()
    text_input.send_keys(self.advertisment.description)

    time.sleep(2)
    price_input=self.driver.find_element_by_xpath('//input[@name="price"]')
    price_input.clear()
    price_input.send_keys(self.advertisment.price)

    price_currency = self.driver.find_element_by_xpath("//select[@name='currency']/option[text()='BYN']").click()     
    time.sleep(2)

    region= self.driver.find_element_by_xpath("//select[@name='region']/option[contains(text(),'"+self.advertisment.location.city+"')]").click()
    time.sleep(2)

    city=self.driver.find_element_by_xpath("//select[@name='city']/option[text()='"+self.advertisment.location.city+"']").click()   
    time.sleep(2)

    type_of_advertisment=self.driver.find_element_by_xpath("//select[@name='adstype']/option[text()='Предложение']").click()
    time.sleep(2)

    animalgroup=self.driver.find_element_by_xpath("//select[@name='animalgroup1']/option[text()='Кошки']").click()
    time.sleep(2)

    select_breed = self.driver.find_element_by_xpath("//select[@name='animalgroup2']/option[text()='Без породы']").click()     
    time.sleep(2)
    

if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment
    
    oo = OO_Bot(user,advertisment)
    #oo.saveCookies()
    oo.loginWithCookies()
    #oo.login()
    oo.viewAds()
    oo.deleteAdvertisment()
    oo.addAdvertisment()
    oo.closeBrowser()