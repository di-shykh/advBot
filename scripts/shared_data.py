import glob, os
from pathlib import Path

category='Животные, растения'
section='Кошки, котята'
title='Озорной котик Томас ищет дом'
description="""Один хороший ребёнок ищет себе родителей!
        Томас - озорной и игривый сорванец, как все мальчишки-ребятишки! Играть обожает безумно, но если хозяин устал, то можно и коленки помять, помурчать. 
        Котик нежный, ласковый, мурчащий. В общем, крутой до невозможности! 
        Идеально подходит вторым котом или в семью с активными детишками! 

        Котику около 1 годика , кастрирован и хорошо воспитан.
         
        Если будут возникать вопросы, всегда готова помочь с консультацией. 
        Могу помочь с доставкой. 

        """
short_description='Хороший котик Томас ищет дом'
price=0
bargain=False
contact_name='Ирина'
contact_phone='+37529-676-85-00'
place='Минск, ст.м. Пушкинская'
age=1.5
age_y='лет'

city="Минск"
region="Минск и область"

images=[]
#find all images file in folder and add its path to array
#images_folder=os.path.join('images','tomas')
images_folder = Path("images/tomas/")
'''os.chdir(images_folder)
for file in glob.glob("*.jpg"):
    images.append(file)'''
try:
  for file in os.listdir(images_folder):
    if file.endswith(".jpg"):
      images.append(os.path.join(images_folder, file))
except FileNotFoundError:
  print('problem with path to image in Win')


class Location:
  def __init__(self,city,region):
    self.city=city
    self.region=region

class Contact:
  def __init__(self,contact_name,contact_phone,place):
    self.contact_name=contact_name
    self.contact_phone=contact_phone
    self.place=place

class Advertisment:
  def __init__(self,category,section,title,location,description,short_description,price,bargain,images,age,age_y):
    self.category=category
    self.section=section
    self.title=title
    self.location=location
    self.description=description
    self.short_description=short_description
    self.price=price
    self.bargain=bargain
    self.images=images
    self.age=age
    self.age_y=age_y

location=Location(city,region)
contact=Contact(contact_name,contact_phone,place)
advertisment=Advertisment(category,section,title,location,description,short_description,price,bargain,images,age,age_y)
