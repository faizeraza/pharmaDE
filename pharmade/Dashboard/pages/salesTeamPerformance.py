import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2 
import pydeck as pdk

class salesTeamPerformance:
    def __init__(self,url) -> None:
        st.set_page_config(
            page_title="Dashboard",
            page_icon="📊",
            layout="wide",
        )
        st.title("Sales Team Performance")
        # self.pharmadf = pd.read_csv(url)
        conn = psycopg2.connect("dbname=postgres user=postgres")
        self.cur = conn.cursor()
    # def selectjob(self):
    #     query = """SELECT Distinct("Year") FROM public."Fact-sales";"""
    #     self.cur.execute(query)
    #     years =["ALL"]
    #     years = years+[str(ele[0])[:4] for ele in self.cur.fetchall()]
    #     job_filter = st.selectbox("Select the Year", years)
    #     # self.cur.close()
    #     return job_filter
    def plottopSalesTeam(self):
        st.write("Top Sales Team")
        query = """SELECT "Sales Team", SUM("fs"."Sales")
                    FROM public."Fact-sales" as "fs" left join public."DIM-sales-team" as "steam" on "fs"."Sales_team_ID" = "steam"."Sales_team_ID"
                    Group BY "steam"."Sales Team"
                    Order By "sum";"""
        self.cur.execute(query)
        result = self.cur.fetchall()
        df = pd.DataFrame(np.array(result),columns=["Sales Team","Sales"])
        # print(df)
        fig = px.bar(df,x="Sales Team",y="Sales")
        st.plotly_chart(fig,use_container_width=True)

if __name__=="__main__":
    path = r"C:\Users\Faizan Raza\Desktop\pharmaDE\pharmade\DATA\pharma-data.csv"
    stperformance = salesTeamPerformance(path)
    # mainpage.selectjob()
    stperformance.plottopSalesTeam()