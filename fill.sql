create database dbo;
use dbo;
CREATE TABLE dbo.Calendar(`d` DATE PRIMARY KEY);
CREATE TABLE dbo.plans(`dd` DATE PRIMARY KEY, `plans` varchar(100));

insert into dbo.plans values ( '2017-1-1'  ,   "free trial" );
insert into dbo.plans values ('2017-1-3'  ,   "advanced" );
insert into dbo.plans values ( '2017-2-14'  ,  "free trial"  );
insert into dbo.plans values ('2017-2-28'  ,   "free"  );


DROP PROCEDURE IF EXISTS filldates;
DELIMITER |
CREATE PROCEDURE filldates(dateStart DATE, dateEnd DATE)
BEGIN
  WHILE dateStart <= dateEnd DO
    INSERT INTO Calendar (d) VALUES (dateStart);
    SET dateStart = date_add(dateStart, INTERVAL 1 DAY);
  END WHILE;
END;
|
DELIMITER ;
CALL filldates('2017-01-01','2016-12-31');

create table test select * from calendar left outer join plans on calendar.d = plans.dd order by d 

DROP PROCEDURE IF EXISTS Ree;
DELIMITER |
create procedure Ree()
BEGIN
  DECLARE cursor_ID INT;
  DECLARE cursor_VAL VARCHAR(1);
  DECLARE done INT DEFAULT FALSE;
  
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  DECLARE varc1 INT DEFAULT 0;
  DECLARE varc2 INT DEFAULT 0;
  DECLARE varc3 INT DEFAULT 0;
  DECLARE cursor_i CURSOR FOR SELECT plans FROM test;
  OPEN cursor_i;
	read_loop: LOOP
    FETCH cursor_i INTO varc1;
    IF done THEN
      LEAVE read_loop;
    END IF;
    if varc1 is not null then
		 set varc2 = varc1;
	else
		update test set plans=varc2 ;
	end if;
  END LOOP;
  CLOSE cursor_i;
END;
|
DELIMITER ;

CALL Ree();