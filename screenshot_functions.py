import time
#from datetime import datetime
import os
import random
import string
#from pyvirtualdisplay import Display
#from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def current_time():
    now = datetime.now()
    print(now.strftime("%H:%M:%S"))

def new_screenshot():
    
    #display = Display(visible=0, size=(480, 280))
    #display.start()
    options = Options()
    options.add_argument("--headless")
    options.BinaryLocation = "/usr/bin/chromium-browser"
    driver_path = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(options=options, service=Service(driver_path))
    driver.get("http://192.168.86.103/")
    #time.sleep(3)

    f = open("current_screenshot.txt", 'r+')
    old_ss_id = f.read()[0:9]
    #print(old_ss_id)
    f.close()

    os.remove(old_ss_id)
    open("current_screenshot.txt", 'w').close()
    new_ss_id = generate_ss_id()
    f = open("current_screenshot.txt", "r+")
    f.write(new_ss_id)
    f.close()
    driver.save_screenshot(new_ss_id)
    driver.close()

 
def generate_ss_id():
    ss_id = str(random.randint(0,9)) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
    return "ss" + ss_id + ".png"

if __name__ == '__main__':
   new_screenshot() 

