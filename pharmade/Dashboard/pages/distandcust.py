import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2 
import pydeck as pdk

class distandcustanalysis:
    def __init__(self,url) -> None:
        st.set_page_config(
            page_title="Dashboard",
            page_icon="📊",
            layout="wide",
        )
        st.title("Distributor And Customer Analysis")
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
    def plottopdist(self):
        st.write("Top Distributors")
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

    def plottopcust(self):
        st.write("Top Customers")
        query = """SELECT "Customer Name", SUM("fs"."Sales")
                FROM public."Fact-sales" as "fs" left join public."DIM-customer" as "cust" on "fs"."Customer_ID" = "cust"."Customer_ID"
                Group BY "cust"."Customer Name"
                Order By "sum" DESC limit 5;"""
        self.cur.execute(query)
        result = self.cur.fetchall()
        df = pd.DataFrame(np.array(result),columns=["Customer Name","Sales"])
        # print(df)
        fig = px.bar(df,x="Customer Name",y="Sales")
        st.plotly_chart(fig,use_container_width=True)

    def plottopcity(self):
        st.write("Sales By City")
        query = """SELECT "ct"."City", SUM("fs"."Sales") as "SalesSum",AVG("ct"."Latitude") as "Latitude",AVG("Longitude") as "Longitude"
                FROM public."Fact-sales" as "fs" left join public."DIM-city" as "ct" on "fs"."City_ID" = "ct"."City_ID"
                Group BY "ct"."City"
                Order By "SalesSum" DESC;"""
        self.cur.execute(query)
        result = self.cur.fetchall()
        df = pd.DataFrame(np.array(result),columns=["City","SalesSum","Lat","Long"])
        df["Long"] = df["Long"].astype(float)
        df["Lat"] = df["Lat"].astype(float)
        df["SalesSum"] = df["SalesSum"].astype(float)
        # df["SalesSum"] = df["SalesSum"]/1000
        print(df)
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=df['Lat'][0],
                longitude=df['Long'][0],
                zoom=5,
                pitch=100,
            ),
            layers=[
                pdk.Layer(
                    'ColumnLayer',
                    data=df,
                    get_position=['Long',"Lat"],
                    get_elevation=["SalesSum/10000"],
                    auto_highlight=True,
                    elevation_scale=50,
                    pickable=True,
                    extruded=True,
                    get_radius=100,
                    get_fill_color=[245, 203, 66],
                    coverage=1
                ),
                pdk.Layer(
                    'HexagonLayer',
                    data=df,
                    get_position=['Long',"Lat"],
                    get_elevation=["SalesSum"],
                    auto_highlight=True,
                    elevation_scale=100,
                    pickable=True,
                    extruded=True,
                    get_radius=100,
                    get_fill_color=[227, 99, 14],
                    coverage=1
                )
            ]
        ))    

    def plotsalesbychannel(self):
        st.write("Sales By Channel")
        query = """SELECT "Channel", SUM("fs"."Sales")
                    FROM public."Fact-sales" as "fs" left join public."DIM-subchannel" as "schnl" on "fs"."Subchannel_ID" = "schnl"."Subchannel_ID"
                    Group BY "schnl"."Channel"
                    Order By "sum";"""
        self.cur.execute(query)
        result = self.cur.fetchall()
        df = pd.DataFrame(np.array(result),columns=["Channel","Sales"])
        # print(df)
        fig = px.pie(df,names="Channel",values="Sales",title="Sales By Channel")
        st.plotly_chart(fig,use_container_width=True)

    def plotsalesbysub_channel(self):
        st.write("Sales By Sub_Channel")
        query = """SELECT "Sub-channel", SUM("fs"."Sales")
                    FROM public."Fact-sales" as "fs" left join public."DIM-subchannel" as "schnl" on "fs"."Subchannel_ID" = "schnl"."Subchannel_ID"
                    Group BY "schnl"."Sub-channel"
                    Order By "sum";"""
        self.cur.execute(query)
        result = self.cur.fetchall()
        df = pd.DataFrame(np.array(result),columns=["Sub_Channel","Sales"])
        # print(df)
        fig = px.pie(df,names="Sub_Channel",values="Sales",title="Sales By Sub_Channel")
        st.plotly_chart(fig,use_container_width=True)

if __name__=="__main__":
    path = r"C:\Users\Faizan Raza\Desktop\pharmaDE\pharmade\DATA\pharma-data.csv"
    dandcanalysis = distandcustanalysis(path)
    # mainpage.selectjob()
    dandcanalysis.plottopdist()
    dandcanalysis.plottopcust()
    dandcanalysis.plottopcity()
    dandcanalysis.plotsalesbychannel()
    dandcanalysis.plotsalesbysub_channel()