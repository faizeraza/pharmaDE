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
    def ggenerator(self,df,metadata,colums):
        if metadata[0]=="Bar Chart":
            fig = px.bar(df,x=colums[0],y=columns[1])
            st.plotly_chart(fig,use_container_width=True)
        elif metadata[0]=="Line Chart":
            fig = px.line(df,x=colums[0],y=columns[1])
            st.plotly_chart(fig,use_container_width=True)
        elif metadata[0]=="Pie Chart":
            fig = px.pie(df,names=colums[0],values=columns[1])
            st.plotly_chart(fig,use_container_width=True)
    def querytodf(self,query,columns):
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
            df = pd.DataFrame(np.array(result),columns=columns.split(","))
        except:
            st.warning("There is something wrong with your query", icon="🤕")
            df = None
        return df
    def decorator(self):
        pass

if __name__=="__main__":
    query = st.text_area("Entery Query Here (the output must contain two columns only)")
    columns = st.text_input("Enter Columns Name (first must be continues second categorical)")
    option = st.selectbox("Select Graph",("Bar Chart","Line Chart","Pie Chart"))
    if st.button('Run'):
        main = sqltoquery()
        df = main.querytodf(query,columns)
        st.dataframe(df,use_container_width=True)
        metadata = [option]
        columns = columns.split(',')
        print(type(columns))
        main.ggenerator(df,metadata,columns)