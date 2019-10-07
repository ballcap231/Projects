-- average weather conditions for days with the same congress activity level
create view congress_bills.weather_activities as
(select num_acts, round(avg(temp), 3) as avg_temp, round(avg(hum), 3) as avg_hum, round(avg(wind), 3) as avg_wind from
(select b.num_acts as num_acts, a.temp as temp, a.hum as hum, a.wind as wind
from congress_bills.Weather_cluster a
join
(select acted_at, count(*) as num_acts
from congress_bills.Activity_v4 
group by acted_at) b on a.date=b.acted_at)
group by num_acts
order by num_acts desc)

-- on average it is 1 degree warmer when the senate passes a bill compared to when the house does
create view congress_bills.temp_house_senate as
(select c.avg_house_temp as avg_house_temp, d.avg_senate_temp as avg_senate_temp from 
(select avg(b.temp) as avg_house_temp
from congress_bills.Basic_History_v4 a 
join congress_bills.Weather_cluster b
on a.house_passage_result_at = b.date) c
cross join
(select avg(b.temp) as avg_senate_temp
from congress_bills.Basic_History_v4 a 
join congress_bills.Weather_cluster b
on a.senate_passage_result_at = b.date) d)

-- on average it is 8% more humid on dates the sponsors withdrew the bill than the dates they sponsored it
create view congress_bills.hum_sponsored_withdrawn as
(select c.avg_hum as avg_sponsored_hum, d.avg_hum as avg_withdrawn_hum from 
(select avg(b.hum) as avg_hum
from congress_bills.BillSponsors_v4 a 
join congress_bills.Weather_cluster b
on a.sponsored_at = b.date) c
cross join
(select avg(b.hum) as avg_hum
from congress_bills.BillSponsors_v4 a 
join congress_bills.Weather_cluster b
on a.withdrawn_at = b.date) d)

-- seeing how the average DC temperature at which bills are sponsored for by each state, Guam seems to be in favor of colder temperature at which to sponsor bills
create view congress_bills.sponsors_weather_relation as
(select state,avg(temp) avg_temp,count(temp) count_temp from 
(select s.sponsors_bill_id, s.name,s.state, w.date,w.temp
from `dbfox-230200.congress_bills.Sponsors_01_to_12` s
inner join `dbfox-230200.congress_bills.Weather_cluster` w
on w.date = s.sponsored_at
order by date)
group by state
order by avg_temp)

-- average weather conditions for days with the same congress activity level for bill introductions
create view congress_bills.weather_history_introductions as
(select num_acts, round(avg(temp), 3) as avg_temp, round(avg(hum), 3) as avg_hum, round(avg(wind), 3) as avg_wind from
(select b.num_acts as num_acts, a.temp as temp, a.hum as hum, a.wind as wind
from `dbfox-230200.congress_bills.Weather_cluster` a
join
(select introduced_at, count(*) as num_acts
from `dbfox-230200.congress_bills.Basic_History_v4` 
group by introduced_at) b on a.date=b.introduced_at)
group by num_acts
order by num_acts desc)

-- average weather conditions for days with the same congress activity level for bill sponsors 
create view congress_bills.weather_sponsors as
(select num_acts, round(avg(temp), 3) as avg_temp, round(avg(hum), 3) as avg_hum, round(avg(wind), 3) as avg_wind from
(select b.num_acts as num_acts, a.temp as temp, a.hum as hum, a.wind as wind
from `dbfox-230200.congress_bills.Weather_cluster` a
join
(select sponsored_at, count(*) as num_acts
from `dbfox-230200.congress_bills.BillSponsors_v4` 
group by 	sponsored_at) b on a.date=b.sponsored_at)
group by num_acts
order by num_acts desc)
