CREATE TABLE `smsqueue` (
  `uniqueid` varchar(32) NOT NULL DEFAULT '',
  `sent` tinyint(1) NOT NULL DEFAULT '0',
  KEY `PK` (`uniqueid`);

-- select calldate,dst,uniqueid,left(lastdata,27) as DongData, cnum,disposition from cdr where dstchannel like "Dongle%" AND lastdata like "Dongle%" and cnum like "8%" limit 1;
-- +---------------------+-----+--------------+-----------------------------+------------+-------------+
-- | calldate            | dst | uniqueid     | DongData                    | cnum       | disposition |
-- +---------------------+-----+--------------+-----------------------------+------------+-------------+
-- | 2017-02-20 16:52:27 | 191 | 1487598747.4 | Dongle/dongle0/+79510000000 | 8310000000 | ANSWERED    |
-- +---------------------+-----+--------------+-----------------------------+------------+-------------+
-- 1 row in set (0.00 sec)


DELIMITER $

CREATE TRIGGER smsqueue_fill AFTER INSERT on cdr 
FOR EACH ROW 
BEGIN
IF (NEW.dstchannel like "Dongle%" AND NEW.lastdata like "Dongle%" AND NEW.cnum like "8%") 
then
INSERT INTO smsqueue (uniqueid,sent) values( NEW.uniqueid,False );
end if;
END;
$

DELIMITER ;