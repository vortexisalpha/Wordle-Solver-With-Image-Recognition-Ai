from selenium import webdriver
from PIL import Image
from io import BytesIO
import time

def getImage(driver, element, left, top, name):
   # element = driver.find_element_by_xpath('/html/body/header/div/div[1]/a[2]') # find part of the page you want image of
    
    png = driver.get_screenshot_as_png() # saves screenshot of entire page

    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
    
    right = left+125
    bottom = top+125


    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(str(name) +'.png') # saves new cropped image