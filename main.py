from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import *

import time
import random

def auth(login, password, link, types, message):

    executable_path = 'C:\\Users\\user\\Desktop\\Python\\telegram-bot\\chromedriver.exe'
    url = 'https://vk.com/'
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={random.choice(userAgent)}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.headless = True

    driver = webdriver.Chrome(executable_path=executable_path, options=options)
    try:
        driver.get(url=url)
        print('start')
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "index_email"))
        )
        email_input.clear()
        email_input.send_keys(login)

        try:
            password_input = driver.find_element(By.ID, "index_pass")
            password_input.clear()
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
        except:
            email_input.send_keys(Keys.ENTER)
            passwordInput = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            passwordInput.clear()
            passwordInput.send_keys(password)
            passwordInput.send_keys(Keys.ENTER)

        time.sleep(2)
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'left_label'))
            ).click
        print('auth...')
        driver.get(url=f'{link}')
        print('get link')

        if types == 'лайки':
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(('class name', 'like_button_icon'))
            ).click()
            time.sleep(2)
            print('add like')

        else:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(('class name', 'FlatButton__in'))
            ).click()
            time.sleep(1)
            mess = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(('id', 'mail_box_editable'))
            )
            mess.clear()
            mess.send_keys(message)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(('id', 'mail_box_send'))
            ).click()
            print('add message')
            time.sleep(2)
            
        driver.close()
        driver.quit()
        return True

    except Exception as ex:
        print(ex)
        return False
        driver.close()
        driver.quit()