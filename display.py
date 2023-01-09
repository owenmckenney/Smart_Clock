#!/usr/bin/python3
import sys
import json
import random
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
        self.data_draw = ImageDraw.Draw(self.background)
        self.date_width = 0
        self.quote_num = 3

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
        print("driver initialized")
        driver.get("https://www.wunderground.com/weather/us/va/charlottesville/22903")
        print("opened website")
        element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inner-content"]/div[3]/div[1]/div/div[1]/div[1]/lib-city-current-conditions/div'))).get_attribute("value")
        element = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[3]/div[1]/div/div[1]/div[1]/lib-city-current-conditions/div')
        driver.execute_script("window.scrollTo(0, 200)")
        element.screenshot(self.image_path + "weatherData.png")

        print("screenshotted")

        driver.quit()

        pic = Image.open(self.image_path + "weatherData.png").convert("L")
        enhancer = ImageEnhance.Contrast(pic)
        pic = enhancer.enhance(4)
        width, height = pic.size
        
        current_temp = pic.crop((50, 140, width - 200, height - 160))
        current_temp.save(self.image_path + "currentTemp.png")
        self.resize_image("currentTemp.png", 170)
        
        high_low = pic.crop((65, 120, width - 220, height - 245))
        high_low.save(self.image_path + "highLow.png")
        self.resize_image("highLow.png", 100)

        like_temp = pic.crop((70, 215, width - 220, height - 140))
        like_temp.save(self.image_path + "likeTemp.png")
        self.resize_image("likeTemp.png", 100)
        
        weatherImage = pic.crop((235, 60, width - 30, height - 215))
        weatherImage = weatherImage.save(self.image_path + "weatherImage.png")
        self.resize_image("weatherImage.png", 100)
    
    def update_time(self):
        tz = pytz.timezone('America/New_York')
        current_data = datetime.now(tz)
        current_time = current_data.strftime('%H:%M')
        current_date = current_data.strftime('%a, %x')
        
        ip_adress = ''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_adress = s.getsockname()[0]
        s.close()

        date_width = self.data_draw.textsize(current_time, font=self.font_size(100))[0]
        self.date_width = date_width
   
        self.data_draw.text((5, 0), current_time, font=self.font_size(100), fill=0)
        self.data_draw.text((15, 100), current_date, font=self.font_size(38), fill=0)
        self.data_draw.text((0, 270), str(ip_adress), font=self.font_size(10), fill=0)        

        self.data_draw.rectangle((date_width + 14, 0, date_width + 19, 280), fill=0)

    def update_weather(self):
        pic = Image.open(self.image_path + 'currentTemp.png')
        self.background.paste(pic, (300, 20))

        pic = Image.open(self.image_path + 'weatherImage.png')
        self.background.paste(pic, (325, 150))

        pic = Image.open(self.image_path + 'highLow.png')
        self.background.paste(pic, (328, 10))

        pic = Image.open(self.image_path + 'likeTemp.png')
        self.background.paste(pic, (328, 125))

    def get_new_quote(self):
        quote_num = randomt.randint(0, 19)

    def update_quote(self):
        q = open('/home/pi/Documents/Smart_Clock/quotes.json')
        data = json.load(q)
        quote = data["quotes"][self.quote_num]
        q.close()

        font = self.font_size(15)
        
        quote_width = self.data_draw.textsize(quote, font=font)[0]

        if quote_width > self.date_width:
            formatted_quote = self.format_quote(quote, font)
            print(formatted_quote)
            
            for i in range(0, len(formatted_quote)):
                self.data_draw.text((5, 150 + i * 16), formatted_quote[i], font = font, fill=0)
        else:
            self.data_draw.text((5, 150), quote, font=font, fill=0)

    def format_quote(self, quote, font):
        split_quote = list(quote.split(' '))
        author = ' '.join(split_quote[len(split_quote) - 3: len(split_quote)])
        quote = ' '.join(quote.split(' ')[:-3])

        words = list(quote.split(' '))
        lines = []
        cur_pos = 0
        running = True

        while running:
            line = ''

            for i in range(cur_pos, len(words)):
                line += words[i] + ' '
                line_width = self.data_draw.textsize(line, font=font)[0]
                cur_pos = i

                if line_width > self.date_width + 10:
                    line = line[0:len(line) - 1]
                    line = ' '.join(line.split(' ')[:-1])
                    lines.append(line)
                    break
                elif cur_pos == len(words) - 1:
                    line = line[0:len(line) - 1]
                    lines.append(line)
                    running = False
                    break
        
        lines.append(" "*16 + author)
        return lines

    def update_display(self):
        self.epd.display_4Gray(self.epd.getbuffer_4Gray(self.background))
        self.epd.sleep()

    def run(self):
        current_minutes = int(datetime.now().strftime('%M'))
        current_hour = int(datetime.now().strftime('%H'))
        #self.scrape_weather()
        self.update_time()
        self.update_weather()
        self.update_quote()
        self.update_display()

        if current_minutes == 59 or current_minutes == 29:
            print("scraping weather at " + datetime.now().strftime('%H:%M'))
            self.scrape_weather()

        if current_hour == 23 and current_minutes == 59:
            self.get_new_quote()

if __name__ == "__main__":
    d = display()
    d.run()

