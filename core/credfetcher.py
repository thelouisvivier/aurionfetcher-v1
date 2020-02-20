"""
    Aurion Credentials Fetcher
"""
import sys

# Credentials
from config.config import *

#Storage
from core.storage import *

# Selenium for Firefox/Chrome control
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# Sleep
from time import sleep

def credfetcher(trail):
    try:
        #Get informations needed on Aurion : cookie, ViewState

        #Headless firefox
        options = Options()
        options.headless = True
        
        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages', 'fr-FR, fr')

        #Init driver
        driver = webdriver.Firefox(firefox_profile=profile,options=options)

        #Go to login page
        driver.get(aurion_url + "/faces/Login.xhtml")

        #Wait for login page to load
        while True:
            try:
                print ("        Login page loaded")
                driver.find_element_by_id("username")
                break
            except:
                sleep(1)
                continue

        #Fill with user informations from config.py
        driver.find_element_by_id("username").send_keys(aurion_username)
        driver.find_element_by_id("password").send_keys(aurion_password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        print ("        Logged")
        #Wait for load of start page
        #while True:
        #    try:
        #        # On clicke sur l'onglet Scolarité
        #        driver.find_element_by_xpath("//*[contains(text(), 'Scolarité')]").click()
        #        break
        #    except:
        #        sleep(1)
        #        continue

        #Wait for load of Scolarité tab
        while True:
            try:
                #Click in Schedule tab
                driver.find_element_by_xpath("//*[contains(text(), 'Mon Planning')]").click()
                break
            except:
                sleep(1)
                continue

        #When schedule loaded
        while True:
            try:
                print ("        Schedule loaded")
                driver.find_element_by_class_name("fc-month-button")
                break
            except:
                sleep(1)
                continue

        #Get ViewState
        trail._viewState = driver.find_element_by_xpath("//input[@name='javax.faces.ViewState']").get_attribute("value")

        #Get form id (form:j_idtxxx)
        trail._formId = driver.find_element_by_class_name("schedule").get_attribute("id")

        #Get cookie
        cookies = driver.get_cookies()
        trail._sessionId = ""

        #Keep session id
        for c in cookies:
            if c["name"] == "JSESSIONID":
                trail._sessionId = c["value"]

        #Close browser
        driver.close()
        return True
    except:
        print("Unexpected error in credfetcher:", sys.exc_info()[0])
