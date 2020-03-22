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

path_to_cookies=os.path.join('scripts/cookies','cookies_doska_by.pkl')

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

class Doska_Bot:
  def __init__(self,user,advertisment):
    self.user=user
    self.advertisment=advertisment
    self.driver=webdriver.Chrome()

  def closeBrowser(self):
    self.driver.quit()

  def login(self):
    self.driver.get('https://www.doska.by/login/')

    time.sleep(random.randint(1,3))
    email_input=self.driver.find_element_by_xpath('//input[@name="login"][@id="login_txt"]')
    email_input.clear()
    email_input.send_keys(self.user.email)

    time.sleep(random.randint(1,3))
    password_input=self.driver.find_element_by_xpath('//input[@type="password"][@name="passwd"][@id="pass_txt"]')
    password_input.clear()
    password_input.send_keys(self.user.password)

    time.sleep(random.randint(1,3))
    savepass_input=self.driver.find_element_by_xpath('//input[@type="checkbox"][@name="savepass"][@id="savepass"]')
    if not savepass_input.is_selected():
      savepass_input.click()

    time.sleep(random.randint(1,3))
    button_enter=self.driver.find_element_by_xpath('//input[@type="submit"][@name="blogin"][@value="Войти"]')
    time.sleep(random.randint(2,5))
    button_enter.click()

  def saveCookies(self):
    self.login()
    #cookies dump
    pickle.dump( self.driver.get_cookies() , open(path_to_cookies,"wb"))
    #driver.close()

  def loginWithCookies(self):
    self.driver.get('https://www.doska.by/')
    #get cookies from dump
    cookies = pickle.load(open(path_to_cookies,"rb"))
    self.driver.delete_all_cookies()#delete old cookes from browser
    for cookie in cookies:
      if 'expiry' in cookie:
        del cookie['expiry']
      self.driver.add_cookie(cookie)
    time.sleep(3)
    self.driver.get('https://www.doska.by/my-ads/')

  def select_mode(self):
    time.sleep(random.randint(2,5))
    label=self.driver.find_element_by_xpath("//label[text()='Разрешить с любого компьютера']").click()
    buttton_change=self.driver.find_element_by_xpath('//input[@type="button"][@value="Изменить"]').click()

  def viewAds(self):
    self.driver.get('https://www.doska.by/my-ads/')

  def addAdvertisment(self):
    button_add_advertisment=self.driver.find_element_by_xpath("//button[text()='Подать новое обьявление']").click()

    time.sleep(random.randint(1,3))
    group=self.driver.find_element_by_xpath("//label[text()='Животные']").click()

    time.sleep(random.randint(2,3))
    section=self.driver.find_element_by_xpath("//label[contains(.,'"+self.advertisment.section+"')]").click()

    time.sleep(random.randint(2,3))
    select_breed = self.driver.find_element_by_xpath("//select[@name='cid_2'][@class='new_ad_select']/option[text()='Беспородная']").click()

    time.sleep(random.randint(1,3))
    next_button=self.driver.find_element_by_xpath('//input[@type="button"][@value="Продолжить >>"]').click()

    time.sleep(random.randint(2,3))
    adv_section=self.driver.find_element_by_xpath("//select[@name='sid'][@id='ad_section_id']/option[text()='Продаю']").click()

    time.sleep(random.randint(2,3))
    age=self.driver.find_element_by_xpath("//input[@type='text'][@id='opt[1276]']")
    age.clear()
    age.send_keys(str(self.advertisment.age))
    age_y=self.driver.find_element_by_xpath("//select[@name='currency_price[1276]']/option[text()='"+self.advertisment.age_y+"']").click()

    time.sleep(random.randint(2,3))
    price=self.driver.find_element_by_xpath("//input[@type='text'][@id='opt[8]']")
    price.clear()
    price.send_keys(self.advertisment.price)
    currency=self.driver.find_element_by_xpath("//select[@name='currency_price[8]'][@id='currency_price_8']/option[text()='бр.']").click()

    time.sleep(random.randint(2,3))
    text_input=self.driver.find_element_by_xpath('//textarea[@name="mtxt"]')
    text_input.clear()
    text_input.send_keys(self.advertisment.description)

    self.addImages()

    time.sleep(random.randint(2,3))
    city = self.driver.find_element_by_xpath("//select[@name='region']/option[text()='"+self.advertisment.location.city+"']").click()
    city_region= self.driver.find_element_by_xpath("//select[@name='region_town']/option[text()='Кунцевщина']").click()#убрать текст из кода

    time.sleep(random.randint(2,3))
    phone1=self.driver.find_element_by_xpath("//input[@type='tel'][@name='tel1']")
    if not phone1.get_attribute('value'):
      phone1.clear()
      phone1.send_keys(shared_data.contact_phone)

    time.sleep(random.randint(2,3))
    phone2=self.driver.find_element_by_xpath("//input[@type='tel'][@name='tel2']")
    if not phone2.get_attribute('value'):
      phone2.clear()
      phone2.send_keys(shared_data.contact_phone)

    time.sleep(random.randint(2,3))
    email_input=self.driver.find_element_by_xpath("//input[@type='email']")
    if not email_input.get_attribute('value'):
      email_input.clear()
      email_input.send_keys(self.user.email)

    time.sleep(random.randint(2,5))
    button_publish=self.driver.find_element_by_xpath("//input[@type='button'][@value='Опубликовать объявление']")
    button_publish.click()

    time.sleep(random.randint(2,3))
    self.closeAlert()

    time.sleep(random.randint(2,3))
    price.clear()
    if self.advertisment.price==0:
      price.send_keys(str(self.advertisment.price+1.0))

    time.sleep(random.randint(2,5))
    button_publish.click()

  def closeAlert(self):
    try:
        alert=self.driver.find_element_by_xpath("//div[@id='alert_dv']")
        if alert:
          ok_button=alert.find_element_by_xpath("//a[@id='alert_ok']").click()
    except NoSuchElementException:
      return None

  def addImages(self):
    add_file_buttons=self.driver.find_elements_by_xpath('//input[@type="file"]')
    i=0
    for add_file_button in add_file_buttons:
      if i<len(self.advertisment.images):
        time.sleep(random.randint(1,3))
        add_file_button.clear()
        add_file_button.send_keys(os.path.abspath(self.advertisment.images[i]))
        i+=1

  def findAdvertisment(self):
    self.driver.get('https://www.doska.by/my-ads/')
    tables_with_advertisments=self.driver.find_elements_by_tag_name('table')

    if len(tables_with_advertisments)>3:
      rows=tables_with_advertisments[3].find_elements_by_tag_name('tr')
      for row in rows:
        cells=row.find_elements_by_tag_name('td')
        for cell in cells:
          if self.removeExtraCharacters(self.advertisment.description[:60]) in cell.text:
            return row
  def removeExtraCharacters(self,string):
    string = string.replace("\r","")
    string = string.replace("\n","")
    string=' '.join(string.split()).strip()
    string= string.replace("!",".")
    return string

  def deleteAdvertisment(self):
    row=self.findAdvertisment()
    if row:
      delete_button=row.find_element_by_xpath("//a[text()='удалить']").click()
      delete_adv=self.driver.find_element_by_xpath("//input[@type='button'][@value='Удалить объявление']").click()

if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment

    doska = Doska_Bot(user,advertisment)
    doska.saveCookies()
    doska.loginWithCookies()
    doska.deleteAdvertisment()
    doska.addAdvertisment()
    doska.viewAds()
    time.sleep(random.randint(3,6))
    doska.closeBrowser()

  # script is ready.sometimes deleteAdvertisment() did't work well,need to do two times