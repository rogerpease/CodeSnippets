#!/usr/bin/python3.6 
from PIL import Image, ImageDraw, ImageFont
import os
import sys


#
# Simple Script to make JPG files containing words. 
#

if not os.path.isdir("./images/"):
  os.system("mkdir images")
  

imageWidth  = 250 
imageHeight = 250 

font = ImageFont.truetype("/usr/local/lib/python3.6/dist-packages/pygame/freesansbold.ttf", 48)


#
# Draw the numbers 1 to 10 
#
for x in ['Dog','Bear','Tiger','Fish','Coffee','Coal','Eye','Lamp','Cup','Run']: 
  img = Image.new('RGB', (imageWidth,imageHeight),(255,255,255)); 
  # https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil
  draw = ImageDraw.Draw(img)
  
  messageSizeX, messageSizeY = font.getsize(str(x)) # Figure out the size of our text so we can center properly. 
  draw.text(((imageWidth-messageSizeX)/2, (imageHeight-messageSizeY)/2),str(x),(0,0,0),font=font)
  img.save("images/Word"+str(x)+'.jpg')

print ("Made Images in images subdir!")
