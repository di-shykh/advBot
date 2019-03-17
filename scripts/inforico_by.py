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

username = "di49"
email="*****" #убрала,чтобы не светить ящик и пароль
password = "*****" #убрала,чтобы не светить ящик и пароль

path_to_cookies=os.path.join('cookies','cookies_inforico_by.pkl')

try:
  driver = webdriver.Chrome('chromedriver.exe') if webdriver.Chrome('chromedriver.exe') else webdriver.Chrome('chromedriver')
except Exception:
  print('some error')
class Account:
  def __init__(self,username,password,email):
    self.username=username
    self.password=password
    self.email=email

class Inforico_Bot:

  def __init__(self,user,advertisment):
    self.user=user
    self.advertisment=advertisment
    self.driver=webdriver.Chrome()

  def closeBrowser(self):
    self.driver.close()
  
  def login(self):
    driver=self.driver

    '''executor_url = driver.command_executor._url
    session_id = driver.session_id

    print (session_id)
    print (executor_url)'''

    driver.get('http://inforico.by/my/')

    '''def create_driver_session(session_id, executor_url):
      from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

      # Save the original function, so we can revert our patch
      org_command_execute = RemoteWebDriver.execute

      def new_command_execute(self, command, params=None):
          if command == "newSession":
              # Mock the response
              return {'success': 0, 'value': None, 'sessionId': session_id}
          else:
              return org_command_execute(self, command, params)

      # Patch the function before creating the driver object
      RemoteWebDriver.execute = new_command_execute

      new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
      new_driver.session_id = session_id

      # Replace the patched function with original function
      RemoteWebDriver.execute = org_command_execute

      return new_driver

    driver2 = create_driver_session(session_id, executor_url)
    print (driver2.current_url)'''

    time.sleep(random.randint(1,5))
    email_input=driver.find_element_by_xpath('//input[@name="email"]')
    email_input.clear()
    email_input.send_keys(self.user.email)
    time.sleep(random.randint(1,3))
    password_input=driver.find_element_by_xpath('//input[@name="password"]')
    password_input.clear()
    password_input.send_keys(self.user.password)
    time.sleep(random.randint(1,3))
    checkbox_remember_me=driver.find_element_by_xpath('//input[@type="checkbox"][@name="remember"]')
    if not checkbox_remember_me.is_selected():
      checkbox_remember_me.click()
    time.sleep(random.randint(1,3))
    button_enter=driver.find_element_by_xpath('//input[@type="submit"]')
    #passworword_elem.send_keys(Keys.RETURN)
    time.sleep(random.randint(2,5))
    button_enter.click()

  def addAdvertisment(self):
    #тут все хорошо,только после добавления нужно по ссылке в письме переходить,если руками логиниться,то не нужно почту проверять и т.п.,объявление появляется сразу
    driver=self.driver
    driver.get('http://inforico.by/add/')

    time.sleep(random.randint(1,5))
    title_input=driver.find_element_by_xpath('//input[@name="ad[main][title]"]')
    title_input.clear()
    title_input.send_keys(self.advertisment.title)

    time.sleep(1)
    text_input=driver.find_element_by_xpath('//textarea[@name="ad[main][text]"]')
    text_input.clear()
    text_input.send_keys(self.advertisment.description)

    price_input=driver.find_element_by_xpath('//input[@name="ad[main][price]"]')
    price_input.clear()
    price_input.send_keys(self.advertisment.price)

    #add images to adv
    for image in self.advertisment.images:

      time.sleep(random.randint(1,3))
      add_file_button=driver.find_element_by_xpath('//input[@type="file"][@name="new-image"]')
      add_file_button.clear()
      
      image_for_linux_windows=os.path.join('images','tomas',image)
      add_file_button.send_keys(os.path.abspath(image_for_linux_windows))
      while True:
        error_picture=None
        try:
          error_picture=WebDriverWait(driver, 5).until( \
          EC.presence_of_element_located((By.CSS_SELECTOR, "div[style*='url(\"http://img.inforico.com.ua/d2/img-failed.png\")']")))
        except  NoSuchElementException as exception:
          print("Element not found and test failed")
        finally:
          if error_picture:
            del_button=error_picture.find_element_by_class_name('avf-uimg-del').click()
            error_picture=None
            add_file_button=driver.find_element_by_xpath('//input[@type="file"][@name="new-image"]')
            add_file_button.clear()
            add_file_button.send_keys(os.path.abspath(image_for_linux_windows))
          else:
            break
    
    select_region = driver.find_element_by_id('geo_l1')
    for option in select_region.find_elements_by_tag_name('option'):
      if option.text == self.advertisment.location.region:
          option.click() 
          break
    time.sleep(2)
    select_city = driver.find_element_by_id('geo_l2')
    for option in select_city.find_elements_by_tag_name('option'):
      if option.text == self.advertisment.location.city:
          option.click() 
          break
    time.sleep(random.randint(1,5))
    select_time = driver.find_element_by_name('ad[main][period]')
    for option in select_time.find_elements_by_tag_name('option'):
      if option.text == '6 месяцев':
          option.click() 
          break

    time.sleep(random.randint(1,5))
    checkbox=driver.find_element_by_xpath('//input[@name="ad[main][terms-agree]"][@type="checkbox"]')
    if not checkbox.is_selected():
      checkbox.click()

    time.sleep(random.randint(1,5))
    radio=driver.find_element_by_xpath('//label/input[@name="ad[main][e_company]"][@type="radio"][@value="0"]').click()
    name='Ирина'
    phone='+375-29-676-85-00'

    name_input=driver.find_element_by_xpath('//input[@name="ad[main][name]"]').send_keys(name)
    time.sleep(random.randint(2,5))
    phone_input=driver.find_element_by_xpath('//input[@name="ad[main][tel_1]"]').send_keys(phone)
    time.sleep(random.randint(2,5))
    email_input=driver.find_element_by_name('ad[main][email]').send_keys(self.user.email)

    time.sleep(random.randint(2,5))
    continue_button=driver.find_element_by_xpath('//input[@type="submit"][@value="продолжить"]').click()

    time.sleep(2)
    chenge_category=driver.find_element_by_xpath('//a[text() = "выбрать другую рубрику"]').click()
    category=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//span[contains(.,"'+self.advertisment.category+'")]'))).click()
    section=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//span[contains(.,"'+self.advertisment.section+'")]'))).click()
    time.sleep(2)
    select_type_of_adv = driver.find_element_by_xpath("//select[@name='ad[main][type]']/option[text()='отдам']").click()
    time.sleep(2) 
    select_breed = driver.find_element_by_xpath("//select[@name='ad[vals][cat_breed]']/option[text()='Обычная']").click()     
    time.sleep(2)
    save_button=driver.find_element_by_xpath('//input[@type="submit"][@value="сохранить"]').click()

    #нужно проверять почту и переходить по ссылке,чтобы опубликовать объявление

  def deleteAdvertisment(self):
    #не работает,после входа не могу перейти к списку объявлений(т.е. сразу после авторизации попадаю на 'http://inforico.by/', при переходе на  'http://inforico.by/my/' выкидывает снова окно авторизации )

    isAdvertismentFound=False
    foundedAdvertisment=None

    #self.loginWithCookies()
    driver=self.driver
    #driver.get('http://inforico.by/add/')

    time.sleep(random.randint(1,5))
    driver.get('http://inforico.by/my/')
    advertisment_div=driver.find_elements_by_class_name('alvi-info')
    print(advertisment_div)
    for advertisment in advertisment_div:
      print(advertisment.find_element_by_css_selector('div.alvi-title>a').text)

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
    driver.get('http://inforico.by/')
    #get cookies from dump
    cookies = pickle.load(open(path_to_cookies,"rb"))
    driver.delete_all_cookies()#delete old cookes from browser
    for cookie in cookies:
      driver.add_cookie(cookie)
    time.sleep(3)
    driver.get('http://inforico.by/my/')

if __name__ == "__main__":

    user=Account(username,password,email)
    location=shared_data.location
    advertisment=shared_data.advertisment

    inforico = Inforico_Bot(user,advertisment)
    inforico.login()
    #inforico.getCookies() #Cookies сохраняются в файле
    #inforico.loginWithCookies() #Отрабатывает без ошибок,но авторизация не работает
    #inforico.addAdvertisment() #Работает вроде как хорошо
    inforico.deleteAdvertisment() #Не могу перейти к списку объявлений, выкидывает окно авторизации