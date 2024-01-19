import pandas as pd
import psycopg2
import numpy
class Pipline:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
        host='localhost',
        database='gdadatawarehouse',
        user='postgres',
        password="yourpassword"
        )
        self.cur = self.conn.cursor()
    
    def extractor():
        data =  pd.read_csv("pharmade/DATA/pharma-data.csv")
        return 

    def transform(data):
        #it will return list of dataframes for respective tables
        return 

    def schema(dflist):
        # it will create tables and schema for the perticular dataframe
        return 

