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
email='di49@mail.ru'#Нельзя зарегить нового пользователя для тестов.Возможно скоро сайт канет в Лету
password = shared_data.password
dict_for_cities={'Барановичи':'baranovichi','Бобруйск':'bobruysk','Борисов':'borisov','Брест':'brest',
'Витебск':'vitebsk','Волковыск':'volkovysk','Гомель':'gomel','Жлобин':'zhlobin','Жодино':'zhodino','Кобрин':'kobrin',
'Лида':'lida','Минск':'minsk','Могилев':'mogilev','Мозырь':'mozyr','Молодечно':'molodechno','Новополоцк':'novopolock',
'Орша':'orsha','Пинск':'pinsk','Полоцк':'polotsk','Речица':'rechica','Рогачев':'rogachev','Светлогорск':'svetlogorsk',
'Слоним':'slonim','Слуцк':'sluck','Сморгонь':'smorgon','Солигорск':'soligorsk'}

path_to_cookies=os.path.join('scripts/cookies','cookies_ekomissionka_by.pkl')

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

class Ekomissionka_Bot:
  def __init__(self,user,advertisment):
    self.user=user
    self.advertisment=advertisment
    self.driver=webdriver.Chrome()

  def closeBrowser(self):
    self.driver.quit()

  def login(self):
    self.driver.get('http://minsk.ekomissionka.by/ru-i-loginform')

    time.sleep(random.randint(1,3))
    email_input=self.driver.find_element_by_xpath("//input[@name='Login'][@type='text']")
    email_input.clear()
    email_input.send_keys(self.user.email)

    time.sleep(random.randint(1,3))
    password_input=self.driver.find_element_by_xpath("//input[@type='password'][@name='Password']")
    password_input.clear()
    password_input.send_keys(self.user.password)

    time.sleep(random.randint(1,3))
    button_enter=self.driver.find_element_by_xpath("//input[@type='submit'][@value='Вход']").click()

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
    self.driver.get('http://minsk.ekomissionka.by/ru-i-myhome.html')

  def addAdvertisment(self):
    city=dict_for_cities.get(self.advertisment.location.city,'minsk')
    self.driver.get('http://'+city+'.ekomissionka.by/ru-i-add.html')
    time.sleep(random.randint(3,5))
    self.fillInputs()
    self.addImages()
    time.sleep(random.randint(3,5))
    button_check_advertisment=self.driver.find_element_by_xpath("//input[@type='submit'][@value='Проверить объявление']").click()
    time.sleep(random.randint(3,5))
    button_add_advertisment=self.driver.find_element_by_xpath("//input[@type='button'][@value='Опубликовать объявление']").click()

  def fillInputs(self):
    category=self.driver.find_element_by_xpath("//a[contains(.,'"+self.advertisment.category.lower()+"')]").click()
    time.sleep(random.randint(1,3))
    section=self.driver.find_element_by_xpath("//a[contains(.,'"+self.advertisment.section+"')]").click()
    time.sleep(random.randint(1,3))
    #doesn't work!
    '''if self.advertisment.location.city!='Минск':
      link_to_change_city=self.driver.find_element_by_xpath("//a[text()='другой город']").click()
      time.sleep(3)
      popup_div=self.driver.find_element_by_xpath("//div[@id='ChangeLocationAdd']")
      #self.driver.execute_script("arguments[0].style.display='block'",popup_div)
      time.sleep(random.randint(1,3))
      #link_to_city=self.driver.find_element_by_xpath("//a[contains(.,'"+self.advertisment.location.city+"')]").click()
    time.sleep(random.randint(3,5))'''
    adv_type=self.driver.find_element_by_xpath("//select[@name='ResourceOffer_11_ResourceOfferType']/option[text()='Продам, предлагаю - частное лицо']").click()
    time.sleep(random.randint(1,3))
    title_input=self.driver.find_element_by_xpath("//input[@type='text'][@id='ResourceOffer_11_ResourceOfferTitle']")
    title_input.clear()
    title_input.send_keys(self.advertisment.title)
    time.sleep(random.randint(1,3))
    description_input=self.driver.find_element_by_xpath("//textarea[@id='ResourceOffer_11_ResourceOfferContent']")
    description_input.clear()
    description_input.send_keys(self.advertisment.description+'\n'+shared_data.contact.place+'\n'+shared_data.contact.contact_name+':'+'\n'+shared_data.contact.contact_phone)
    time.sleep(random.randint(1,3))
    price_input=self.driver.find_element_by_xpath("//input[@type='text'][@name='ResourceOffer_11_ResourceOfferPrice']")
    price_input.clear()
    price_input.send_keys(str(self.advertisment.price))
    time.sleep(random.randint(1,3))
    currency=self.driver.find_element_by_xpath("//select[@name='ResourceOffer_11_ResourceOfferCurrency']/option[@value='BYR']").click()
    time.sleep(random.randint(1,3))
    key_words_input=self.driver.find_element_by_xpath("//input[@type='text'][@name='ResourceOffer_11_ResourceOfferKeywords']")
    key_words_input.clear()
    key_words_input.send_keys(self.advertisment.key_words)

  def addImages(self):
    for image in self.advertisment.images:
      time.sleep(random.randint(1,3))
      add_file_button=self.driver.find_element_by_xpath("//input[@type='file'][@name='uploadFile[ResourceOfferIcon]']")
      #add_file_button.clear() добавляет фото по 2 одинаковых
      add_file_button.send_keys(os.path.abspath(image))
  
  def viewAds(self):
    self.driver.find_element_by_xpath("//a[text()='Мои объявления']").click()

  def findAdvertisment(self):
    self.viewAds()
    try:
      div_adv=self.driver.find_elements_by_xpath("//div[@class='offer']/h1")
      for div in div_adv:
        if(div.find_element_by_xpath(".//a[contains(.,'"+self.advertisment.title+"')]")):
          return div
    except:
      return False

  def raiseAdvertisment(self):
    if (self.findAdvertisment()):
      row=self.findAdvertisment()
      raise_button=row.find_element_by_xpath(".//a[text()='[Обновить дату]']").click()
  
  def editAdvertisment(self):
    if (self.findAdvertisment()):
      row=self.findAdvertisment()
      raise_button=row.find_element_by_xpath(".//a[text()='[Изменить]']").click()
      section=self.driver.find_element_by_xpath("//select[@name='ResourceOffer_11_ResourceOfferCategoryID']/option[contains(.,'"+self.advertisment.section+"')]").click()
      type_of_advertisment=self.driver.find_element_by_xpath("//select[@name='ResourceOffer_11_ResourceOfferType']/option[@value='ad']").click()
      title_input=self.driver.find_element_by_xpath("//input[@name='ResourceOffer_11_ResourceOfferTitle']")
      title_input.clear()
      title_input.send_keys(self.advertisment.title)
      time.sleep(random.randint(1,3))
      description_input=self.driver.find_element_by_xpath("//textarea[@name='ResourceOffer_11_ResourceOfferContent']")
      description_input.clear()
      description_input.send_keys(self.advertisment.description+'\n'+shared_data.contact.place+'\n'+shared_data.contact.contact_name+':'+'\n'+shared_data.contact.contact_phone)
      time.sleep(random.randint(1,3))
      price_input=self.driver.find_element_by_xpath("//input[@type='text'][@name='ResourceOffer_11_ResourceOfferPrice']")
      price_input.clear()
      price_input.send_keys(str(self.advertisment.price))
      time.sleep(random.randint(1,3))
      currency=self.driver.find_element_by_xpath("//select[@name='ResourceOffer_11_ResourceOfferCurrency']/option[@value='BYR']").click()
      time.sleep(random.randint(1,3))
      try:
        for i in range(self.advertisment.images.__len__()):
          links_delete=self.driver.find_element_by_xpath("//a[contains(.,'Удалить')]").click()
      except:
        print("All element were deleted")
      for image in self.advertisment.images:
        time.sleep(random.randint(1,3))
        add_file_button=self.driver.find_element_by_xpath("//input[@type='file'][@name='uploadFile[FileIcon]']")
        #add_file_button.clear()
        add_file_button.send_keys(os.path.abspath(image))
      time.sleep(random.randint(3,5))
      button_check_advertisment=self.driver.find_element_by_xpath("//input[@type='submit'][@value='Проверить объявление']").click()
      time.sleep(random.randint(3,5))
      button_add_advertisment=self.driver.find_element_by_xpath("//input[@type='button'][@value='Опубликовать объявление']").click()
    '''self.deleteAdvertisment()
    #сразу опубликовать объявление с тем же заголовком нельзя. Попробую утром
    self.addAdvertisment()'''

  def deleteAdvertisment(self):
    if (self.findAdvertisment()):
      row=self.findAdvertisment()
      raise_button=row.find_element_by_xpath(".//a[text()='[Удалить]']").click()
      time.sleep(random.randint(3,5))
      alert=self.driver.switch_to_alert()
      alert.accept()


if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment
    
    ekomissionka = Ekomissionka_Bot(user,advertisment)
    ekomissionka.loginWithCookies()#без ввода логина и пароля не пускает даже с сохраненными кукисами
    ekomissionka.raiseAdvertisment()
    #ekomissionka.editAdvertisment()
    #ekomissionka.deleteAdvertisment()
    #ekomissionka.findAdvertisment()
    #ekomissionka.viewAds()
    #ekomissionka.addAdvertisment()
    ekomissionka.closeBrowser()