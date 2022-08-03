#!/usr/bin/python3
import sys
import socket
sys.path.insert(0, "/home/pi/Documents/Smart_Clock/lib")
import epd3in7
from datetime import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image, ImageEnhance

#480x280

class display:
    
    def __init__(self):
        self.epd = epd3in7.EPD()
        self.epd.init(0)
        self.height = epd3in7.EPD_HEIGHT
        self.width = epd3in7.EPD_HEIGHT
        self.background = Image.new('1', (epd3in7.EPD_HEIGHT, epd3in7.EPD_WIDTH), 255)
        self.image_path = '/home/pi/Documents/Smart_Clock/images/'

    def font_size(self, size):
        return ImageFont.truetype('/home/pi/Documents/Smart_Clock/fonts/Roboto-Black.ttf', size)

    def resize_image(self, image, basewidth):
        img = Image.open(self.image_path + image)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(self.image_path + image)

    def scrape_weather(self):
        options = Options()
        options.add_argument("--headless")
        options.BinaryLocation = "/usr/bin/chromium-browser"
        driver_path = "/usr/bin/chromedriver"
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"

        driver = webdriver.Chrome(options=options, desired_capabilities=caps, service=Service(driver_path))
        driver.get("https://www.wunderground.com/weather/us/va/charlottesville/22903")

        element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inner-content"]/div[3]/div[1]/div/div[1]/div[1]/lib-city-current-conditions/div'))).get_attribute("value")
        element = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[3]/div[1]/div/div[1]/div[1]/lib-city-current-conditions/div')
        driver.execute_script("window.scrollTo(0, 200)")
        element.screenshot("weatherData.png")
        driver.quit()

        pic = Image.open("weatherData.png").convert("L")
        enhancer = ImageEnhance.Contrast(pic)
        pic = enhancer.enhance(4)
        width, height = pic.size
        
        current_temp = pic.crop((50, 140, width - 200, height - 160))
        current_temp.save("currentTemp.png")
        self.resize_image("currentTemp.png", 170)
        
        high_low = pic.crop((65, 120, width - 220, height - 245))
        high_low.save("highLow.png")
        self.resize_image("highLow.png", 100)

        like_temp = pic.crop((70, 215, width - 220, height - 140))
        like_temp.save("likeTemp.png")
        self.resize_image("likeTemp.png", 100)
        
        weatherImage = pic.crop((245, 60, width - 40, height - 215))
        weatherImage = weatherImage.save("weatherImage.png")
        self.resize_image("weatherImage.png", 100)
    
    def update_time(self):
        data_draw = ImageDraw.Draw(self.background)
        tz = pytz.timezone('America/New_York')
        current_data = datetime.now(tz)
        current_time = current_data.strftime('%H:%M')
        current_date = current_data.strftime('%a, %x')
        
        ip_adress = ''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_adress = s.getsockname()[0]
        s.close()

        date_width = data_draw.textsize(current_date, font=self.font_size(40))[0]
   
        data_draw.text((5, 0), current_time, font=self.font_size(100), fill=0)
        data_draw.text((15, 110), current_date, font=self.font_size(38), fill=0)
        data_draw.text((0, 270), str(ip_adress), font=self.font_size(10), fill=0)        

        data_draw.rectangle((date_width + 10, 0, date_width + 15, 280), fill=0)

    def update_weather(self):
        pic = Image.open(self.image_path + 'currentTemp.png')
        self.background.paste(pic, (300, 20))

        pic = Image.open(self.image_path + 'weatherImage.png')
        self.background.paste(pic, (325, 150))

        pic = Image.open(self.image_path + 'highLow.png')
        self.background.paste(pic, (328, 10))

        pic = Image.open(self.image_path + 'likeTemp.png')
        self.background.paste(pic, (328, 125))

    def update_display(self):
        self.epd.display_4Gray(self.epd.getbuffer_4Gray(self.background))
        self.epd.sleep()

    def run(self):
        current_minutes = int(datetime.now().strftime('%M'))
        #self.scrape_weather()
        self.update_time()
        self.update_weather()

        self.update_display()

        if current_minutes == 30 or current_minutes == 0:
            scrape_weather()

if __name__ == "__main__":
    d = display()
    d.run()

