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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image

def current_time():
    now = datetime.now()
    print(now.strftime("%H:%M:%S"))

def init_selenium():
    options = Options()
    options.add_argument("--headless")
    options.BinaryLocation = "/usr/bin/chromium-browser"
    driver_path = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(options=options, service=Service(driver_path))

    return driver

def new_screenshot():   
    init_selenium()
    
    driver.get("http://192.168.86.103/")

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

def scrape_weather():
    #driver = init_selenium()
    options = Options()
    options.add_argument("--headless")
    options.BinaryLocation = "/usr/bin/chromium-browser"
    driver_path = "/usr/bin/chromedriver"

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    #prefs = {"profile.managed_defualt_content_settings.images": 2}
    #options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options, desired_capabilities=caps, service=Service(driver_path))
    print("driver set up")

    driver.get("https://www.wunderground.com/weather/us/va/charlottesville/22903")

    print("website opened")
    
    #WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cdk-overlay-0"]/snack-bar-container/privacy-toast-view/div/button'))).click()
     
    #

    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inner-content"]/div[3]/div[1]/div/div[1]/div[1]/lib-city-current-conditions/div'))).get_attribute("value")
    
    element = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[3]/div[1]/div/div[1]/div[1]/lib-city-current-conditions/div')

    print("element found")

    driver.execute_script("window.scrollTo(0, 200)")

    print("scrolled")

    element.screenshot("weatherDataUncropped.png")
    driver.close()

    print("screenshot taken, driver closed")

    pic = Image.open("weatherDataUncropped.png")
    width, height = pic.size
    cropped_pic = pic.crop((0, 65, width - 20, height - 85))
    cropped_pic = cropped_pic.save("weatherData.png")


def generate_ss_id():
    ss_id = str(random.randint(0,9)) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
    return "ss" + ss_id + ".png"

if __name__ == '__main__':
   #new_screenshot() 
   scrape_weather()

