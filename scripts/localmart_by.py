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

path_to_cookies=os.path.join('scripts/cookies','cookies_localmart_by.pkl')

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

class Localmart_Bot:
  def __init__(self,user,advertisment):
    self.user=user
    self.advertisment=advertisment
    self.driver=webdriver.Chrome()

  def closeBrowser(self):
    self.driver.quit()
  
  def login(self):
    self.driver.get('http://localmart.by/')
    time.sleep(random.randint(1,3))
    self.driver.get('http://localmart.by/login')

    time.sleep(random.randint(1,3))
    email_input=self.driver.find_element_by_xpath('//input[@id="LoginForm_email"]')
    email_input.clear()
    email_input.send_keys(self.user.email)

    time.sleep(random.randint(1,3))
    password_input=self.driver.find_element_by_xpath('//input[@type="password"][@id="LoginForm_password"]')
    password_input.clear()
    password_input.send_keys(self.user.password)

    time.sleep(random.randint(1,3))
    rememberMe_input=self.driver.find_element_by_xpath('//input[@type="checkbox"][@id="LoginForm_rememberMe"]')
    if not rememberMe_input.is_selected():
      rememberMe_input.click()
    
    time.sleep(random.randint(1,3))
    button_enter=self.driver.find_element_by_xpath('//a[text()="Войти"][@id="yt0"]')
    time.sleep(random.randint(2,5))
    button_enter.click()

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
      self.driver.add_cookie(cookie)
    time.sleep(3)
    self.driver.get('http://localmart.by/cabinet/items')

  def addAdvertisment(self):
    #self.driver.get('http://localmart.by/add')
    link_to_add_adv=self.driver.find_element_by_xpath("//a[@href='http://localmart.by/add'][text()='Подать объявление']").click()
    time.sleep(random.randint(1,3))
    self.fillInputs()
    self.addImages()
    time.sleep(random.randint(3,5))
    button_add_advertisment=self.driver.find_element_by_xpath("//a[text()='Разместить объявление']").click()

  def fillInputs(self):
    rows=self.driver.find_elements_by_xpath("//form/table/tbody/tr")

    title_input=rows[0].find_element_by_xpath(".//input[@id='Ad_title']")
    title_input.clear()
    title_input.send_keys(self.advertisment.title)

    time.sleep(random.randint(1,3))
    row=rows[1]
    link_select_category=row.find_element_by_xpath(".//a[text()='Выбрать']").click()

    time.sleep(random.randint(1,3))
    category=row.find_element_by_xpath(".//input[@class='category_name input-text type-login suggest-toggle aka-dropdown-input ui-autocomplete-input'][@type='text']")
    category.clear()
    category.send_keys(self.advertisment.category)
    popup_category=row.find_element_by_xpath(".//a[text()='"+self.advertisment.category+"']").click()

    while True:
      try:
        self.fillInputsForSectionPriceBreed()
        break
      except:
        print('Some error.Try again')

    time.sleep(random.randint(1,3))
    phone_input=self.driver.find_element_by_xpath("//input[@id='Ad_phones_0'][@type='text']")
    phone_input.clear()
    phone_input.send_keys(shared_data.contact.contact_phone)

    time.sleep(random.randint(1,3))
    description_input=self.driver.find_element_by_xpath("//textarea[@id='Ad_description']")
    description_input.clear()
    description_input.send_keys(self.advertisment.description+'\n'+shared_data.contact.place+'\n'+shared_data.contact.contact_name+':'+'\n'+shared_data.contact.contact_phone)

    time.sleep(random.randint(2,5))

    input_to_select_region=self.driver.find_element_by_xpath("//input[@id='region_name'][@type='text']").click()
    time.sleep(1)
    region_input=self.driver.find_element_by_xpath("//a[contains(.,'"+self.advertisment.location.region+"')]").click()

    time.sleep(random.randint(1,3))
    input_to_select_city=self.driver.find_element_by_xpath("//input[@id='city_name'][@type='text']").click()
    time.sleep(1)
    #region_input=self.driver.find_element_by_xpath("//a[text()='"+self.advertisment.location.city+"']").click()
    self.driver.execute_script("document.getElementById('city_name').value='"+self.advertisment.location.city+"';")
    try:
      self.driver.execute_script("document.getElementById('ui-id-6').style.display='none';")
    except:
      print("It wasn't any popup elements")


    time.sleep(random.randint(1,3))
    contact_name_input=self.driver.find_element_by_xpath("//input[@id='Ad_username'][@type='text']")
    contact_name_input.clear()
    contact_name_input.send_keys(shared_data.contact.contact_name)

    time.sleep(random.randint(1,3))
    user_type_input=self.driver.find_element_by_xpath("//input[@id='user_type_name'][@type='text']").click()
    time.sleep(1)
    user_type_link=self.driver.find_element_by_xpath("//a[text()='Владелец']").click()

  def fillInputsForSectionPriceBreed(self):
    time.sleep(random.randint(1,3))
    rows=self.driver.find_elements_by_xpath("//form/table/tbody/tr")
  
    row_level2=rows[2]
    link_select_section=row_level2.find_element_by_xpath(".//a[text()='Выбрать']")

    time.sleep(random.randint(1,3))
    section=rows[2].find_element_by_xpath(".//input[@type='text']")
    section.clear()
    section.send_keys(self.advertisment.section)
 
    time.sleep(random.randint(1,3))
    popup_section=rows[2].find_element_by_xpath(".//a[text()='"+self.advertisment.section+"']")
    popup_section.click() 

    section=rows[2].find_element_by_xpath(".//input[@type='text']").click()
    time.sleep(1)
    popup_section=rows[2].find_element_by_xpath(".//a[text()='"+self.advertisment.section+"']") 
    popup_section.click()

    #sometimes falls here(need to check if element //input[@type='radio'][@id='price_free'] is on the page)
    time.sleep(random.randint(1,3))
    if self.advertisment.price==0:
      free_input=self.driver.find_element_by_xpath("//input[@type='radio'][@id='price_free']").click()
    else:
      price_radio_input=self.driver.find_element_by_xpath("//input[@type='radio'][@id='CategoryField_fields_price']").click()
      price_input=self.driver.find_element_by_xpath("//input[@id='CategoryField_fields_1'][@type='text']")
      price_input.clear()
      price_input.send_keys(str(self.advertisment.price))

    time.sleep(random.randint(1,3))
    link_select_breed=self.driver.find_element_by_xpath("//input[@field='fields[32]']").click()
    time.sleep(random.randint(1,3))
    breed=self.driver.find_element_by_xpath("//li[@class='ui-menu-item']/a[text()='Другая']").click()


  def addImages(self):
    for image in self.advertisment.images:
      time.sleep(random.randint(1,3))
      #button_add_file=self.driver.find_element_by_xpath("//span[@class='browse'][text()='Загрузить фотографии']").click()
      self.driver.execute_script("document.getElementById('upload_form_container').style.left='0';")
      self.driver.execute_script("document.getElementById('upload_images').style.opacity='1';")
      self.driver.execute_script("document.getElementById('upload_images').style.margin='0 auto';")
      add_file_button=self.driver.find_element_by_xpath("//input[@type='file']")
      add_file_button.clear()
      add_file_button.send_keys(os.path.abspath(image))

  def viewAds(self):
    self.driver.get("http://localmart.by/cabinet/items")

  def findAdvertisment(self):
    self.viewAds()
    table_with_advertisment=self.driver.find_element_by_tag_name('table')
    rows=table_with_advertisment.find_elements_by_tag_name('tr')
    for row in rows:
      cells=row.find_elements_by_tag_name('td')
      for cell in cells:
        if self.advertisment.title in cell.text:
          return row

  def raiseAdvertisment(self):
    if self.openAdvertisment():
      time.sleep(random.randint(3,5))
      submit_button=self.driver.find_element_by_xpath("//a[text()='Разместить объявление']").click()

  def openAdvertisment(self):
    row_with_advertisment=self.findAdvertisment()
    if row_with_advertisment:
      select_link=row_with_advertisment.find_element_by_xpath(".//a[text()='Выберите']").click()
      time.sleep(1)
      edit_link=row_with_advertisment.find_element_by_xpath(".//a[text()='Редактировать']").click()
      return True
    else:
      return False

  def deleteOldImages(self):
    div_with_photo=self.driver.find_element_by_xpath("//div[@id='photos']")
    links_to_del_photo=div_with_photo.find_elements_by_xpath(".//a[@class='delete']")
    for link in links_to_del_photo:
      self.driver.execute_script("arguments[0].style.visibility='visible'",link)
      link.click()

  def editAdvertisment(self):
    if self.openAdvertisment():
      #self.fillInputs()
      self.deleteOldImages()
      self.addImages()
      time.sleep(random.randint(3,5))
      submit_button=self.driver.find_element_by_xpath("//a[text()='Разместить объявление']").click()

  def deleteAdvertisment(self):
    row_with_advertisment=self.findAdvertisment()
    if row_with_advertisment:
      select_link=row_with_advertisment.find_element_by_xpath(".//a[text()='Выберите']").click()
      time.sleep(1)
      delete_link=row_with_advertisment.find_element_by_xpath(".//a[text()='Удалить']").click()
      time.sleep(random.randint(1,3))
      confirm_popup=self.driver.find_element_by_xpath("//div[@id='confirmDelete']")
      confirm_delete_button=confirm_popup.find_element_by_xpath(".//a[text()='Да, удаляю']").click()


if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment
    
    localmart = Localmart_Bot(user,advertisment)
    localmart.loginWithCookies()#без ввода логина и пароля не пускает даже с сохраненными кукисами
    #localmart.raiseAdvertisment()
    #localmart.editAdvertisment()
    #localmart.viewAds()
    #localmart.deleteAdvertisment()
    localmart.addAdvertisment()
    time.sleep(10)
    localmart.closeBrowser()