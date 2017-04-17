# Connecting to the database

1. First create the database socialmedia:

Marks-MBP:data meutband$ psql
psql (9.5.3)
Type "help" for help.

meutband=# CREATE DATABASE socialmedia;
CREATE DATABASE
meutband=# \q

Marks-MBP:data meutband$ psql socialmedia < socialmedia.sql

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
CREATE TABLE
ALTER TABLE
COPY 15111
COPY 78588
COPY 506019
COPY 104
COPY 1000
COPY 1000
REVOKE
REVOKE
GRANT
GRANT
`
Marks-MBP:data meutband$ psql socialmedia

socialmedia=# \d

`             List of relations
 Schema |     Name      | Type  |  Owner
--------+---------------+-------+----------
 public | friends       | table | postgres
 public | logins        | table | postgres
 public | messages      | table | postgres
 public | optout        | table | postgres
 public | registrations | table | postgres
 public | test_group    | table | postgres
(6 rows)
`

socialmedia=# \d friends

`    Table "public.friends"
 Column  |  Type   | Modifiers
---------+---------+-----------
 userid1 | integer |
 userid2 | integer |
`

socialmedia=# \d logins

`              Table "public.logins"
 Column |            Type             | Modifiers
--------+-----------------------------+-----------
 userid | integer                     |
 tmstmp | timestamp without time zone |
 type   | character varying           |
`

socialmedia=# \d messages

`          Table "public.messages"
  Column   |       Type        | Modifiers
-----------+-------------------+-----------
 sender    | integer           |
 recipient | integer           |
 message   | character varying |
`

socialmedia=# \d optout

`    Table "public.optout"
 Column |  Type   | Modifiers
--------+---------+-----------
 userid | integer |
`

socialmedia=# \d registrations

`           Table "public.registrations"
 Column |            Type             | Modifiers
--------+-----------------------------+-----------
 userid | integer                     |
 tmstmp | timestamp without time zone |
 type   | character varying           |
`

socialmedia=# \d test_group

`       Table "public.test_group"
 Column |       Type        | Modifiers
--------+-------------------+-----------
 userid | integer           |
 grp    | character varying |
`

# Write Some SQL Queries

1. Get the number of users who have registered each day, ordered by date.

socialmedia=# SELECT tmstmp::date AS date, COUNT(1) AS cnt FROM registrations
socialmedia-# GROUP BY date ORDER BY date;

`    date    | cnt
------------+-----
 2013-08-14 |   1
 2013-08-15 |   4
 2013-08-16 |   3
 2013-08-17 |   5
 2013-08-18 |   3
 2013-08-19 |   1
 2013-08-20 |   5
 2013-08-22 |   1
 2013-08-23 |   4
 2013-08-24 |   3
 2013-08-25 |   1
 2013-08-26 |   4
 2013-08-27 |   3
 2013-08-28 |   3
...
`

2. Which day of the week gets the most registrations?

socialmedia=# SELECT EXTRACT(dow FROM tmstmp) AS day_of_week, COUNT(1) AS cnt
socialmedia-# FROM registrations GROUP BY day_of_week ORDER By cnt;

` day_of_week | cnt
-------------+-----
           4 | 125
           5 | 130
           1 | 135
           2 | 146
           3 | 148
           0 | 151
           6 | 165
(7 rows)
`

3. You are sending an email to users who haven't logged in in the week before '2014-08-14' and have not opted out of receiving email. Write a query to select these users.

socialmedia=# SELECT r.userid FROM registrations AS r
socialmedia-# LEFT OUTER JOIN logins AS l
socialmedia-# ON r.userid=l.userid AND l.tmstmp>timestamp '2014-08-07'
socialmedia-# LEFT OUTER JOIN optout AS o ON r.userid=o.userid
socialmedia-# WHERE l.userid IS NULL AND o.userid IS NULL ORDER BY userid;

` userid
--------
     19
     20
     24
     27
     33
     36
     38
     40
     42
     49
     59
     64
     65
     66
     68
     ...
`

4. For every user, get the number of users who registered on the same day as them.

socialmedia=# SELECT a.userid, COUNT(1) FROM registrations a JOIN registrations b
socialmedia-# ON date_part('year', a.tmstmp)=date_part('year', b.tmstmp) AND
socialmedia-# date_part('doy', a.tmstmp)=date_part('doy', b.tmstmp) GROUP BY a.userid;

` userid | count
--------+-------
    251 |     1
    106 |     5
    681 |     3
    285 |     5
    120 |     2
    866 |     4
    887 |     5
    264 |     3
    802 |     4
    ...
`

5. You are running an A/B test and would like to target users who have logged in on mobile more times than web. You should only target users in test group A. Write a query to get all the targeted users.

socialmedia=# SELECT u.userid FROM (SELECT mobile.userid
socialmedia(# FROM (SELECT userid, COUNT(1) AS cnt FROM logins
socialmedia(# WHERE type='mobile' GROUP BY userid) mobile
socialmedia(# JOIN (SELECT userid, COUNT(1) AS cnt FROM logins
socialmedia(# WHERE type='web' GROUP BY userid) web
socialmedia(# ON mobile.userid=web.userid AND mobile.cnt > web.cnt) u
socialmedia-# JOIN test_group t ON u.userid=t.userid AND t.grp='A';

` userid
--------
    106
    866
    887
    264
    802
    664
    647
    497
    455
    630
    209
    ...
`

6. You would like to determine each user's most communicated with user. For each user, determine the user they exchange the most messages with (outgoing plus incoming).

socialmedia=# WITH num_messages AS (
socialmedia(# SELECT a.usr, a.other, a.cnt + b.cnt AS cnt
socialmedia(# FROM (SELECT sender AS usr, recipient AS other, COUNT(1) as cnt
socialmedia(# FROM messages GROUP BY sender, recipient) a
socialmedia(# JOIN (SELECT recipient AS usr, sender AS other, COUNT(1) AS cnt
socialmedia(# FROM messages GROUP BY sender, recipient) b
socialmedia(# ON a.usr=b.usr AND a.other=b.other)

socialmedia-# SELECT num_messages.usr, num_messages.other, cnt FROM num_messages
socialmedia-# JOIN (SELECT usr, MAX(cnt) AS max_cnt FROM num_messages GROUP BY usr) a
socialmedia-# ON num_messages.usr=a.usr AND num_messages.cnt=a.max_cnt ORDER BY usr;

` usr | other | cnt
-----+-------+-----
   0 |   902 |  97
   1 |   352 |  79
   2 |   126 | 100
   2 |   273 | 100
   3 |   270 |  96
   4 |   161 |  80
   5 |   254 |  91
   6 |   290 |  83
   7 |   295 |  50
   8 |   911 | 100
   9 |   790 |  75
   ...
`

7. You could also consider the length of the messages when determining the user's most communicated with friend.

socialmedia=# With message_lengths AS (
socialmedia(# SELECT a.usr, a.other, a.cnt + b.cnt AS cnt
socialmedia(# FROM (SELECT sender AS usr, recipient AS other, COUNT(1) AS cnt
socialmedia(# FROM messages GROUP BY sender, recipient) a
socialmedia(# JOIN (SELECT recipient AS usr, sender AS other, COUNT(1) AS cnt
socialmedia(# FROM messages GROUP BY sender, recipient) b
socialmedia(# ON a.usr=b.usr AND a.other=b.other)
socialmedia-#
socialmedia-# SELECT message_lengths.usr, message_lengths.other, cnt FROM message_lengths
socialmedia-# JOIN (SELECT usr, MAX(cnt) AS max_cnt FROM message_lengths GROUP BY usr) a
socialmedia-# ON message_lengths.usr=a.usr AND message_lengths.cnt=a.max_cnt ORDER BY usr;

` usr | other |  cnt
-----+-------+-------
   0 |   902 |  8789
   1 |   352 |  6492
   2 |   273 | 20391
   3 |   270 |  8316
   4 |   161 | 12041
   5 |   951 | 15595
   6 |   290 | 10297
   7 |   349 |  7887
   8 |   674 |  8357
   9 |   276 | 13879
  10 |   561 | 12432
   ...
`

# Extra Credit

8. Write a query which gets each user, the number of friends and the number of messages received.

### Creates new tables
socialmedia=# CREATE TABLE friends_and_messages AS
socialmedia-# WITH cleaned_friends AS (
socialmedia(# (SELECT userid1, userid2 FROM friends) UNION (SELECT userid2, userid1 FROM friends))
socialmedia-# SELECT f.userid, f.friends, m.messages
socialmedia-# FROM (SELECT userid1 as userid, COUNT(1) AS friends
socialmedia(# FROM cleaned_friends GROUP BY userid1) f
socialmedia-# JOIN (SELECT recipient AS userid, COUNT(1) AS messages
socialmedia(# FROM messages GROUP BY recipient) m ON f.userid=m.userid;

### Runs table
socialmedia=# SELECT * FROM friends_and_messages;

` userid | friends | messages
--------+---------+----------
    251 |      14 |      296
    106 |      14 |      279
    681 |      21 |      340
    120 |      39 |      857
    285 |      18 |      393
    866 |      18 |      434
    264 |      37 |      806
    887 |      25 |      466
    802 |      24 |      454
    601 |      19 |      309
    664 |      19 |      369
    ...
`

9. Break the users into 10 cohorts based on their number of friends and get the average number of messages for each group.

### Get max of number of friends
socialmedia=# SELECT MAX(friends) FROM friends_and_messages;

### Cohort groupings are (1)0-4, (2)5-9, (3)10-14, (4)15-19,
### (5)20-24, (6)25-29, (7)30-34, (8)35-39, (9)40-44, (10)45-49

socialmedia=# SELECT friends/((SELECT MAX(friends) FROM friends_and_messages) / 9)+1 AS cohort, AVG(messages) FROM friends_and_messages GROUP BY 1 ORDER BY 1;

` cohort |         avg
--------+----------------------
      2 | 168.2500000000000000
      3 | 245.2500000000000000
      4 | 335.6000000000000000
      5 | 445.5297297297297297
      6 | 540.8695652173913043
      7 | 652.5549450549450549
      8 | 749.3103448275862069
      9 | 827.0000000000000000
     10 | 854.0000000000000000
(9 rows)
`
