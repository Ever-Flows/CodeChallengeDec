
/* Create database*/
create database fillnull;
use fillnull;

/*create two tables*/
CREATE TABLE fillnull.Calendar(`datecal` DATE PRIMARY KEY);
CREATE TABLE fillnull.plans(`dateplan` DATE PRIMARY KEY, `plans` varchar(100));

/*insert sample plans data */
insert into fillnull.plans values ( '2017-1-1'  ,   "free trial" );
insert into fillnull.plans values ('2017-1-3'  ,   "advanced" );
insert into fillnull.plans values ( '2017-2-14'  ,  "free trial"  );
insert into fillnull.plans values ('2017-2-28'  ,   "free"  );

/* procedure for fill dates in Calendr table*/
DROP PROCEDURE IF EXISTS filldates;
DELIMITER |
CREATE PROCEDURE filldates(dateStart DATE, dateEnd DATE)
BEGIN
  WHILE dateStart <= dateEnd DO
    INSERT INTO Calendar (datecal) VALUES (dateStart);
    SET dateStart = date_add(dateStart, INTERVAL 1 DAY);
  END WHILE;
END;
|
DELIMITER ;

/* fill the Calendar table with consecutive dates */
CALL filldates('2017-01-01','2017-12-31');

/* join the tables to get composite plans table for entire year - planforcalendaryear*/
create table planforcalendaryear select * from calendar left outer join plans on calendar.datecal = plans.dateplan order by datecal
