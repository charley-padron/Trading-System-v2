import json
import configparser
import requests
from rauth import OAuth1Service

#from accounts.accounts import Accounts
#from market.market import Market
#from alerts.alerts import Alerts

# not needed from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import random
import selenium

# loading configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Read config file
# login and authenticate
class account:
    def oauth(self):
        """Allows user authorization for the sample application with OAuth 1"""
        etrade = OAuth1Service(
            name="etrade",
            consumer_key=config["DEFAULT"]["CONSUMER_KEY"],
            consumer_secret=config["DEFAULT"]["CONSUMER_SECRET"],
            request_token_url="https://api.etrade.com/oauth/request_token",
            access_token_url="https://api.etrade.com/oauth/access_token",
            authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
            base_url="https://api.etrade.com")
        
        base_url = config["DEFAULT"]["PROD_BASE_URL"]
        
         # Step 1: Get OAuth 1 request token and secret
        request_token, request_token_secret = etrade.get_request_token(
            params={"oauth_callback": "oob", "format": "json"})
    
        # Step 2: Go through the authentication flow. Login to E*TRADE.
        # After you login, the page will provide a text code to enter.
        authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
        
        #############################################
        # Automate the login process
        # Version 17, now 18
        # driver = webdriver.Edge(executable_path='C:/Users/charl/Downloads/edgedriver_win64/MicrosoftWebDriver.exe')
        driver = webdriver.Edge()
        
        driver.get(authorize_url)
        
        logon = driver.find_element_by_id("logon_button")
        logon.click()
        
        # not working
       # driver.implicitly_wait(5)
         
        accept = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//form[@name='CustInfo']/input[3]")))
         
        #accept = driver.find_element_by_xpath("//form[@name='CustInfo']/input[3]")
        accept.click()
        
        #code = driver.find_element_by_xpath("//div[@style='text-align:center']/input[1]")
        code = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@style='text-align:center']/input[1]")))
        code = code.get_attribute('value')
        
        driver.close()
            
        text_code = code
    
        # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
        session = etrade.get_auth_session(request_token,
                                      request_token_secret,
                                      params={"oauth_verifier": text_code})
        
        #automateTrades(session, base_url)
        #print(session, base_url)
    
if __name__ == "__main__":
    account.oauth()