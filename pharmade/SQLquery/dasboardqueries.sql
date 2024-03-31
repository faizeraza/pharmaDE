SELECT "Distributor", SUM("fs"."Sales")
	FROM public."Fact-sales" as "fs" left join public."DIM-distributor" as "dist" on "fs"."Distributor_ID" = "dist"."Distributor_ID"
	Group BY "dist"."Distributor"
	Order By "sum" DESC limit 5;
;