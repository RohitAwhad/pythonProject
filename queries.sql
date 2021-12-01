select DATE(createdat),count(1)  from mask.messages group by DATE(createdat) order by DATE(createdat);

select distinct u.id from mask.users u left join mask.messages m on u.id = m.receiverid where m.receiverid is null;

select to_char(current_timestamp,'yyyy-MM-dd') as today,count(1) from mask.subscriptions where status ='Active' and current_timestamp between startdate and enddate group by to_char(current_timestamp,'yyyy-MM-dd');

select distinct m.senderid from mask.messages m  left join mask.subscriptions s on m.senderid=s.userid where s.userid is null or (s.userid is not null and m.createdat not between s.startdate and s.enddate );

