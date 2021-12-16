import functions
from datetime import date
import  time
import sys

todays_date = date.today()
year = todays_date.year

for i in range(1 , 6):
    try:
        api_data = functions.fetch_data(year,year)
        flag = True
        break
    except Exception as e:
        print("Oops!", e.__class__, "occured! Trying again after 30 seconds")
        time.sleep(3)

if flag == False:
    sys.exit('Database api fetch has failed. Please try again later!')
print('Data fetched successfully!')


try:
    functions.data_to_db(api_data)
except Exception as e:
    print("Oops!", e.__class__, "occured! Try again later")
    sys.exit(0)

print('Data stored in Database')