from ast import main
import mailbox
from operator import index
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
class ETL:
    def __init__(self) -> None:
        # self.conn = psycopg2.connect(
        # host='localhost',
        # database='gdadatawarehouse',
        # user='postgres',
        # password="yourpassword"
        # )
        # self.cur = self.conn.cursor()
        self.postgresql_engine = create_engine("postgresql+psycopg2://postgres:PostgreSQL@localhost:5432/postgres")
    
    def extractor(url):
        data =  pd.read_csv("pharmade/DATA/pharma-data.csv")
        print("Data Extracted Successfully...")
        return data

    def transform(self,pharma_df):
        #it will return list of dataframes for respective tables
        pharma_df['calc_amount'] = pharma_df["Quantity"] * pharma_df["Price"]
        dflist = {}

        #creating customer dimension
        customer = pd.DataFrame({"Customer Name":pharma_df['Customer Name'].unique()})
        customer['Customer_ID'] = customer.index
        dflist['DIM-customer'] = customer

        #creating distributor dimension
        df_distributor = pd.DataFrame({"Distributor":pharma_df['Distributor'].unique()}).reset_index().drop('index',axis=1)
        df_distributor['Distributor_ID'] = df_distributor.index
        dflist['DIM-distributor'] = df_distributor

        #creating month dimension
        df_month = pd.DataFrame({"Month":pharma_df["Month"].unique()})
        df_month['Month_ID'] = df_month.index
        dflist['DIM-month'] = df_month

        #creating produt dimension
        df_product = pharma_df[['Product Name', 'Product Class']].drop_duplicates().reset_index().drop('index',axis=1)
        df_product['Product_ID'] = df_product.index
        dflist['DIM-product'] = df_product

        #creating subchannel dimension
        df_subchannel = pharma_df[['Sub-channel', 'Channel']].drop_duplicates().reset_index().drop('index',axis=1)
        df_subchannel["Subchannel_ID"] = df_subchannel.index
        dflist['DIM-subchannel'] = df_subchannel


        #creating city dimension
        df_city = pharma_df[['City', 'Country','Latitude', 'Longitude']].drop_duplicates().reset_index().drop('index',axis=1)
        df_city["City_ID"] = df_city.index
        dflist['DIM-city'] = df_city
        # print(df_city.head())

        #creating sales repository dimension
        df_salserep = pd.DataFrame({"Name of Sales Rep":pharma_df["Name of Sales Rep"].unique()})
        df_salserep["Sales_rep_ID"] = df_salserep.index
        dflist['DIM-slaes-rep'] = df_salserep

        #creating slaes team dimension
        df_salseteam = pharma_df[['Sales Team', 'Manager']].drop_duplicates()[:-1].reset_index().drop('index',axis=1)
        df_salseteam["Sales_team_ID"] = df_salseteam.index
        dflist['DIM-slaes-team'] = df_salseteam

        #creating fact dataframe
        # print(pharma_df.columns)
        fact_table = pd.merge(pharma_df,customer,on="Customer Name",how='left')
        fact_table.drop('Customer Name',axis=1,inplace=True)
        fact_table = pd.merge(fact_table,df_distributor,on="Distributor",how='left')
        fact_table.drop('Distributor',axis=1,inplace=True)
        fact_table = pd.merge(fact_table,df_month,on="Month",how='left')
        fact_table.drop('Month',axis=1,inplace=True)
        fact_table = pd.merge(fact_table,df_product,on="Product Name",how='left')
        fact_table.drop(columns=['Product Name',"Product Class_x","Product Class_y"],axis=1,inplace=True)
        fact_table = pd.merge(fact_table,df_subchannel,on="Sub-channel",how='left')
        fact_table.drop(columns=['Sub-channel',"Channel_x","Channel_y"],axis=1,inplace=True)
        fact_table = pd.merge(fact_table,df_salseteam,on="Sales Team",how='left')
        fact_table.drop(columns=['Sales Team',"Manager_x","Manager_y"],axis=1,inplace=True)
        fact_table = pd.merge(fact_table,df_salserep,on="Name of Sales Rep",how='left')
        # print(fact_table.columns)
        fact_table.drop(columns=['Name of Sales Rep'],axis=1,inplace=True)
        fact_table = pd.merge(fact_table,df_city,on="City",how='left')
        fact_table.drop(columns=['City','Country_x','Country_y','Latitude_x', 'Longitude_x','Latitude_y', 'Longitude_y'],axis=1,inplace=True)
        dflist['Fact-sales'] = fact_table

        print("Data Tranformed Successfully...")
        return dflist

    def load_to_postgres(self,dflist):
        # it will create tables and schema for the perticular dataframe
        for key, value in dflist.items():
            value.to_sql(key,self.postgresql_engine,if_exists='replace',index= False)

        print("Data Loaded Successfully...")
    
    def load_to_bigquery(dflist):
        # it will create tables and schema for the perticular dataframe
        return 
    
if __name__=="__main__":
    etl = ETL()
    df = etl.extractor()
    dflist = etl.transform(df)
    etl.load_to_postgres(dflist)
