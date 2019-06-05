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

path_to_cookies=os.path.join('scripts/cookies','cookies_bu_by.pkl')

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

class Bu_Bot:
  def __init__(self,user,advertisment):
    self.user=user
    self.advertisment=advertisment
    self.driver=webdriver.Chrome()

  def closeBrowser(self):
    self.driver.quit()
  
  def login(self):
    self.driver.get('http://bu.by/user_auth.html?action=login')
    
    time.sleep(random.randint(1,3))
    email_input=self.driver.find_element_by_xpath('//input[@name="email"]')
    email_input.clear()
    email_input.send_keys(self.user.email)

    time.sleep(random.randint(1,3))
    password_input=self.driver.find_element_by_xpath("//input[@type='password'][@name='pswd']")
    password_input.clear()
    password_input.send_keys(self.user.password)
    
    time.sleep(random.randint(1,3))
    button_enter=self.driver.find_element_by_xpath('//input[@type="image"][@src="_img/go.gif"]')
    button_enter.click()

  def saveCookies(self):
    self.login()
    #cookies dump
    pickle.dump( self.driver.get_cookies() , open(path_to_cookies,"wb")) 
    #driver.close() 

  def loginWithCookies(self):
    self.driver.get('http://bu.by/')
    #get cookies from dump
    cookies = pickle.load(open(path_to_cookies,"rb"))
    self.driver.delete_all_cookies()#delete old cookes from browser
    for cookie in cookies:
      self.driver.add_cookie(cookie)
    time.sleep(3)
    self.driver.get('http://bu.by/')

  def viewAds(self):
    self.driver.get('http://bu.by/')
    link_to_ads=self.driver.find_element_by_xpath("//a[text()='Ваши объявления']").click()

  def addAdvertisment(self):
    link_add=self.driver.find_element_by_xpath("//a[text()='Добавить']").click()

    time.sleep(2)
    category=self.driver.find_element_by_xpath("//select[@id='main_cat_id']/option[text()='Животные и растения']").click()#подумать как убрать текст
    time.sleep(2)
    subcategory=self.driver.find_element_by_xpath("//select[@id='sel_cat_135']/option[@value='139_0_1_2']").click() #self.driver.find_element_by_xpath("//select[@id='sel_cat_135']/option[text()='&nbsp; &nbsp; Кошки']").click() переписать!!!
    time.sleep(2)
    
    self.fillInputs()
    self.addImages()

    button_add=self.driver.find_element_by_xpath("//input[@type='button'][@value='Добавить']").click()
    button_save=self.driver.find_element_by_xpath("//input[@type='button'][@value='Сохранить']").click()

  def findAdvertisment(self):
    self.viewAds()
    try:
      link_to_advertisment=self.driver.find_element_by_xpath("//a[text()='"+self.advertisment.title +"']").click()
      return True
    except NoSuchElementException as exception:
      print("Element not found")
      return False

  def editAdvertisment(self):
    isAdvertismentFounded=self.findAdvertisment()
    if isAdvertismentFounded:
      link_to_edit=self.driver.find_element_by_partial_link_text("Изменить объявление").click()
      self.fillInputs()
      self.deleteImages()
      self.addImages()
      time.sleep(random.randint(3,5))
      button_save=self.driver.find_element_by_xpath("//input[@type='button'][@value='Сохранить']").click()


  def fillInputs(self):
    city=self.driver.find_element_by_xpath("//select[@name='e_city_id']/option[text()='"+self.advertisment.location.city+"']").click()
    time.sleep(2)
    adv_type=self.driver.find_element_by_xpath("//select[@name='e_type']/option[text()='Предложение']").click()
    time.sleep(2)
    title_input=self.driver.find_element_by_xpath("//input[@name='e_title']")
    title_input.clear()
    title_input.send_keys(self.advertisment.title)
    time.sleep(random.randint(2,5))
    description_input=self.driver.find_element_by_xpath("//textarea[@name='e_text']")
    description_input.clear()
    description_input.send_keys(self.advertisment.description+'\n'+shared_data.contact.place+'\n'+shared_data.contact.contact_name+':'+'\n'+shared_data.contact.contact_phone)
    time.sleep(random.randint(2,4))
    price_input=self.driver.find_element_by_xpath("//input[@name='e_cost']")
    price_input.clear()
    price_input.send_keys(str(self.advertisment.price))
    currency=self.driver.find_element_by_xpath("//select[@name='e_currency']/option[text()='Бел.рубль [BYN]']").click()

  def addImages(self):
    count=0
    for image in self.advertisment.images:
      time.sleep(random.randint(1,3))
      if count<=5:
        add_file_button=self.driver.find_element_by_xpath('//input[@type="file"][@name="img_files[]"]')
        add_file_button.clear()
        add_file_button.send_keys(os.path.abspath(image))
        count+=1
  
  def deleteImages(self):
    delete_buttons=self.driver.find_elements_by_xpath("//a[@class='icon icon_img_del delete'][@title='Удалить']")
    for delete_button in delete_buttons:
      delete_button.click()
      time.sleep(random.randint(3,5))
      alert=self.driver.switch_to_alert()
      alert.accept()

  def deleteAdvertisment(self):
    isAdvertismentFounded=self.findAdvertisment()
    if isAdvertismentFounded:
      link_to_edit=self.driver.find_element_by_partial_link_text("Удалить объявление").click()
      time.sleep(random.randint(3,5))
      alert=self.driver.switch_to_alert()
      alert.accept()

if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment
    
    bu = Bu_Bot(user,advertisment)
    bu.saveCookies()
    bu.loginWithCookies()
    #bu.editAdvertisment()
    bu.deleteAdvertisment()
    bu.addAdvertisment()
    bu.closeBrowser()
