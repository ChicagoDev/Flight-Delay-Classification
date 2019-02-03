-- Flights from Chicago that were delayed
create table "DLYD_FRM_ORD" as select * from "ORD_IB_OB" where "ArrDelay" > 0 and "Origin" = 'ORD';

-- Flights from Chicago that were not delayed
create table "ON_TM_FRM_ORD" as select * from "ORD_IB_OB" where "ArrDelay" <= 0 and "Origin" = 'ORD';

-- Ensure my date/times are right on Amazon before I go too deep.