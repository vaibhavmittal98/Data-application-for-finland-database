import pandas as pd
import requests
import mysql.connector as mariadb
from sqlalchemy import create_engine



def fetch_data(start_year, end_year):
    output = pd.DataFrame()
    years = range(start_year, end_year + 1)
    for i in years:  # for loop starts
        url = "https://pxnet2.stat.fi:443/PXWeb/api/v1/en/Postinumeroalueittainen_avoin_tieto/" + i.__str__() + "/"
        temp = requests.get(url)
        name = temp.json()[2]["id"]
        url = url + name

        data_postal_codes = requests.get(url)    # using get to fetch the required parameters fot the post query
        data_postal_codes = data_postal_codes.json()

        list_postal_codes = data_postal_codes["variables"][0]["values"][1:]
        text_value = data_postal_codes["variables"][1]["values"][1]

        json_query = {
            "query": [
                {
                    "code": "Postinumeroalue",
                    "selection": {
                        "filter": "item",
                        "values": list_postal_codes
                    }
                },
                {
                    "code": "Tiedot",
                    "selection": {
                        "filter": "item",
                        "values": [
                            text_value
                        ]
                    }
                }
            ],
            "response": {
                "format": "json-stat2"
            }
        }

        data_income = requests.post(url, json=json_query)

        avg_income = data_income.json()["value"]

        diction = dict(zip(list_postal_codes, avg_income))
        output = output.append(diction, ignore_index=True)  # creating a dataframe of values
        # for loop ends
    return output


def data_to_db(data):
    final_data = pd.DataFrame(columns=['ID', 'ZIPCODE', 'YEAR', 'AVG_INCOME'])
    columns = ["ID", "ZIPCODE", "YEAR", "AVG_INCOME"]

    for j in range(len(data.columns)):
        for i in range(len(data)):
            year = (2017 + i)
            zipcode = data.columns[j]
            ID = data.columns[j] + "_" + year.__str__()
            avg_income = data.iat[i, j]
            dict_data = dict(zip(columns, [ID, zipcode, year, avg_income]))
            if (pd.isna(avg_income) == False):
                final_data = final_data.append(dict_data, ignore_index=True)

    mariadb_connection = mariadb.connect(user='root', password='9012349000', host='db', port='3306')   # running in a docker
                                                                                                        # container hence the host is used a service from docker yaml file
    create_cursor = mariadb_connection.cursor()

    create_cursor.execute("CREATE DATABASE IF NOT EXISTS FINLAND_DATABASE")
    sql_query = "USE FINLAND_DATABASE"
    create_cursor.execute(sql_query)
    sql_query = "CREATE OR REPLACE TABLE INCOME_TABLE ( ID VARCHAR(255), ZIPCODE VARCHAR(255), YEAR INT , AVG_INCOME DECIMAL(10,2), PRIMARY KEY (ID))"
    create_cursor.execute(sql_query)

    engine = create_engine("mysql+pymysql://root:9012349000@db/FINLAND_DATABASE")

    final_data.to_sql(name='INCOME_TABLE', con=engine, if_exists='append', index=False) #storing the whole dataframe at once in the database

def calc_max_avg_income(start_year,end_year):
    mariadb_connection = mariadb.connect(user='root', password='9012349000', database='FINLAND_DATABASE',
                                         host='db', port='3306')

    create_cursor = mariadb_connection.cursor()

    sql_query = '''SELECT ZIPCODE, AVG_INCOME FROM INCOME_TABLE WHERE YEAR = %s;'''
    data_start_year = pd.read_sql_query(sql_query, mariadb_connection,params = [start_year])

    sql_query = '''SELECT ZIPCODE, AVG_INCOME FROM INCOME_TABLE WHERE YEAR = %s;'''
    data_end_year = pd.read_sql_query(sql_query, mariadb_connection, params = [end_year])   #selecting data for different years to compare

    max_value = -11111.0
    final_zipcode = ''
    for i in range(len(data_end_year)):
        zipcode = data_end_year.iat[i, 0]
        check = data_start_year.loc[data_start_year['ZIPCODE'] == zipcode]
        if check.empty:
            continue
        diff = data_end_year.iat[i, 1] - data_start_year.loc[data_start_year['ZIPCODE'] == zipcode].iat[0, 1]
        if (diff > max_value):
            max_value = diff
            final_zipcode = zipcode

    print('The zipcode with the most improved income is ', final_zipcode)
    curr_income = data_end_year.loc[data_end_year['ZIPCODE'] == final_zipcode].iat[0, 1]
    prev_income = data_start_year.loc[data_start_year['ZIPCODE'] == final_zipcode].iat[0, 1]
    return (100 * (curr_income - prev_income) / prev_income)


