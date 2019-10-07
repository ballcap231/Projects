-- find highest bill number per bill type
select bill_type, max(number) as num
from congress_bills.basic_history_mod
group by bill_type
order by num desc

-- list the number of representatives per state who were cosponsors
select cosp_state, count(cosp_title) as num_rep
from `dbfox-230200.congress_bills.CoSponsors`
group by cosp_state, cosp_title
having cosp_title='Rep'
order by num_rep desc

-- list the number of senators per state who were sponsors
select state, count(title) as num_rep
from `dbfox-230200.congress_bills.Sponsors`
group by state, title
having title='Sen'
order by num_rep desc

-- list the number of passed bills per type_reference
select type_reference,  count(bill_id) as num_bills
from `dbfox-230200.congress_bills.Activity`
group by result, type_reference
having result='pass'
order by num_bills desc

-- grouping bills that were acted upon by year and month
select extract(year from acted_at) bill_year,extract(month from acted_at)bill_month, count(extract(month from acted_at)) as count_num
from `dbfox-230200.congress_bills.Activity` 
group by bill_year, bill_month
order by bill_year,bill_month

-- selecting number of different states that cosponsors come from (not equal to 50!)
select count(distinct cosp_state) from congress_bills.CoSponsors


-- getting unique number of districts and parties for sponsors
select count(distinct title) as party_, count(distinct district) as district_
from `congress_bills.sponsor_info`

-- getting unique number of districts and parties for cosponsors, (not equal to sponsors district_; therefore not all sponsors had cosponsors)
select count(distinct cosp_title) as party_, count(distinct cosp_district) as district_
from `congress_bills.cosponsor_info`
