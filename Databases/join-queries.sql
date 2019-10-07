--selecting bill information and their representative
select distinct b.bill_id,bill_type,number,name,s.serialid
from congress_bills.basic_history_mod b
INNER JOIN `congress_bills.sponsors_mod` s 
on b.bill_id = s.bill_id
order by serialid


--selecting which bills were acted on and relative information for the specific bill
select distinct acted_at,how,result,bill_type,number,am.serialid,am.bill_id
from congress_bills.basic_history_mod bhm
INNER JOIN `congress_bills.activity_mod` am 
on bhm.bill_id = am.bill_id
order by bill_id

--joining sponsors info and the cosponsors for them
select si.*,sm.cospons_name
from `congress_bills.sponsor_info` si
INNER JOIN `congress_bills.sponsors_mod` sm
on si.name = sm.name

--selecting all information on representative and the bill they introduced,(if only serial id different, cosponsors were different)
select cbb.bill_id,bill_type,introduced_at,name, cbs.serialid
from `congress_bills.sponsors_mod` cbs 
left JOIN congress_bills.basic_history_mod cbb
on cbb.bill_id = cbs.bill_id


--selecting bill information in common between basic historical info on bills, sponsors and the bills' activity (representative's name and the bill they introduced info)
select distinct cbb.bill_id,bill_type,introduced_at,name,cbs.serialid as cbs_serialid,cba.serialid as cba_serialid
from `congress_bills.basic_history_mod`  cbb
FULL JOIN `congress_bills.sponsors_mod` cbs 
on cbb.bill_id = cbs.bill_id
FULL Join `congress_bills.activity_mod` cba
on cba.bill_id = cbs.bill_id
where cbs.serialid is not null or cba.serialid is not null

--selecting when bill was introduced and acted upon as well as the type
select am.bill_id,bill_type,introduced_at,acted_at,am.serialid
from congress_bills.basic_history_mod bhm
left JOIN `congress_bills.activity_mod` am
on bhm.bill_id = am.bill_id
where am.bill_id is not null
