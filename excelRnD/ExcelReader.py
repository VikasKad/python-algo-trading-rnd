# Program extracting all columns
# name in Python
import xlrd
import pandas as pd
import requests
from lxml import html
import numpy as np
from time import time

excel_loc = "sample_with_button.xlsm"
USERNAME = "miso@microfox.com"
PASSWORD = "C\woV7VJ5(b>bdh"

LOGIN_URL = "http://equ.microfox.io:8080/Identity/Account/Login"

url = 'http://equ.microfox.io:8080/'


def main():
    while True:
        try:
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
            result = session_requests.post(
                LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))
            print('user logged in')
            # Scrape url
            result = session_requests.get(url, headers=dict(referer=url))
            pd_html = (pd.read_html(result.text))
            pd_html = pd_html[0]
            pd_html_required = pd_html[['ID', 'Symbol', 'Decrement',
                                        'CurrentValue', 'Increment']]
            print('fetched website data')
            pd_excel = pd.read_excel(excel_loc, engine='xlrd')
            pd_excel_required = pd_excel[['ID', 'Symbol', 'Decrement',
                                          'CurrentValue', 'Increment']]

            print('fetched excel data')
            print(pd_html_required.equals(pd_excel_required))
            if pd_html_required.equals(pd_excel_required):
                print('identitical')
            else:
                print('find to update columns')
                # create new column in df1 to check if prices match
                diff_output = np.where(
                    pd_excel_required.CurrentValue == pd_html_required.CurrentValue, 'True', 'False')
                # print(diff_output)
                # print('length', diff_output.size)
                count = 0
                for i in diff_output:
                    if i == "False":  # its false so we have to update it into web
                        if pd_excel_required.CurrentValue[count] > pd_html_required.CurrentValue[count]:
                            # get increment by value
                            number_of_clicks = (
                                pd_excel_required.CurrentValue[count] - pd_html_required.CurrentValue[count])
                            print('click plus button ',
                                  pd_excel_required.ID[count], number_of_clicks, ' times')
                            payload = {
                                "ValueID": pd_excel_required.ID[count],
                                "Value": number_of_clicks,
                            }
                            response = session_requests.post(
                                'http://equ.microfox.io:8080/home/increment', data=payload, headers=dict(referer=LOGIN_URL))
                        else:
                            number_of_clicks = (
                                pd_html_required.CurrentValue[count] - pd_excel_required.CurrentValue[count])
                            payload = {
                                "ValueID": pd_excel_required.ID[count],
                                "Value": number_of_clicks,
                            }
                            print('click plus button ',
                                  pd_excel_required.ID[count], number_of_clicks, ' times')
                            response = session_requests.post(
                                'http://equ.microfox.io:8080/home/decrement', data=payload, headers=dict(referer=LOGIN_URL))

                    count = count + 1
        except:
            print('file locked it will try ')


start_time = time()
main()
end_time = time()
time_taken = end_time - start_time  # time_taken is in seconds
print(time_taken)
