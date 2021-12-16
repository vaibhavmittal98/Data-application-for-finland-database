import pandas as pd
import requests
import sys
import functions
import time
import pycron

flag = False
for i in range(1 , 6):
    try:
        api_data = functions.fetch_data(2017,2021)
        flag = True
        break
    except Exception as e:
        print("Oops!", e.__class__, "occured! Trying again after 30 seconds")
        time.sleep(30)


if flag == False:
    sys.exit('Database api fetch has failed. Please try again later!')
print('Data fetched successfully!')


try:
    functions.data_to_db(api_data)
except Exception as e:
    print("Oops!", e.__class__, "occured! Try again later")
    sys.exit(0)

print('Data stored in Database')
try:
    percent_income = functions.calc_max_avg_income(2017,2021)
except Exception as e:
    print("Oops!", e.__class__, "occured! Try again later")
    sys.exit(0)

print('The percentage increase in income is ', percent_income)


while True:
    if pycron.is_now('0 0 5 3 *'):   # True every 5th march at 00:00
        print('Updating database')
        todays_date = date.today()
        year = todays_date.year

        for i in range(1, 6):
            try:
                api_data = functions.fetch_data(year, year)
                flag = True
                break
            except Exception as e:
                print("Oops!", e.__class__, "occured! Trying again after 30 seconds")
                time.sleep(30)

        if flag == False:
            sys.exit('Database api fetch has failed. Please try again later!')
        print('Data fetched successfully!')

        try:
            functions.data_to_db(api_data)
        except Exception as e:
            print("Oops!", e.__class__, "occured! Try again later")
            sys.exit(0)

        print('Data stored in Database')
        time.sleep(100)
    else:
        time.sleep(15)
        print("Waiting for next year!")