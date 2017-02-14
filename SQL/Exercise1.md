Goals
======================
   1. Explore the Database
   2. Basic Querying - Selecting From Tables
   3. Selecting specific attributes of a table
   4. Where clause/ filtering
   5. Aggregation functions: counting
   6. Aggregation functions: AVG
   7. Intervals, Ranges, and sorting
   8. Subqueries


Loading the database
======================

#Open postgres
Marks-MBP:sql meutband$ psql
psql (9.5.3)
Type "help" for help.

#Create Database readychef
meutband=# CREATE DATABASE readychef;
CREATE DATABASE
meutband=# \q

#Find database and import the database
Marks-MBP:sql meutband$ cd data
Marks-MBP:data meutband$ psql readychef < readychef.sql

`SET
SET
SET
SET
SET
SET
CREATE EXTENSION
COMMENT
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE TABLE
ALTER TABLE
CREATE TABLE
ALTER TABLE
CREATE TABLE
ALTER TABLE
CREATE TABLE
ALTER TABLE
COPY 318120
COPY 1993
COPY 2157
COPY 5524
COPY 514281
REVOKE
REVOKE
GRANT
GRANT
`

#Enter postgress prompt for database readychef
Marks-MBP:data meutband$ psql readychef


Basic Exploration
=================

1. What are the tables in our database?

readychef=# \d

`           List of relations
 Schema |   Name    | Type  |  Owner
--------+-----------+-------+----------
 public | events    | table | postgres
 public | meals     | table | postgres
 public | referrals | table | postgres
 public | users     | table | postgres
 public | visits    | table | postgres
(5 rows)
`

2. What columns does each table have?

readychef=# \d events

`          Table "public.events"
 Column  |       Type        | Modifiers
---------+-------------------+-----------
 dt      | date              |
 userid  | integer           |
 meal_id | integer           |
 event   | character varying |
`

readychef=# \d meals

`          Table "public.meals"
 Column  |       Type        | Modifiers
---------+-------------------+-----------
 meal_id | integer           |
 type    | character varying |
 dt      | date              |
 price   | integer           |
`

readychef=# \d referrals

`     Table "public.referrals"
   Column    |  Type   | Modifiers
-------------+---------+-----------
 referred    | integer |
 referred_by | integer |
`

readychef=# \d users

`            Table "public.users"
   Column    |       Type        | Modifiers
-------------+-------------------+-----------
 userid      | integer           |
 dt          | date              |
 campaign_id | character varying |
`

readychef=# \d visits

`    Table "public.visits"
 Column |  Type   | Modifiers
--------+---------+-----------
 dt     | date    |
 userid | integer |
`

Select statements
===================

1. To get an understanding of the data, run a [SELECT] statement on each table.
Keep all the columns and limit the number of rows to 10.

readychef=# SELECT * FROM events LIMIT 10;

`     dt     | userid | meal_id | event
------------+--------+---------+--------
 2013-01-01 |      3 |      18 | bought
 2013-01-01 |      7 |       1 | like
 2013-01-01 |     10 |      29 | bought
 2013-01-01 |     11 |      19 | share
 2013-01-01 |     15 |      33 | like
 2013-01-01 |     18 |       4 | share
 2013-01-01 |     18 |      40 | bought
 2013-01-01 |     21 |      10 | share
 2013-01-01 |     21 |       4 | like
 2013-01-01 |     22 |      23 | bought
(10 rows)
`

readychef=# SELECT * FROM meals LIMIT 10;

` meal_id |  type   |     dt     | price
---------+---------+------------+-------
       1 | french  | 2013-01-01 |    10
       2 | chinese | 2013-01-01 |    13
       3 | mexican | 2013-01-02 |     9
       4 | italian | 2013-01-03 |     9
       5 | chinese | 2013-01-03 |    12
       6 | italian | 2013-01-03 |     9
       7 | italian | 2013-01-03 |    10
       8 | french  | 2013-01-03 |    14
       9 | italian | 2013-01-03 |    13
      10 | french  | 2013-01-03 |     7
(10 rows)
`

readychef=# SELECT * FROM referrals LIMIT 10;

` referred | referred_by
----------+-------------
       54 |          44
      158 |          80
      184 |         139
      263 |         107
      275 |          35
      279 |           6
      298 |         167
      305 |          59
      311 |          80
      330 |         289
(10 rows)
`

readychef=# SELECT * FROM users LIMIT 10;

` userid |     dt     | campaign_id
--------+------------+-------------
      1 | 2013-01-01 | RE
      2 | 2013-01-01 | PI
      3 | 2013-01-01 | FB
      4 | 2013-01-01 | FB
      5 | 2013-01-01 | FB
      6 | 2013-01-01 | FB
      7 | 2013-01-01 | PI
      8 | 2013-01-01 | FB
      9 | 2013-01-01 | FB
     10 | 2013-01-01 | TW
(10 rows)
`

readychef=# SELECT * FROM visits LIMIT 10;

`     dt     | userid
------------+--------
 2013-01-01 |      3
 2013-01-01 |      7
 2013-01-01 |      8
 2013-01-01 |     10
 2013-01-01 |     11
 2013-01-01 |     15
 2013-01-01 |     18
 2013-01-01 |     19
 2013-01-01 |     20
 2013-01-01 |     21
(10 rows)
`

2. Write a `SELECT` statement that would get just the userids.

readychef=# SELECT userid FROM users;

` userid
--------
      1
      2
      3
      4
      5
      6
      7
      8
      9
     10
     11
     12
     13
     ...
`

3. Maybe you're just interested in what the campaign ids are.
# Note: Pinterest=PI, Facebook=FB, Twitter=TW, and Reddit=RE

readychef=# SELECT DISTINCT campaign_id FROM users;

` campaign_id
-------------
 RE
 FB
 TW
 PI
(4 rows)
`

Where Clauses / Filtering
========================================

1. Write a new `SELECT` statement that returns all rows where `Campaign_ID` is equal to `FB`.

readychef=# SELECT * FROM users WHERE campaign_id = 'FB';

` userid |     dt     | campaign_id
--------+------------+-------------
      3 | 2013-01-01 | FB
      4 | 2013-01-01 | FB
      5 | 2013-01-01 | FB
      6 | 2013-01-01 | FB
      8 | 2013-01-01 | FB
      9 | 2013-01-01 | FB
     12 | 2013-01-01 | FB
     17 | 2013-01-01 | FB
     19 | 2013-01-01 | FB
     24 | 2013-01-01 | FB
              ...
`

2. We don't need the campaign id in the result since they are all the same, so only include the other two columns.

readychef=# SELECT userid, dt FROM users WHERE campaign_id = 'FB';

` userid |     dt
--------+------------
      3 | 2013-01-01
      4 | 2013-01-01
      5 | 2013-01-01
      6 | 2013-01-01
      8 | 2013-01-01
      9 | 2013-01-01
     12 | 2013-01-01
     17 | 2013-01-01
     19 | 2013-01-01
     24 | 2013-01-01
          ...
`

Aggregation Functions
=======================

1. Write a query to get the count of just the users who came from Facebook.

readychef=# SELECT COUNT(1) FROM users WHERE campaign_id = 'FB';

` count
-------
  2192
(1 row)
`

2. Now, count the number of users coming from each service.

readychef=# SELECT campaign_id, count(1) FROM users GROUP BY campaign_id;

` campaign_id | count
-------------+-------
 RE          |   862
 FB          |  2192
 TW          |  1882
 PI          |   588
(4 rows)
`

3. Get the number of unique dates that appear in the `users` table.

readychef=# SELECT count(DISTINCT dt) FROM users;

` count
-------
   352
(1 row)
`

4. Write a query to get the first and last registration date from the `users` table.

readychef=# SELECT MIN(dt), MAX(dt) FROM users;

`    min     |    max
------------+------------
 2013-01-01 | 2013-12-31
(1 row)
`

5. Calculate the mean price for a meal (from the `meals` table). Y

readychef=# SELECT AVG(price) FROM meals;

`         avg
---------------------
 10.6522829904666332
(1 row)
`

6. Now get the average price, the min price and the max price for each meal type.

readychef=# SELECT type, AVG(price), MIN(price), MAX(price) FROM meals GROUP BY type;

`    type    |         avg         | min | max
------------+---------------------+-----+-----
 mexican    |  9.6975945017182131 |   6 |  13
 french     | 11.5420000000000000 |   7 |  16
 japanese   |  9.3804878048780488 |   6 |  13
 italian    | 11.2926136363636364 |   7 |  16
 chinese    |  9.5187165775401070 |   6 |  13
 vietnamese |  9.2830188679245283 |   6 |  13
(6 rows)
`

7. Alias all the above columns to type, avg_price, min_price, max_price

readychef=# SELECT type, AVG(price) AS avg_price, MIN(price) AS min_price, MAX(price) AS max_price
readychef-# FROM meals
readychef-# GROUP BY type;

`    type    |      avg_price      | min_price | max_price
------------+---------------------+-----------+-----------
 mexican    |  9.6975945017182131 |         6 |        13
 french     | 11.5420000000000000 |         7 |        16
 japanese   |  9.3804878048780488 |         6 |        13
 italian    | 11.2926136363636364 |         7 |        16
 chinese    |  9.5187165775401070 |         6 |        13
 vietnamese |  9.2830188679245283 |         6 |        13
(6 rows)
`

8. Maybe you only want to consider the meals which occur in the first quarter (January through March).

readychef=# SELECT type, AVG(price) AS avg_price, MIN(price) AS min_price, MAX(price) AS max_price
readychef-# FROM meals
readychef-# WHERE date_part('year', dt)=2013 AND date_part('month', dt)<=3
readychef-# GROUP BY type;

`    type    |      avg_price      | min_price | max_price
------------+---------------------+-----------+-----------
 mexican    |  9.6951219512195122 |         6 |        13
 french     | 11.7522123893805310 |         7 |        16
 japanese   |  9.6521739130434783 |         6 |        13
 vietnamese |  9.3750000000000000 |         6 |        13
 italian    | 11.0877192982456140 |         7 |        16
 chinese    |  9.7727272727272727 |         6 |        13
(6 rows)
`

9. Modify the above query so that we get the aggregate values for each month and type.

readychef=# SELECT type, date_part('month', dt) AS month, AVG(price) AS avg_price, MIN(price) AS min_price, MAX(price) AS max_price
readychef=# FROM meals
readychef=# WHERE date_part('year', dt)=2013 AND date_part('month', dt)<=3
readychef=# GROUP BY type, month;

`    type    | month |      avg_price      | min_price | max_price
------------+-------+---------------------+-----------+-----------
 italian    |     2 | 11.2666666666666667 |         7 |        16
 chinese    |     1 | 11.2307692307692308 |         8 |        13
 chinese    |     3 |  9.2500000000000000 |         6 |        13
 chinese    |     2 |  9.0666666666666667 |         6 |        13
 italian    |     1 | 10.8030303030303030 |         7 |        16
 italian    |     3 | 11.2666666666666667 |         7 |        16
 vietnamese |     2 |  9.6000000000000000 |         7 |        13
 french     |     1 | 11.6500000000000000 |         7 |        16
 mexican    |     2 |  8.7916666666666667 |         6 |        13
 french     |     3 | 12.5238095238095238 |         8 |        16
 japanese   |     1 |  9.6153846153846154 |         6 |        13
 japanese   |     3 |  9.5238095238095238 |         6 |        13
 mexican    |     1 | 10.3823529411764706 |         6 |        13
 french     |     2 | 10.8387096774193548 |         7 |        16
 mexican    |     3 |  9.6250000000000000 |         6 |        13
 japanese   |     2 |  9.9166666666666667 |         6 |        13
 vietnamese |     1 | 10.8000000000000000 |         6 |        13
 vietnamese |     3 |  8.8235294117647059 |         6 |        13
(18 rows)
`

10. From the `events` table, write a query that gets the total number of buys, likes and shares for each meal id.

readychef=# SELECT meal_id, SUM(CASE WHEN event='bought' THEN 1 ELSE 0 END) as bought,                                   
readychef=# SUM(CASE WHEN event='like' THEN 1 ELSE 0 END) as liked,
readychef=# SUM(CASE WHEN event='share' THEN 1 ELSE 0 END) as shared                                                       readychef=# FROM events                                                                                                 
readychef=# GROUP BY meal_id;

` meal_id | bought | liked | shared
---------+--------+-------+--------
     251 |     13 |    14 |     11
    1074 |     32 |    58 |     60
    1548 |     59 |    90 |    101
     264 |     11 |    26 |     12
     887 |     22 |    45 |     62
     802 |     26 |    62 |     73
    1513 |     46 |   109 |     84
    1070 |     34 |    61 |     73
    1350 |     33 |    69 |     77
    1080 |     28 |    62 |     61
    1209 |     42 |    60 |     85
     496 |     16 |    32 |     36
     455 |     14 |    15 |     26
    1420 |     35 |    68 |     73
     630 |     28 |    52 |     42
    1087 |     34 |    69 |     77
    ...
`

Sorting
==========================================

1. Let's start with a query which gets the average price for each type.

readychef=# SELECT type, AVG(price) AS avg_price FROM meals GROUP BY type;

`    type    |      avg_price
------------+---------------------
 mexican    |  9.6975945017182131
 french     | 11.5420000000000000
 japanese   |  9.3804878048780488
 italian    | 11.2926136363636364
 chinese    |  9.5187165775401070
 vietnamese |  9.2830188679245283
(6 rows)
`

2. To make it easier to read, sort the results by the `type` column.

readychef=# SELECT type, AVG(price) AS avg_price FROM meals GROUP BY type ORDER BY type;

`    type    |      avg_price
------------+---------------------
 chinese    |  9.5187165775401070
 french     | 11.5420000000000000
 italian    | 11.2926136363636364
 japanese   |  9.3804878048780488
 mexican    |  9.6975945017182131
 vietnamese |  9.2830188679245283
(6 rows)
`

3. Now return the same table again, except this time order by the price in descending order

readychef=# SELECT type, AVG(price) AS avg_price FROM meals GROUP BY type ORDER BY avg_price DESC;

`   type    |      avg_price
------------+---------------------
 french     | 11.5420000000000000
 italian    | 11.2926136363636364
 mexican    |  9.6975945017182131
 chinese    |  9.5187165775401070
 japanese   |  9.3804878048780488
 vietnamese |  9.2830188679245283
(6 rows)
`

4. Write a query to get all the meals, but sort by the type and then by the price.

readychef=# SELECT meal_id, type, price FROM meals ORDER BY type, price;

` meal_id |    type    | price
---------+------------+-------
    1108 | chinese    |     6
     562 | chinese    |     6
    1667 | chinese    |     6
    1937 | chinese    |     6
    1932 | chinese    |     6
     418 | chinese    |     6
    1648 | chinese    |     6
    1340 | chinese    |     6
    1228 | chinese    |     6
    1618 | chinese    |     6
    1320 | chinese    |     6
    1957 | chinese    |     6
     683 | chinese    |     6
    ...
`

Joins
=========================

1. Write a query to get one table that joins the `events` table with the `users` table (on `userid`).

readychef=# SELECT users.userid, users.campaign_id, events.meal_id, events.event FROM users
readychef-# JOIN events ON users.userid=events.userid;

` userid | campaign_id | meal_id | event
--------+-------------+---------+--------
      3 | FB          |      18 | bought
      7 | PI          |       1 | like
     10 | TW          |      29 | bought
     11 | RE          |      19 | share
     15 | RE          |      33 | like
     18 | TW          |       4 | share
     18 | TW          |      40 | bought
     21 | RE          |      10 | share
     21 | RE          |       4 | like
     22 | RE          |      23 | bought
     25 | FB          |       8 | bought
     27 | FB          |      29 | like
     28 | TW          |      37 | share
     28 | TW          |      18 | bought
      5 | FB          |      43 | bought
      ...
`

2. Also include information about the meal, like the `type` and the `price`. Only include the `bought` events.

readychef=# SELECT users.userid, users.campaign_id, events.meal_id, meals.type, meals.price
readychef-# FROM users
readychef-# JOIN events ON users.userid=events.userid AND events.event='bought'
readychef-# JOIN meals ON meals.meal_id=events.meal_id;

` userid | campaign_id | meal_id |    type    | price
--------+-------------+---------+------------+-------
      3 | FB          |      18 | french     |     9
     10 | TW          |      29 | italian    |    15
     18 | TW          |      40 | japanese   |    13
     22 | RE          |      23 | mexican    |    12
     25 | FB          |       8 | french     |    14
     28 | TW          |      18 | french     |     9
      5 | FB          |      43 | italian    |    10
      8 | FB          |      39 | french     |    15
     35 | RE          |      35 | italian    |     8
      3 | FB          |      15 | italian    |    11
     17 | FB          |      25 | chinese    |    11
     21 | RE          |      44 | french     |    13
     ...
`

3. Write a query to get how many of each type of meal were bought.

readychef=# SELECT type, COUNT(1) FROM meals
readychef-# JOIN events ON meals.meal_id=events.meal_id AND events.event='bought'
readychef-# GROUP BY type;

`    type    | count
------------+-------
 mexican    |  8792
 french     | 16179
 japanese   |  6921
 italian    | 22575
 chinese    |  6267
 vietnamese |  3535
(6 rows)
`

Subqueries
================================

1. Write a query to get meals that are above the average meal price.

readychef=# SELECT * FROM meals
readychef-# WHERE price > (SELECT AVG(price) FROM meals);

` meal_id |    type    |     dt     | price
---------+------------+------------+-------
       2 | chinese    | 2013-01-01 |    13
       5 | chinese    | 2013-01-03 |    12
       8 | french     | 2013-01-03 |    14
       9 | italian    | 2013-01-03 |    13
      12 | mexican    | 2013-01-03 |    12
      15 | italian    | 2013-01-04 |    11
      16 | italian    | 2013-01-04 |    15
      17 | french     | 2013-01-04 |    15
      19 | japanese   | 2013-01-04 |    11
      21 | vietnamese | 2013-01-04 |    12
      22 | italian    | 2013-01-04 |    12
      23 | mexican    | 2013-01-04 |    12
      24 | japanese   | 2013-01-05 |    11
      ...
`

2. Write a query to get the meals that are above the average meal price *for that type*.

readychef=# SELECT meals.* FROM meals
readychef-# JOIN (SELECT type, AVG(price) AS price FROM meals GROUP BY type) average
readychef-# ON meals.type=average.type AND meals.price>average.price;

` meal_id |    type    |     dt     | price
---------+------------+------------+-------
       2 | chinese    | 2013-01-01 |    13
       5 | chinese    | 2013-01-03 |    12
       8 | french     | 2013-01-03 |    14
       9 | italian    | 2013-01-03 |    13
      12 | mexican    | 2013-01-03 |    12
      16 | italian    | 2013-01-04 |    15
      17 | french     | 2013-01-04 |    15
      19 | japanese   | 2013-01-04 |    11
      21 | vietnamese | 2013-01-04 |    12
      22 | italian    | 2013-01-04 |    12
      23 | mexican    | 2013-01-04 |    12
      24 | japanese   | 2013-01-05 |    11
      25 | chinese    | 2013-01-05 |    11
      ...
`

3. Modify the above query to give a count of the number of meals per type that are above the average price.

readychef=# SELECT meals.type, COUNT(1) FROM meals
readychef=# JOIN (SELECT type, AVG(price) AS price FROM meals GROUP BY type) average
readychef=# ON meals.type=average.type AND meals.price>average.price
readychef=# GROUP BY meals.type;

`    type    | count
------------+-------
 mexican    |   152
 french     |   243
 japanese   |    99
 italian    |   332
 chinese    |    95
 vietnamese |    47
(6 rows)
`

4. Calculate the percentage of users which come from each service.

readychef=# SELECT campaign_id, CAST(COUNT(1) AS REAL) / (SELECT COUNT(1) FROM users) AS percent
readychef-# FROM users GROUP BY campaign_id;

` campaign_id |      percent
-------------+-------------------
 RE          | 0.156046343229544
 FB          | 0.396813902968863
 TW          | 0.340695148443157
 PI          | 0.106444605358436
(4 rows)
`

Extra Credit
========================

1. What user from each campaign bought the most items?

readychef=# WITH user_campaign_count AS (
readychef=# SELECT campaign_id, users.userid, COUNT(1) AS cnt FROM users
readychef=# JOIN events on users.userid=events.userid GROUP BY campaign_id, users.userid)
# Finishes user_campaign_count, start to draw from user_campaign_count

readychef=# SELECT u.campaign_id, u.userid, u.cnt
readychef=# FROM user_campaign_count u
readychef=# JOIN (SELECT campaign_id, MAX(cnt) AS cnt FROM user_campaign_count GROUP BY campaign_id) m
readychef=# ON u.campaign_id=m.campaign_id AND u.cnt=m.cnt ORDER BY u.campaign_id, u.userid;

` campaign_id | userid | cnt
-------------+--------+-----
 FB          |    468 | 303
 PI          |    112 | 338
 RE          |     21 | 371
 TW          |     28 | 316
(4 rows)
`

2. For each day, get the total number of users who have registered as of that day.

readychef=# SELECT a.dt, COUNT(1) FROM (SELECT DISTINCT dt FROM users) a JOIN users b
readychef=# ON b.dt <= a.dt GROUP BY a.dt ORDER BY a.dt;

`     dt     | count
------------+-------
 2013-01-01 |    30
 2013-01-02 |    43
 2013-01-03 |    65
 2013-01-04 |    84
 2013-01-05 |   108
 2013-01-06 |   122
 2013-01-07 |   138
 2013-01-08 |   166
 2013-01-09 |   187
 2013-01-10 |   200
 ...
`

3. What day of the week gets meals with the most buys?

readychef=# SELECt date_part('dow', meals.dt) AS dow, COUNT(1) AS cnt FROM meals
readychef-# JOIN events ON meals.meal_id=events.meal_id AND event='bought'
readychef-# GROUP BY 1 ORDER BY cnt DESC LIMIT 1;

` dow |  cnt
-----+-------
   2 | 10165
(1 row)
`

4. Which month had the highest percent of users who visited the site purchase a meal?

readychef=# SELECT v.month, v.year, CAST(v.cnt AS REAL) / e.cnt AS avg
readychef-# FROM (SELECT date_part('month', dt) AS month, date_part('year', dt) AS year,
readychef(# COUNT(1) AS cnt FROM visits GROUP BY 1,2) v
readychef-# JOIN (SELECT date_part('month', dt) AS month, date_part('year', dt) AS year,
readychef(# COUNT(1) AS cnt FROM events WHERE event='bought' GROUP BY 1,2) as e
readychef-# ON v.month=e.month AND v.year=e.year ORDER BY avg DESC LIMIT 1;

` month | year |       avg
-------+------+------------------
    10 | 2013 | 8.14660438375853
(1 row)
`

5. Find all the meals that are above the average price of the previous 7 days.

readychef=# SELECT a.meal_id FROM meals a JOIN meals b
readychef-# ON b.dt <= a.dt AND b.dt > a.dt - 7
readychef-# GROUP BY a.meal_id, a.price HAVING a.price > AVG(b.price);

` meal_id
---------
    1010
     436
     537
     771
     477
    1421
    1612
     761
     874
    1928
    ...
`

6. What percent of users have shared more meals than they have liked?

readychef=# SELECT CAST(COUNT(1) AS REAL) / (SELECT COUNT(1) FROM users)
readychef-# FROM (SELECT userid FROM events GROUP BY userid
readychef(# HAVING SUM(CASE WHEN event='share' THEN 1 ELSE 0 END) >
readychef(# SUM(CASE WHEN event='like' THEN 1 ELSE 0 END)) t;

`     ?column?
-------------------
 0.463613323678494
(1 row)
`

7. For every day, count the number of users who have visited the site and done no action.

readychef=# SELECT visits.dt, COUNT(1)
readychef-# FROM visits LEFT OUTER JOIN events
readychef-# ON visits.userid=events.userid AND visits.dt=events.dt
readychef-# WHERE events.userid IS NULL GROUP BY visits.dt;

`     dt     | count
------------+-------
 2013-01-01 |     6
 2013-01-02 |     7
 2013-01-03 |    19
 2013-01-04 |    17
 2013-01-05 |    29
 2013-01-06 |    31
 2013-01-07 |    37
 2013-01-08 |    48
 2013-01-09 |    43
 ...
`

8. Find all the dates with a greater than average number of meals.

readychef=# SELECT dt FROM meals GROUP BY dt
readychef-# HAVING COUNT(1) > (SELECT COUNT(1) FROM meals) / (SELECT COUNT(DISTINCT dt) FROM meals);

`    dt
------------
 2013-06-22
 2013-05-06
 2013-06-20
 2013-02-28
 2013-03-29
 2013-10-18
 2013-03-14
 2013-04-16
 2013-08-29
 2013-09-23
 2013-03-06
 2013-03-05
 ...
`

9. Find all the users who bought a meal before liking or sharing a meal.

readychef=# SELECT bought.userid FROM
readychef-# (SELECT userid, MIN(dt) as first FROM events WHERE event='bought' GROUP BY userid) AS bought
readychef-# INNER JOIN (SELECT userid, MIN(dt) AS first FROM events WHERE event IN ('like', 'share')
readychef(# GROUP BY userid) AS like_share
readychef-# ON bought.userid=like_share.userid WHERE bought.first < like_share.first;

` userid
--------
   3028
   2024
   1101
   2247
   1060
   1478
   2150
   4387
   3823
   2452
   2210
   ...
`
