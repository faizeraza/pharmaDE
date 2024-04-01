SELECT "ct"."City", SUM("fs"."Sales") as "SalesSum",AVG("ct"."Latitude") as "Latitude",AVG("Longitude") as "Longitude"
                FROM public."Fact-sales" as "fs" left join public."DIM-city" as "ct" on "fs"."City_ID" = "ct"."City_ID"
                Group BY "ct"."City"
                Order By "SalesSum" DESC limit 5;