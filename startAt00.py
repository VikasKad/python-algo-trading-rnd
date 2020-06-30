import datetime
# import time
# dateSTR = datetime.datetime.now().strftime("%H:%M:%S")
# # print(dateSTR)
# if dateSTR == ("13:23:01"):
#    # do function
#     print(dateSTR)
# else:
#     # do something useful till this time
#     time.sleep(1)
#     pass

import schedule
import time


def job():
    dateSTR = datetime.datetime.now().strftime("%H:%M:%S")
    print("I'm working...", dateSTR)


schedule.every(1).minutes.at(':01').do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
