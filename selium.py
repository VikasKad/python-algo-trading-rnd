import xlrd
import pandas as pd
import requests
from lxml import html
import numpy as np
from time import time

excel_loc = "/Users/cex/Downloads/Sample.xls"
USERNAME = "miso@microfox.com"
PASSWORD = "C\woV7VJ5(b>bdh"

LOGIN_URL = "http://equ.microfox.io:8080/Identity/Account/Login"

url = 'http://equ.microfox.io:8080/'


def login():
    chromedriver = '/usr/local/bin/chromedriver'
    browser = webdriver.Chrome(chromedriver)
    browser.get("http://equ.microfox.io:8080/")
    # time.sleep(10)
    username = browser.find_element_by_id("Input_Email")
    password = browser.find_element_by_id("Input_Password")
    # reqs = browser.find_element_by_id("__RequestVerificationToken")

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    # reqs.sendKeys("__RequestVerificationToken")
    login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
    login_attempt.submit()
    browser.get("http://equ.microfox.io:8080/")
    element = browser.find_element_by_id("logoutForm")
    element.click()

    print(login_attempt.text)


def find():
    session_requests = requests.session()
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(
        set(tree.xpath("//input[@name='__RequestVerificationToken']/@value")))[0]
    payload = {
        "Input.Email": USERNAME,
        "Input.Password": PASSWORD,
        "__RequestVerificationToken": authenticity_token
    }
    response = session_requests.post(
        LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))
    cookies = response.cookies.get_dict()
    payload = {
        "ValueID": 62,
        "Value": 45,
    }
    print('user logged in', cookies)

    response = session_requests.post(
        'http://equ.microfox.io:8080/home/increment', data=payload, headers=dict(referer=LOGIN_URL))
    print('response', html.fromstring(response.text))

# driver.get("http://equ.microfox.io:8080/")
# button = driver.find_element_by_tag_name('input')
# print(button.get_attribute('innerHTML'))
# # button.click()
# driver.quit()


# login()
find()
