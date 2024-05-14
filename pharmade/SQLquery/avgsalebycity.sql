SELECT "ct"."City", SUM("fs"."Sales") as "SalesSum",AVG("ct"."Latitude") as "Latitude",AVG("Longitude") as "Longitude"
                FROM public."Fact-sales" as "fs" left join public."DIM-city" as "ct" on "fs"."City_ID" = "ct"."City_ID"
                Group BY "ct"."City"
                Order By "SalesSum" DESC limit 5;

    -- # def selectjob(self):
    -- #     query = """SELECT Distinct("Year") FROM public."Fact-sales";"""
    -- #     self.cur.execute(query)
    -- #     years =["ALL"]
    -- #     years = years+[str(ele[0])[:4] for ele in self.cur.fetchall()]
    -- #     job_filter = st.selectbox("Select the Year", years)
    -- #     # self.cur.close()
    -- #     return job_filter