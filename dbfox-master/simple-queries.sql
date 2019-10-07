-- rank bills by descending number of sponsors
SELECT bill_id, name, count(name) AS num_sponsored
FROM congress_bills.sponsors_mod
GROUP BY bill_id, name
ORDER BY count(*) DESC;

-- order dates to see what dates have the most number of bills introduced
SELECT introduced_at, count(*) AS num_bills
FROM congress_bills.basic_history_mod
GROUP BY introduced_at
ORDER BY count(*) DESC;

-- select data where the bill got passed from either senate or house
SELECT * FROM congress_bills.activity_mod
WHERE result='pass';

-- select data of bills that were enacted
SELECT * FROM congress_bills.basic_history_mod
WHERE enacted=true

-- select sponsors from Texas
SELECT * FROM congress_bills.sponsor_info
WHERE state='TX'
ORDER BY district

-- select senators by state
SELECT * FROM congress_bills.cosponsor_info
WHERE cosp_title='Sen'
ORDER BY cosp_state
