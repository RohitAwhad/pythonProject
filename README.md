# Assignment Details


<b>Coding</b><br>
•	For python code, installation of 2 libraries are compulsory <br>
o	Requests<br>
o	psycopg2 <br>


<b>Approach for anonymization:</b>

Since data privacy is an important aspect in today’s world and PII compliant of data is of utmost importance. To achieve this I have used below approach <br>
•	Create tables users, subscriptions, messages(without message field) with all data and fields present , this data is sensitive and  will be accessible to only DB admin or key stakeholders.<br>
•	For data analytics we will mask our data with schemas and views .<br>
We’re going to hide firstname,lastName,address,zipCode,email(excluding domain),isSmoking,profession while creating a new view of our table that others can use for reporting and analytics.<br><br>
<b>CREATE SCHEMA mask;<br>
CREATE USER analytics;<br>
REVOKE ALL privileges ON SCHEMA public from analytics;</b>

Now we’re going to create our view that has the restricted view of the data with a CREATE VIEW statement.

<b> CREATE VIEW mask.users AS SELECT id,date_part('year',AGE(birthdate)) as age,city,country,substring(email,position('@' in email)+1,char_length(email))
 as email,isSmoking,gender,income,createdAt,updatedAt from users;<br>
CREATE VIEW mask.subscriptions AS SELECT  userid,startdate,enddate,status ,amount,createdat,userupdatedat subscriptions;<br>
CREATE VIEW mask.messages AS SELECT  id,senderid,receiverid,createdat from messages;</b>

Finally we’re going to grant SELECT access to our newly created view to others:<br>

<b>GRANT USAGE ON SCHEMA mask to analytics;<br>
GRANT SELECT ON ALL TABLES IN SCHEMA mask TO analytics;</b><br>

<b><u>DDL for assignment</u></b>:<br>
<b>Users</b><br>


create table if not exists users
(id int primary key,
firstName varchar (100),
lastName varchar (100),
address varchar (250),
city varchar (100),
country varchar (100),
zipCode varchar (100),
email varchar (250),
birthDate timestamp,
gender varchar (100),
isSmoking boolean,
profession varchar (100),
income decimal,
createdAt timestamp,
updatedAt timestamp);

<b>Subscriptions</b><br>

create table if not exists subscriptions
(userid int,
startdate timestamp,
enddate timestamp,
status varchar(100),
amount float,
createdat timestamp,
userupdatedat timestamp,
CONSTRAINT fk_userId FOREIGN KEY(userid) REFERENCES users(id)
);<br>

<b>Messages</b><br>


create table if not exists messages
(id int,
senderid int,
receiverid int,
createdat timestamp );<br>


<b>Below views are used for analytics purpose<b> <br> <br>
<b>CREATE VIEW mask.users AS SELECT id,date_part('year',AGE(birthdate)) as age,city,country,substring(email,position('@' in email)+1,char_length(email))
 as email,isSmoking,gender,income,createdAt,updatedAt from users; <br>
 CREATE VIEW mask.subscriptions AS SELECT  userid,startdate,enddate,status ,amount,createdat,userupdatedat subscriptions;<br>
 CREATE VIEW mask.messages AS SELECT  id,senderid,receiverid,createdat messages;</b><br>

<b>Queries </b> <br>

•	<b>How many total messages are being sent every day?</b><br>
postgres=# select DATE(createdat),count(1)  from mask.messages group by DATE(createdat) order by DATE(createdat);<br>


    date    | count
 2021-11-25 |     3<br>
 2021-11-26 |     2<br>
 2021-11-27 |     5<br>
 2021-11-28 |     1<br>
 2021-11-29 |     1<br>
 2021-11-30 |     1<br>
 2021-12-02 |     1<br>
 2021-12-03 |     1<br>
 2021-12-04 |     3<br>
 2021-12-05 |     1<br>
 2021-12-06 |     1<br>
(11 rows)<br>

•<b>	Are there any users that did not receive any message?</b><br>
postgres=# select distinct u.id from mask.users u left join mask.messages m on u.id = m.receiverid where m.receiverid is null;</<br>

id <br>
---- <br>
  4 <br>
•	<b>How many active subscriptions do we have today?</b><br>
postgres=# select to_char(current_timestamp,'yyyy-MM-dd') as today,count(1) from mask.subscriptions where status ='Active' and current_timestamp between startdate and enddate group by to_char(current_timestamp,'yyyy-MM-dd');<br>
 
 today    | count<br>
 2021-11-30 |     4<br>
 
•	<b>Are there users sending messages without an active subscription? (some extra context for you: in our apps only premium users can send messages).</b><br>
postgres=# select distinct m.senderid from mask.messages m  left join mask.subscriptions s on m.senderid=s.userid where s.userid is null or (s.userid is not null and m.createdat not between s.startdate and s.enddate );<br>

senderid<br>
----------<br>
        6<br>
(1 row) <br>

•	<b>Did you identified any inaccurate/noisy record that somehow could prejudice the data analyses? How to monitor it (SQL query)? Please explain how do you suggest to handle with this noisy data?</b> <br>

one inccurate noisy column which was observed is the birthdate column in users table. In sample data if we calculate age of a person , it comes out to 0 which is incorrect . It can monitor using below query. <br>
 
 <b>Select * from users where date_part('year',AGE(birthdate)) =0</b><br>

Approch I will use:<br>
First will try to check if there are just a few cases which are affected by the , birthdate column or whether this is a wide-spread problem.<br>
Depending on above scenario will take two different actions:

If only a few cases are affected, you can best remove these rows altogether. This way, they will not disturb your analysis. At the same time you will not be left with partial rows that miss some activities because of data quality issues.

If many cases are affected, like in the situation that age calculation of birthdate column were recorded as 0, you can better remove just the columns that have Zero age and keep the rest of the columns from these cases for your analysis. If column is of almost importance for analytics we can derive this column based on profession column or find out root cause or at product level to resolve this abnormalities




