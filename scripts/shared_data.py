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

        Минск, ст.м. Пушкинская 
        Ирина (029) 676-85-00"""
short_description='Хороший котик Томас ищет дом'
price=0
bargain=False
contact_name='Ирина'
contact_phone='+37529-676-85-00'

city="Минск"
region="Минск и область"

images=[]
#find all images file in folder and add its path to array
#images_folder=os.path.join('images','tomas')
images_folder = Path("images/tomas/")
'''os.chdir(images_folder)
for file in glob.glob("*.jpg"):
    images.append(file)'''
for file in os.listdir(images_folder):
  if file.endswith(".jpg"):
    images.append(os.path.join(images_folder, file))


class Location:
  def __init__(self,city,region):
    self.city=city
    self.region=region

class Advertisment:
  def __init__(self,category,section,title,location,description,short_description,price,bargain,images):
    self.category=category
    self.section=section
    self.title=title
    self.location=location
    self.description=description
    self.short_description=short_description
    self.price=price
    self.bargain=bargain
    self.images=images

location=Location(city,region)
advertisment=Advertisment(category,section,title,location,description,short_description,price,bargain,images)
