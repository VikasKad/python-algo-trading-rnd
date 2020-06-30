from datetime import datetime
from datetime import timedelta

# machine_time_minute = datetime.utcnow().strftime("%M")
# print(machine_time_minute)
# print('mach', machine_time_minute)
# print(len(machine_time_minute))
# print(machine_time_minute[1])
# if machine_time_minute[1] == '5':
#     print('yes')
# elif machine_time_minute[1] == '0':
#     print('yes')
# else:
#     print('no')
# arr = '232'
# if machine_time_minute[1] == '0' or machine_time_minute[1] == '5':
#     print('ues')
# else:
#     print('rr')

current_time = datetime.now().replace(microsecond=0)
requested_time = '2019-09-25T10:17:42.000Z'
requested_time = requested_time.replace('T', ' ')
requested_time = requested_time.replace('.000Z', '')
print('requested time', requested_time)
datetime_object = datetime.strptime(
    requested_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
time_diff = (
    current_time-datetime.strptime(datetime_object, '%Y-%m-%d %H:%M:%S'))
print(time_diff)

time_difference_in_minutes = time_diff / timedelta(minutes=1)
if time_difference_in_minutes > 10:
    print('greater than 10 mins')
else:
    print('less than 10 mins')
