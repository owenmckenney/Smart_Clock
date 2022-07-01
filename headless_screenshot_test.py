import time
from pyvirtualdisplay import Display
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

display = Display(visible=0, size=(480, 280))
display.start()

options = Options()
options.add_argument("--headless")
options.BinaryLocation = "/usr/bin/chromium-browser"
driver_path = "/usr/bin/chromedriver"

driver = webdriver.Chrome(options=options, service=Service(driver_path))
driver.get("https://www.google.com")
print("site opened")
time.sleep(3)
driver.save_screenshot('screenshot1.png')
print("screenshot taken")
driver.close()




