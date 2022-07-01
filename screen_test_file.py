#!/usr/bin/python3
import sys
sys.path.insert(1, "./lib")
import epd3in7
import time
from PIL import Image,ImageDraw,ImageFont

epd = epd3in7.EPD()
epd.init(0)
epd.Clear(0xFF, 0)

def drawBackground():
    background = Image.new('1', (epd3in7.EPD_HEIGHT, epd3in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(background)
    return background, draw

def printToDisplay(string):
    #background = drawBackground()[0]
    #draw = drawBackground()[1]
    background = Image.new('1', (epd3in7.EPD_HEIGHT, epd3in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('/home/pi/Documents/Smart_Clock/rpi_image_delivery/Roboto-Black.ttf', 30)

    draw.text((25, 65), string, font = font, fill = 0)
    epd.display_4Gray(epd.getbuffer_4Gray(background))

def imageToDisplay(path):
    background = Image.new('1', (epd3in7.EPD_HEIGHT, epd3in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(background)
    pic = Image.open(path)
    background.paste(pic, (0, 0))
    epd.display_4Gray(epd.getbuffer_4Gray(background))
    

#printToDisplay("Owen McKenney")

p = '/home/pi/Documents/Smart_Clock/screenshot1.png'
imageToDisplay(p)



'''
try:
    epd = epd3in7.EPD()
    logging.debug("Initialize screen")
    epd.init(0)
    
    #font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    #font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    #font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    
    if datetime.datetime.now().minute == 0 and datetime.datetime.now().hour == 2:
        logging.debug("Clear screen")
        epd.Clear(0xFF, 0)
    
    filename = sys.argv[1]

    logging.debug("Read image file: " + filename)
    Himage = Image.open(filename)
    logging.info("Display image file on screen")
    epd.display_4Gray(epd.getbuffer_4Gray(Himage))
    epd.sleep()
    #epd.Dev_exit()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd3in7.epdconfig.module_exit()
    exit()
'''
