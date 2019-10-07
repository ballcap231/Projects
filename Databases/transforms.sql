--creating activity table (cleaned and has correct key relationships)
create table congress_bills.activity_mod as
select official_activity_bill_id as bill_id, cast(cast(acted_at as TIMESTAMP) as DATE) as acted_at,
how, reference, type_reference, result, roll, text, type, vote_type, x_where, max(serialid) as serialid
from congress_bills.activity
group by bill_id, acted_at, how, reference, type_reference, result, roll, text, type, vote_type, x_where
order by bill_id
--creating sponsors table (cleaned and has correct key relationships)
create table congress_bills.sponsors_mod as
select sponsors_bill_id as bill_id, concat(name, " (", title, ")") as name, concat(cospons_name, " (", cosp_title, ")") as cospons_name,
sponsored_at, cast(withdrawn_at as TIMESTAMP) as withdrawn_at, serialid
from congress_bills.sponsors
order by bill_id
--creating sponsors info table (cleaned and has correct key relationships)
create table congress_bills.sponsor_info as
select concat(name, " (", title, ")") as name, district, state, thomas_id, title
from congress_bills.sponsors
group by name, district, state, thomas_id, title
order by name
--creating cosponsors info table (cleaned and has correct key relationships)
create table congress_bills.cosponsor_info as
select concat(cospons_name, " (", cosp_title, ")") as cospons_name, cosp_district, cosp_state, cosp_thomas_id, cosp_title
from congress_bills.sponsors
group by cospons_name, cosp_district, cosp_state, cosp_thomas_id, cosp_title
order by cospons_name
--creating basic/history table combined (cleaned and has correct key relationships)
create table congress_bills.basic_history_mod as
select basic_info_bill_id as bill_id, bill_type, number, congress, introduced_at,
house_passage_result, house_passage_result_at, senate_passage_result, senate_passage_result_at, vetoed,
awaiting_signature, enacted, enacted_at
from congress_bills.basic b join congress_bills.history h on basic_info_bill_id = h.bill_history_bill_id
order by bill_id

--extra commands to see relationships in tables
SELECT serialid from congress_bills.sponsors_mod

SELECT distinct bill_id from congress_bills.basic_history_mod

SELECT distinct serialid from congress_bills.activity_mod

select distinct name from congress_bills.sponsor_info

select cospons_name from congress_bills.cosponsor_info

--checking if activity_mod has referential integrity with respect to basic_history_mod
select bhm.*
from congress_bills.activity_mod am 
left join congress_bills.basic_history_mod bhm 
on bhm.bill_id=am.bill_id
where bhm.congress is null

--checking if sponsors_mod has referential integrity with respect to basic_history_mod
select bhm.*
from `congress_bills.sponsors_mod` sm
left join `congress_bills.basic_history_mod` bhm
on bhm.bill_id=sm.bill_id
where bhm.congress is null

--checking if sponsors mod has referential integrity with respect to sponsor info
select sm.*
from `congress_bills.sponsors_mod` sm
left join congress_bills.sponsor_info si
on sm.name = si.name
where si.state is null

--checking if sponsors mod has referential integrity with respect to cosponsor info (should produce no results)
select sm.*
from `congress_bills.sponsors_mod` sm
left join congress_bills.cosponsor_info ci
on sm.cospons_name = ci.cospons_name
where ci.cosp_state is null
