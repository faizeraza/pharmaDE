import pandas as pd 
import streamlit as st
import psycopg2 as psy
import numpy as np
import plotly.express as px

class sqltoquery:
    def __init__(self) -> None:
        st.sidebar.markdown("# Query graph")
        st.header('Query To Graph')
        conn = psy.connect("dbname=postgres user=postgres")
        self.cur = conn.cursor()
    def ggenerator(self,df,metadata):
        if metadata[0]=="Bar Chart":
            fig = px.bar(df,x="Distributors",y="Sales")
            st.bar_chart(df)
    def querytodf(self,query,columns):
        self.cur.execute(query)
        result = self.cur.fetchall()
        df = pd.DataFrame(np.array(result),columns=columns.split(","))
        return df
    def decorator(self):
        pass

if __name__=="__main__":
    query = st.text_area("Entery Query Here")
    columns = st.text_input("Enter Columns Name")
    option = st.selectbox("Select Graph",("Bar Chart","Line Chart","Pie Chart"))
    if st.button('Run'):
        main = sqltoquery()
        df = main.querytodf(query,columns)
        st.dataframe(df,use_container_width=True)
        metadata = [option]
        main.ggenerator(df,metadata)