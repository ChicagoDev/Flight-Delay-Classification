


-- To update the data on the server:

CREATE view ORD_ALL as
  select "ORD_IB_OB".*
       ,date_trunc('week', to_date("FlightDate", 'YYYY-MM-DD')) as WEEK_BEGIN
     , jetfuel_price.*
    from  "ORD_IB_OB"
      left join jetfuel_price
        on date_trunc('week', to_date("ORD_IB_OB"."FlightDate", 'YYYY-MM-DD'))=date_trunc('week', jetfuel_price.date)
;

create table translate_month (
  month_txt text,
  month_num bigint
);

insert into translate_month (month_txt, month_num) values ('January', 1) , ('February', 2), ('March', 3), ('April', 4), ('May', 5), ('June', 6), ('July', '7'), ('August', 8), ('September', 9), ('October', 10), ('November', 11), ('December', 12);
--
-- Create a sentiment selection that has month encoded as an int
select translate_month.month_num, cnsmr_sntmt_indx.yyyy, cnsmr_sntmt_indx.cons_sent_um from cnsmr_sntmt_indx left join translate_month on cnsmr_sntmt_indx.month=translate_month.month_txt;

create view sentiment_months as select translate_month.month_num, cnsmr_sntmt_indx.yyyy, cnsmr_sntmt_indx.cons_sent_um from cnsmr_sntmt_indx left join translate_month on cnsmr_sntmt_indx.month=translate_month.month_txt;
select * from "ORD_IB_OB" left join sentiment_months on sentiment_months.month_num="ORD_IB_OB"."Month" and sentiment_months.yyyy="ORD_IB_OB"."Year";

------------



-- -- Create the Month translation table
-- create table translate_month (
--   month_txt text,
--   month_num bigint
-- );
--
-- insert into translate_month (month_txt, month_num) values ('January', 1) , ('February', 2), ('March', 3), ('April', 4), ('May', 5), ('June', 6), ('July', '7'), ('August', 8), ('September', 9), ('October', 10), ('November', 11), ('December', 12);
-- --
-- -- Create a sentiment selection that has month encoded as an int
-- select translate_month.month_num, cnsmr_sntmt_indx.yyyy, cnsmr_sntmt_indx.cons_sent_um from cnsmr_sntmt_indx left join translate_month on cnsmr_sntmt_indx.month=translate_month.month_txt;
--
-- create view sentiment_months as select translate_month.month_num, cnsmr_sntmt_indx.yyyy, cnsmr_sntmt_indx.cons_sent_um from cnsmr_sntmt_indx left join translate_month on cnsmr_sntmt_indx.month=translate_month.month_txt;
-- select * from "ORD_IB_OB" left join sentiment_months on sentiment_months.month_num="ORD_IB_OB"."Month" and sentiment_months.yyyy="ORD_IB_OB"."Year";
--
-- ------------
--
--
--
--
--
-- select "ORD_IB_OB".*
--        ,date_trunc('week', to_date("FlightDate", 'YYYY-MM-DD')) as WEEK_START
--      , jetfuel_price.*
--     from  "ORD_IB_OB"
--       left join jetfuel_price
--         on date_trunc('week', to_date("ORD_IB_OB"."FlightDate", 'YYYY-MM-DD'))=date_trunc('week', jetfuel_price.date)
-- ;
