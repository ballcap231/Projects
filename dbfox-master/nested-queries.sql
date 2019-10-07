-- find the bills that took a longer than average time between the introduction and enactment of the bill
select bill_id, introduced_at, enacted_at, date_diff(enacted_at,introduced_at,day) as intro_enact from congress_bills.basic_history_mod
where date_diff(enacted_at,introduced_at,day) >
(select avg(intro_enact) as avg_diff from 
  (select date_diff(enacted_at,introduced_at,day) as intro_enact
  from congress_bills.basic_history_mod
  where enacted = true))
order by intro_enact desc

-- find the number of activities per bill type
select bill_type, count(a.bill_id) as act_passed
from congress_bills.basic_history_mod a join
(select *
from congress_bills.Activity
where result='pass') b
on a.bill_id = b.bill_id
group by a.bill_type
order by act_passed desc
   
-- find all the sponsors with the same last name
select distinct first, last
from congress_bills.Sponsors join
(select first as f, last as l
from congress_bills.Sponsors)
on last = l
where first != f
order by last
 
-- find the cosponsors with the most common first name
select * from congress_bills.CoSponsors 
where cosp_first in 
(select cosp_first from congress_bills.CoSponsors 
group by cosp_first
order by  count(cosp_last) desc limit 1)


-- selecting all dates that from bills in basic table that were introduced with a count greater than the average (not enactment time but rather number of times introduced)
select introduced_at, count
from (select introduced_at, count(*) count
from congress_bills.basic
group by introduced_at)
where count > 
(select avg(count) avg from 
(select introduced_at, count(*) count
from congress_bills.basic
group by introduced_at))

-- selecting all possible combinations of cosponsors and sponsors who live in Texas
select f,l,cf,cl, state
from 
(select distinct first f, last l,cosp_first cf,cosp_last cl, sp.state
from congress_bills.Sponsors sp join congress_bills.CoSponsors cosp
on cosp.cosp_state =  sp.state)
where state = 'TX'


-- selecting all bills and pertinent info for which their text or "comment" field is not common (less than average) 
-- (only showing text in datastudio, as that is the only interesting field to graph)
(select distinct text, count
from 
(select text, count(*) count
from congress_bills.Activity
group by text)
where count <
(select avg(count) avg
from (select text, count(*) count
from congress_bills.Activity
group by text)))

-- selecting districts shared between cosponsors and sponsors for which they have the same title (Rep or Sen, etc...)
select district, title from 
(select distinct cosp_first,cosp_last,first,last,district,sp.title, cosp.cosp_title
from congress_bills.CoSponsors cosp join congress_bills.Sponsors sp
on cosp.cosp_district = sp.district)
where title = cosp_title

