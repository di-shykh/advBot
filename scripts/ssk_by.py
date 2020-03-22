from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager #for updating webdriver

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

path_to_cookies=os.path.join('scripts/cookies','cookies_ssk_by.pkl')

driver=webdriver.Chrome(ChromeDriverManager().install())

'''if platform == "linux" or platform == "linux2":
 driver=webdriver.Chrome('chromedriver')
elif platform == "darwin":
 driver=webdriver.Chrome('chromedriver_mac')
elif platform == "win32":
  driver = webdriver.Chrome('chromedriver.exe')'''

class Account:
  def __init__(self,username,password,email):
    self.username=username
    self.password=password
    self.email=email

class Ssk_Bot:
  def __init__(self,user,advertisment):
    self.user=user
    self.advertisment=advertisment
    self.driver=webdriver.Chrome()

  def closeBrowser(self):
    self.driver.quit()

  def login(self):
    self.driver.get('https://ssk.by/')
    time.sleep(random.randint(1,3))
    login_link=self.driver.find_element_by_xpath("//a[text()=' Авторизация']").click()
    time.sleep(1)
    login_input=self.driver.find_element_by_xpath("//*[@id='login_name']")
    login_input.clear()
    login_input.send_keys(self.user.username)

    time.sleep(random.randint(1,3))
    password_input=self.driver.find_element_by_xpath("//*[@id='login_password']")
    password_input.clear()
    password_input.send_keys(self.user.password)

    time.sleep(random.randint(1,3))
    enter_button=self.driver.find_element_by_xpath("//button[@title='Войти'][@type='submit']").click()

  def saveCookies(self):
    self.login()
    #cookies dump
    pickle.dump( self.driver.get_cookies() , open(path_to_cookies,"wb"))
    #driver.close()

  def loginWithCookies(self):
    self.saveCookies()
    #get cookies from dump
    cookies = pickle.load(open(path_to_cookies,"rb"))
    self.driver.delete_all_cookies()#delete old cookes from browser
    for cookie in cookies:
      if 'expiry' in cookie:
        del cookie['expiry']
      self.driver.add_cookie(cookie)
    time.sleep(3)
    self.driver.get('https://ssk.by/')

  def addAdvertisment(self):
    link_to_add_advertisment=self.driver.find_element_by_xpath("//a[text()='Добавить объявление']").click()
    self.fillInputs()
    self.addImages()
    time.sleep(random.randint(3,5))
    submit_button=self.driver.find_element_by_xpath("//input[@type='submit'][@value='Подать объявление']").click()
  
  def fillInputs(self):
    title_input=self.driver.find_element_by_xpath("//input[@type='text'][@name='title']")
    title_input.clear()
    title_input.send_keys(self.advertisment.title)

    time.sleep(random.randint(1,3))
    price_input=self.driver.find_element_by_xpath("//input[@type='text'][@name='price']")
    price_input.clear()
    if self.advertisment.price==0:
      price_input.send_keys(str(self.advertisment.price+1))
    else:
      price_input.send_keys(str(self.advertisment.price))

    time.sleep(random.randint(1,3))
    country=self.driver.find_element_by_xpath("//select[@name='country'][@id='SelectListCountryAdd']/option[text()='Беларусь']").click()

    time.sleep(random.randint(1,3))
    city=self.driver.find_element_by_xpath("//select[@name='city'][@id='SelectCityAdd']/option[text()='"+self.advertisment.location.city+"']").click()

    time.sleep(random.randint(1,3))
    type_of_advertisment=self.driver.find_element_by_xpath("//select[@name='board_type'][@id='BoardTypeSelect']/option[text()='Продам']").click()

    time.sleep(random.randint(1,3))
    category=self.driver.find_element_by_xpath("//select[@name='MainCategory'][@id='mainCat']/option[text()='"+self.advertisment.category+"']").click()

    time.sleep(random.randint(1,3))
    section=self.driver.find_element_by_xpath("//select[@name='category'][@id='BoardSelectCategory']/option[text()='"+self.advertisment.section+"']").click()

    time.sleep(random.randint(1,3))
    description_input=self.driver.find_element_by_xpath("//textarea[@name='text'][@id='BoardStory']")
    description_input.clear()
    description_input.send_keys(self.advertisment.description+'\n'+shared_data.contact.place+'\n'+shared_data.contact.contact_name+':'+'\n'+shared_data.contact.contact_phone)

    time.sleep(random.randint(3,5))
    if shared_data.contact_operator=='VELCOM':
      phone_input=self.driver.find_element_by_xpath("//input[@type='text'][@name='field[telefon]'][@id='field_telefon']")
    elif shared_data.contact_operator=='МТС':
      phone_input=self.driver.find_element_by_xpath("//input[@type='text'][@name='field[telefon-mts]'][@id='field_telefon-mts']")
    else:
      phone_input=self.driver.find_element_by_xpath("//input[@type='text'][@name='field[telefon-life]'][@id='field_telefon-life']")
    phone_input.clear()
    phone_input.send_keys(shared_data.contact_phone)

  def addImages(self):
    count=0
    for image in self.advertisment.images:
      time.sleep(random.randint(1,3))
      if count<=50:
        add_file_button=self.driver.find_element_by_xpath('//input[@type="file"][@name="file"]')
        add_file_button.clear()
        add_file_button.send_keys(os.path.abspath(image))
        count+=1

  def viewAds(self):
    link_to_ads=self.driver.find_element_by_xpath("//a[text()='Мои объявления']").click()

  def findAdvertisment(self):
    self.viewAds()
    try:
      blocks_with_advertisment=self.driver.find_elements_by_xpath("//div[@class='BoardMainPost']")
      for block_with_advertisment in blocks_with_advertisment:
        el=block_with_advertisment.find_element_by_xpath(".//h3")
        if el.get_attribute("textContent").strip()==self.advertisment.title[0].upper() + self.advertisment.title[1:].lower():
          return block_with_advertisment
    except NoSuchElementException as exception:
      print("Element not found")
      return False
  
  def editAdvertisment(self):
    self.deleteAdvertisment()
    self.addAdvertisment()
      
  def deleteImages(self):
    delete_buttons=self.driver.find_elements_by_xpath("//div[@class='uploadedfile ui-sortable-handle']/div[@class='info']/a[text()='Удалить']")
    for button in delete_buttons:
      button.click()
      WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='dialog']/button[text()='Да']"))).click()

  def deleteAdvertisment(self):
    advertisment=self.findAdvertisment()
    if advertisment:
      block_of_buttons=advertisment.find_element_by_xpath(".//div[@class='BoardMainPostEdit']")
      delete_button=block_of_buttons.find_element_by_xpath(".//a/strong[text()='Удалить']").click()
      accept_deleting=self.driver.find_element_by_xpath("//input[@type='submit'][@value='Да, удалить']").click()

  def raiseAdvertisment(self):
    advertisment=self.findAdvertisment()
    if advertisment:
      block_of_buttons=advertisment.find_element_by_xpath(".//div[@class='BoardMainPostEdit']")
      raise_button=block_of_buttons.find_element_by_xpath(".//a/strong[text()='Поднять вверх']").click()
      hidden_div=self.driver.find_element_by_xpath("//span[text()='Поднять объявление']/../..")
      self.driver.execute_script("arguments[0].style.display='block'",hidden_div)
      time.sleep(1)
      label_freeup=hidden_div.find_element_by_xpath(".//strong[text()='Поднять объявление бесплатно']/..").click()
      submit_button=hidden_div.find_element_by_xpath(".//input[@type='submit'][@value='Далее']").click()
      close_button=hidden_div.find_element_by_xpath(".//span[text()='close']").click()

if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment
    
    ssk = Ssk_Bot(user,advertisment)
    #ssk.login()
    ssk.loginWithCookies()
    #ssk.addAdvertisment()
    #ssk.editAdvertisment()
    ssk.raiseAdvertisment()
    ssk.closeBrowser()