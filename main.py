import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib
import os
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import zxing
from PIL import Image
from io import BytesIO



dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile}")
#navegador = webdriver.Chrome(executable_path=os.path.join(dir_path, "chromedriver.exe"),options=options)
navegador = webdriver.Chrome(executable_path=os.path.join(dir_path, "chromedriver.exe"))

reader = zxing.BarCodeReader()
canvasfile = r"canvas.png"
navegador.get("https://web.whatsapp.com/")
while len(navegador.find_elements_by_id("side")) < 1:
   if len(navegador.find_elements_by_class_name("_2UwZ_")) > 0:
    print('achei o qr code')
    element = navegador.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div")
    location = element.location
    size = element.size
    png = navegador.get_screenshot_as_png() # saves screenshot of entire page

    screenshot = Image.open(BytesIO(png)) 
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    screenshot = screenshot.crop((left, top, right, bottom)) # defines crop points
    store_width = 300
    store_height = 300
    width, height = screenshot.size

    # Create an image with the desired size for the store
    im = Image.new('RGBA', (store_width, store_height), color=(255, 255, 255))

    # Paste the screenshot on the background and center it
    im.paste(screenshot, (
        int(store_width/2 - width/2),
        int(store_height/2 - height/2)
    ), screenshot)
    im.save(canvasfile) # saves new cropped image
    
   time.sleep(1)
contatos_df = pd.read_json("contatos.json")
for i, item in enumerate(contatos_df["mensagem"]):
    numero = contatos_df.loc[i,"numero"]
    contato = contatos_df.loc[i,"contato"]
    mensagem = urllib.parse.quote(contatos_df.loc[i,"mensagem"])
    print(numero,contato)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}"
    navegador.get(link)
    while len(navegador.find_elements_by_id("side")) < 1:
        time.sleep(1)
    WebDriverWait(navegador, 10).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]'))).send_keys(Keys.ENTER)
    time.sleep(10)