# Documentation for Data application project.

The goal of the application is to fetch data for all the zipcodes in the database for all the years starting from 2017. Moreover, a zipcode has to be identified for which the income increment was highest from 2017  to 2021. Finally, every year the table maybe updated using **CRON** job.

This project is made using **python** language and **MariaDB** has been used as the database. This application is containerised using **Docker** and **Docker-compose** hence it can run on any machine without any hassles!

I chose MariaDB over MySQL because it is open source, its transactions are faster than MySQL and it is more scalable relatively.

## Step1 – Fetch the data from API
- The data was fetched from Paavo (open data by postal code area website. The link is mentioned below.
- https://pxnet2.stat.fi/PXWeb/pxweb/en/Postinumeroalueittainen_avoin_tieto
- **Ideally, the url and post query for different years should remain same except the year parameter. In this case, the name of the final px file and one of the parameters in the post query change for every year in the api. To make the data visualization easier, I used the postman website to understand the api structure.**
- 
- 
- fetch_data(start_year, end_year) this function gets data from the api, takes starting and end year as arguments and returns a dataframe containing the average income for all the zipcodes from year 2017 to 2021.
- This function extracts the required parameters from the api to form the final url along with the json query which is required to fetch the data and converts it into a dataframe.
- 
- This dataframe is returned as output with first row as 2017 and last row as 2021.
- As the api has a timeout of 20 seconds, the function is called after every 30 seconds until the api is reached. After 5 retries, the program is terminated.

## Step 2 : Storing the data in the database
- I fetch a MariaDB image for docker when the application is containerized and the docker service is passed as a service host for the application.
- This function takes the above dataframe as in input, converts it in a suitable format for the database and inserts it in the database.
- 
- Final dataframe
- The data fetched from the api is inconsistent i.e not all the zipcodes have data for every year. Hence, the initial dataframe has some NaN value.
- These NaNs are handled in this function and only valid data is stored in the database.
- The database created is ‘FINLAND_DATABASE’ and the table is ‘INCOME_TABLE’
- Some query results
- 
-

## Step 3 : Identifying zipcode with highest income change for 5 years along with the percent change
- calc_max_avg_income(start_year,end_year) : this function takes the input for which the income change is to be calculated then prints the required zipcode and returns the percentage change.
- The function compares the income for every zipcode for both years and calculates the max. difference accordingly.

## Step 4 : Wait for the scheduled time to update the table
- **Pycron** is used for scheduling to wait until the desired time is reached. 
- In this case, the application will run forever and update the table on every 5th of march.
- The same functions used above are used for this process as well.
## Instructions to run the application

- Prerequisites - [Docker](https://www.docker.com/products/docker-desktop), [Python](https://www.python.org/downloads/windows/)
- Clink on [this](https://docs.docker.com/engine/install/ubuntu/) to know more about installing docker.
- After the docker is successfully set-up, run
 ```docker-compose up --force-recreate```
- This command will build and execute the docker compose image which is defined in the docker-compose.yaml file
- The application should start working now.
- finali image

## Incase this application is to be run directly on the machine(Unix like OS )

- The python scheduling can be skipped and instead **Cron** jobs can be scheduled.
- Run the following commands
 ```crontab -e```
 ```0 0 5 3 * $(which python3) {path to updatedata.py} >> ~/cron.log 2>&1 ```
- A cron job will be scheduled accordingly.

