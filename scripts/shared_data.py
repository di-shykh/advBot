import glob, os
from pathlib import Path

category='Животные'# поправить в скриптах категорию(не точное совпадение,а содержит "животные")
section='Кошки'# поправить в скриптах категорию(не точное совпадение,а содержит "кошки")
title='Очаровательный котик Томас ищет дом'
description="""Один хороший ребёнок ищет себе родителей!
        Томас - озорной и игривый сорванец, как все мальчишки-ребятишки! Играть обожает безумно, но если хозяин устал, то можно и коленки помять, помурчать. 
        Котик нежный, ласковый, мурчащий. В общем, крутой до невозможности! 
        Идеально подходит вторым котом или в семью с активными детишками! 

        Котику около 1 годика , кастрирован и хорошо воспитан.
         
        Если будут возникать вопросы, всегда готова помочь с консультацией. 
        Могу помочь с доставкой. 

        """
short_description='Хороший котик Томас ищет дом'
price=0 #убрать из БД запись про торг!
contact_name='Ирина'
contact_phone='+37529-676-85-00'
contact_operator='VELCOM' #posible variants: 'VELCOM', 'МТС', 'Life)'
place='Минск, ст.м. Пушкинская'
age=1.5
age_y='лет'
key_words='кот даром'

city="Минск"
region="Минск"#исправить везде не точное совпадение текста,а содержит...

images=[]
#find all images file in folder and add its path to array
#images_folder=os.path.join('images','tomas')
images_folder = Path("scripts/images/tomas/")
'''os.chdir(images_folder)
for file in glob.glob("*.jpg"):
    images.append(file)'''
for file in os.listdir(images_folder):
  if file.endswith(".jpg"):
    images.append(os.path.join(images_folder, file))

username = "di49di49"
email="*****" #убрала,чтобы не светить ящик и пароль
password = "*****" #убрала,чтобы не светить ящик и пароль


class Location:
  def __init__(self,city,region):
    self.city=city
    self.region=region

class Contact:
  def __init__(self,contact_name,contact_phone,place,contact_operator):
    self.contact_name=contact_name
    self.contact_phone=contact_phone
    self.place=place
    self.contact_operator=contact_operator

class Advertisment:
  def __init__(self,category,section,title,location,description,short_description,price,images,age,age_y,key_words):
    self.category=category
    self.section=section
    self.title=title
    self.location=location
    self.description=description
    self.short_description=short_description
    self.price=price
    self.images=images
    self.age=age
    self.age_y=age_y
    self.key_words=key_words

location=Location(city,region)
contact=Contact(contact_name,contact_phone,place,contact_operator)
advertisment=Advertisment(category,section,title,location,description,short_description,price,images,age,age_y,key_words)
