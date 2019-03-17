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

import pickle

import shared_data #тут данные пользователя и объявление, которые будут общие для всех сайтов

username = "di49di49"
email="*****" #убрала,чтобы не светить ящик и пароль
password = "******" #убрала,чтобы не светить ящик и пароль

path_to_cookies=os.path.join('cookies','cookies_oo_by.pkl')

try:
  driver = webdriver.Chrome('chromedriver.exe') if webdriver.Chrome('chromedriver.exe') else webdriver.Chrome('chromedriver')
except Exception:
  print('some error')

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
    driver=self.driver
    driver.get('http://oo.by/login.html')

    time.sleep(random.randint(1,3))
    username_input=driver.find_element_by_xpath('//input[@name="username"]')
    username_input.clear()
    username_input.send_keys(self.user.username)

    time.sleep(random.randint(1,3))
    password_input=driver.find_element_by_xpath('//input[@name="password"]')
    password_input.clear()
    password_input.send_keys(self.user.password)
    
    time.sleep(random.randint(1,3))
    button_enter=driver.find_element_by_xpath('//button[@type="submit"][@name="Login"]')
    time.sleep(random.randint(2,5))
    button_enter.click()

  def getCookies(self):
    driver=self.driver
    self.login()
    #cookies dump
    pickle.dump( driver.get_cookies() , open(path_to_cookies,"wb")) 
    #закрываю браузер  - куки в браузере не сохраняются
    #driver.close() 

  def loginWithCookies(self):
    # cookies вроде как сохраняются в браузере(ошибок при выполнении не падает),но это никак не помогает с авторизацией
    driver=self.driver
    driver.get('http://oo.by/')
    #get cookies from dump
    cookies = pickle.load(open(path_to_cookies,"rb"))
    driver.delete_all_cookies()#delete old cookes from browser
    for cookie in cookies:
      driver.add_cookie(cookie)
    time.sleep(3)
    driver.get('http://inforico.by/my/') #http://oo.by/index.php?phpSESSID=c2a2bj1vk302ceh5a51jo5jb87 - это в строке браузера, т.е. нужно выдрать это из cookies

  def addAdvertisment(self):
    driver=self.driver
    driver.get('http://oo.by/newad.php')

    #разобраться какого *** не выбирается категория
    time.sleep(2)
    category_click=driver.find_element_by_xpath('//select[@name="category"]').click()
    category=driver.find_element_by_xpath('//select[@name="category"]')
    for option in category.find_elements_by_tag_name('option'):
      if 'Животные' in option.text:
        option.click() 
        break
    submit_button=driver.find_element_by_xpath("//button[@type='submit'][@name='Choose_categ']").click()

    time.sleep(2)
    title_input=driver.find_element_by_name('title')
    title_input.clear()
    title_input.send_keys(self.advertisment.title)

    time.sleep(2)
    text_input=driver.find_element_by_xpath('//textarea[@name="description"]')
    text_input.clear()
    text_input.send_keys(self.advertisment.description)

    '''time.sleep(2)
    email_input=driver.find_element_by_name('mgm_email')
    email_input.clear()
    email_input.send_keys(self.user.email)'''

    time.sleep(2)
    price_input=driver.find_element_by_xpath('//input[@name="price"]')
    price_input.clear()
    price_input.send_keys(self.advertisment.price)

    price_currency = driver.find_element_by_xpath("//select[@name='currency']/option[text()='BYN']").click()     
    time.sleep(2)

    region= driver.find_element_by_xpath("//select[@name='region']/option[text()='Минская область']").click()  #убрать из кода текст   
    time.sleep(2)

    city=driver.find_element_by_xpath("//select[@name='city']/option[text()='Минск']").click()     #убрать из кода текст
    time.sleep(2)

    type_of_advertisment=driver.find_element_by_xpath("//select[@name='adstype']/option[text()='Предложение']").click()
    time.sleep(2)

    animalgroup=driver.find_element_by_xpath("//select[@name='animalgroup1']/option[text()='Кошки']").click()
    time.sleep(2)

    select_breed = driver.find_element_by_xpath("//select[@name='animalgroup2']/option[text()='Без породы']").click()     
    time.sleep(2)

    '''name_phone_input=driver.find_element_by_xpath('mgm_name')
    name_phone_input.clear()
    name_phone_input.send_keys(shared_data.contact_name+' '+shared_data.contact_phone)
    time.sleep(random.randint(2,5))'''

    next_step_button=driver.find_element_by_xpath("//button[@type='submit'][@name='Submit']").click()

    for image in self.advertisment.images:
      time.sleep(random.randint(1,3))
      add_file_button=driver.find_element_by_xpath('//input[@type="file"][@id="myUploadFile"]')
      add_file_button.clear()
      
      image_for_linux_windows=os.path.join('images','tomas',image)
      add_file_button.send_keys(os.path.abspath(image_for_linux_windows))

if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment
    
    oo = OO_Bot(user,advertisment)
    oo.login()
    oo.addAdvertisment()