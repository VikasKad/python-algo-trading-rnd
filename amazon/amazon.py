
# What's new in version 2.0?
# 1. Added push notification features for android.
# 2. New formatting in EMAIL SECTION.
# 3. Confirmation message after sending MAIL and NOTIFICATION

# What's new in version 2.1?
# 1. Minor bug fixing
# 2. Time stamp added
# 3. No. of attempts added

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import requests
import time
import smtplib
from bs4 import BeautifulSoup
# from notify_run import Notify
from datetime import datetime

# USER INPUT-------------------------------------but I make it comment because I want to specify this product only.
'''
url = input("Enter your URL here : ")
dp = int(input("Enter your desired price : "))
'''
# -----------------------------------------------

url = "https://www.amazon.in/Philips-Trimmer-Cordless-QT4001-15/dp/B00L8PEEAI/ref=sr_1_4?crid=26OVQAIRQLJUU&keywords=philips+qt4011%2F15&qid=1569507835&s=hpc&sprefix=philips+qt%2Chpc%2C361&sr=1-4"
dp = 1000
URL = url
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}


page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

# ----------------------------------------------------- TO CHECK WHETHER soup IS WORKING OR NOT
'''
m=open('soupw.txt',"wb")
m.write(soup.prettify().encode("utf-8"))
m.close
'''
# --------------------------------------------------------------------------------------

title = soup.find(id="productTitle").get_text()
price = soup.find(id="priceblock_ourprice").get_text()
main_price = price[2:]

# LETS MAKE IT AN INTEGER---------------------------------------------------------------

l = len(main_price)
if l <= 6:
    main_price = price[2:5]
else:
    p1 = price[2]
    p2 = price[4:7]
    pf = str(p1)+str(p2)
    main_price = int(pf)

price_now = int(main_price)

# VARIABLES FOR SENDING MAIL AND PUSH NOTIFICATION---------------------------------------

title1 = str(title.strip())
main_price1 = main_price
pnmsg = "Rs. "+str(main_price1)+" for "+title1

print("NAME : " + title1)
print("CURRENT PRICE : " + str(main_price1))
print("DESIRED PRICE : " + str(dp))
# -----------------------------------------------Temporary fixed for values under Rs. 9,999

'''
print(title.strip())
print(price.strip())
print(main_price)
 
print(real_price)
print(type(real_price))
print(dp)
print(type(dp))
'''
# FUNCTION TO CHECK THE PRICE-------------------------------------------------------


def check_price():
    count = 0
    if(price_now <= dp):
        print('price')
        # send_mail()
        # push_notification()
    else:
        count = count+1
        print("Rechecking... Last checked at "+str(datetime.now()))

# Lets send the mail-----------------------------------------------------------------


# def send_mail():
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()

#     server.login('dev.amlan.99@gmail.com', 'fzanpwfvxnldiycv')

#     subject = "Price of "+title1+" has fallen down to Rs. "+str(main_price1)
#     body = "Hey Amlan! \n The price of "+title1+" on AMAZON has fallen down to Rs." + \
#         str(main_price1)+", which is less than your desired price of Rs." + \
#         str(dp)+".\n So, hurry up & check the amazon link right now : "+url

#     msg = f"Subject: {subject} \n\n {body} "

#     server.sendmail(
#         'dev.amlan.99@gmail.com',
#         'amlansk53@gmail.com',
#         msg
#     )
#     print("HEY AMLAN, EMAIL HAS BEEN SENT SUCCESSFULLY.")

#     server.quit()
# Now let's send the push notification-------------------------------------------------


# def push_notification():
#     notify = Notify()
#     notify.send(pnmsg)
#     print("HEY AMLAN, PUSH NOTIFICATION HAS BEEN SENT SUCCESSFULLY.")

#     print("Check again after an hour.")


# Now lets check the price after 1 min -----------------------------------------------
count = 0
while(True):
    count += 1
    print("Count : "+str(count))
    check_price()
    time.sleep(60)
