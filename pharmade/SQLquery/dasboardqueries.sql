SELECT "Distributor", SUM("fs"."Sales")
	FROM public."Fact-sales" as "fs" left join public."DIM-distributor" as "dist" on "fs"."Distributor_ID" = "dist"."Distributor_ID"
	Group BY "dist"."Distributor"
	Order By "sum" DESC limit 5;
;
-- seles by month 
SELECT "dm"."Month",SUM("fs"."Sales") as "SumOfSales" FROM public."Fact-sales" 
as "fs" left join public."DIM-month" as "dm" on "fs"."Month_ID" = "dm"."Month_ID" 
GROUP BY "dm"."Month" 
ORDER BY "SumOfSales" desc;

-- sales by channel
SELECT "Channel", SUM("fs"."Sales")
FROM public."Fact-sales" as "fs" left join public."DIM-subchannel" as "schnl" on "fs"."Subchannel_ID" = "schnl"."Subchannel_ID"
Group BY "schnl"."Channel"
Order By "sum";