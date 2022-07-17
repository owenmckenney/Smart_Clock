import sys
import os
sys.path.insert(1, "./lib")
import epd3in7
import time
from PIL import Image, ImageDraw, ImageFont
from screenshot_functions import new_screenshot

epd = epd3in7.EPD()
epd.init(0)
epd.Clear(0xFF, 0)

def updateDisplay():
    new_screenshot()

    background = Image.new('1', (epd3in7.EPD_HEIGHT, epd3in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(background)
    f = open("current_screenshot.txt", "r+")
    current_ss_id = f.read()[0:9]
    f.close()
    p = '/home/pi/Documents/Smart_Clock/' + str(current_ss_id)
    pic = Image.open(p)
    background.paste(pic, (0,0))
    epd.display_4Gray(epd.getbuffer_4Gray(background))

updateDisplay()

