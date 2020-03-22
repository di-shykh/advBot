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

path_to_cookies=os.path.join('scripts/cookies','cookies_baraholka_onliner_by.pkl')

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

class Onliner_Bot:
  def __init__(self,user,advertisment):
    self.user=user
    self.advertisment=advertisment
    self.driver=webdriver.Chrome()

  def closeBrowser(self):
    self.driver.quit()

  def login(self):
    self.driver.get('https://baraholka.onliner.by/')
    time.sleep(random.randint(1,3)) 
    self.driver.find_element_by_xpath('//div[@class="auth-bar__item auth-bar__item--text"][contains(.,"Вход")]').click()
    time.sleep(random.randint(1,3)) 
    input_username=self.driver.find_element_by_xpath('//input[@type="text"][@placeholder="Ник или e-mail"]')
    input_username.clear()
    input_username.send_keys(self.user.email)
    time.sleep(random.randint(1,3))
    input_password=self.driver.find_element_by_xpath('//input[@type="password"][@placeholder="Пароль"]')
    input_password.clear()
    input_password.send_keys(self.user.password)
    time.sleep(random.randint(2,5))
    submit_button=self.driver.find_element_by_xpath('//button[@type="submit"][contains(.,"Войти")]').click() 

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
    self.driver.get('https://baraholka.onliner.by/')

  def addAdvertisment(self):
    self.driver.find_element_by_xpath('//a[contains(.,"Разместить объявление")]').click() 
    time.sleep(random.randint(1,3))
    self.driver.find_element_by_xpath('//span[contains(.,"Продам")]').click()
    time.sleep(random.randint(1,3))
    #type_of_advertisment=self.driver.find_element_by_xpath("//select[@name='ResourceOffer_11_ResourceOfferType']/option[@value='ad']").click()

if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment
    
    onliner = Onliner_Bot(user,advertisment)
    #onliner.login()
    onliner.loginWithCookies()#без ввода логина и пароля не пускает даже с сохраненными кукисами
    #onliner.raiseAdvertisment()
    #onliner.editAdvertisment()
    #onliner.viewAds()
    #onliner.deleteAdvertisment()
    onliner.addAdvertisment()
    time.sleep(120)
    onliner.closeBrowser()