import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2 
import pydeck as pdk

class MainPage:
    def __init__(self,url) -> None:
        st.set_page_config(
            page_title="Dashboard",
            page_icon="📊",
            layout="wide",
        )
        st.title("Pharma Dashboard")
        self.pharmadf = pd.read_csv(url)
        conn = psycopg2.connect("dbname=postgres user=postgres")
        self.cur = conn.cursor()
    def selectjob(self):
        query = """SELECT Distinct("Year") FROM public."Fact-sales";"""
        self.cur.execute(query)
        years = [str(ele[0])[:4] for ele in self.cur.fetchall()]
        years.append("ALL")
        job_filter = st.selectbox("Select the Year", years)
        # self.cur.close()
        return job_filter
    def plottopdict(self):
        query = """SELECT "Distributor", SUM("fs"."Sales")
                FROM public."Fact-sales" as "fs" left join public."DIM-distributor" as "dist" on "fs"."Distributor_ID" = "dist"."Distributor_ID"
                Group BY "dist"."Distributor"
                Order By "sum" DESC limit 5;"""
        self.cur.execute(query)
        result = self.cur.fetchall()
        df = pd.DataFrame(np.array(result),columns=["Distributors","Sales"])
        # print(df)
        fig = px.bar(df,x="Distributors",y="Sales")
        st.plotly_chart(fig,use_container_width=True)

    def plottopcity(self):
        query = """SELECT "ct"."City", SUM("fs"."Sales") as "SalesSum",AVG("ct"."Latitude") as "Latitude",AVG("Longitude") as "Longitude"
                FROM public."Fact-sales" as "fs" left join public."DIM-city" as "ct" on "fs"."City_ID" = "ct"."City_ID"
                Group BY "ct"."City"
                Order By "SalesSum" DESC;"""
        self.cur.execute(query)
        result = self.cur.fetchall()
        df = pd.DataFrame(np.array(result),columns=["City","SalesSum","Lat","Long"])
        df["Long"] = df["Long"].astype(float)
        df["Lat"] = df["Lat"].astype(float)
        df["SalesSum"] = df["SalesSum"].astype(float)/10000
        # df["SalesSum"] = df["SalesSum"]/1000
        print(df)
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=df['Lat'][0],
                longitude=df['Long'][0],
                zoom=5,
                pitch=30,
            ),
            layers=[
                pdk.Layer(
                    'ColumnLayer',
                    data=df,
                    get_position=['Long',"Lat"],
                    get_elevation=["SalesSum"],
                    auto_highlight=True,
                    elevation_scale=10,
                    pickable=True,
                    extruded=True,
                    get_radius=100,
                    get_fill_color=[245, 203, 66],
                    coverage=1
                )
            ]
        ))
    

if __name__=="__main__":
    path = r"C:\Users\Faizan Raza\Desktop\pharmaDE\pharmade\DATA\pharma-data.csv"
    mainpage = MainPage(path)
    mainpage.selectjob()
    mainpage.plottopdict()
    mainpage.plottopcity()
