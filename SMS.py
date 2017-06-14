#!/usr/bin/python

# CREATE TABLE `smsqueue` (
#   `uniqueid` varchar(32) NOT NULL DEFAULT '',
#   `sent` tinyint(1) NOT NULL DEFAULT '0',
#   KEY `PK` (`uniqueid`);

# select calldate,dst,uniqueid,left(lastdata,27) as DongData, cnum,disposition from cdr where dstchannel like "Dongle%" AND lastdata like "Dongle%" and cnum like "8%" limit 1;
# +---------------------+-----+--------------+-----------------------------+------------+-------------+
# | calldate            | dst | uniqueid     | DongData                    | cnum       | disposition |
# +---------------------+-----+--------------+-----------------------------+------------+-------------+
# | 2017-02-20 16:52:27 | 191 | 1487598747.4 | Dongle/dongle0/+79510000000 | 8310000000 | ANSWERED    |
# +---------------------+-----+--------------+-----------------------------+------------+-------------+
# 1 row in set (0.00 sec)


# DELIMITER $

# CREATE TRIGGER smsqueue_fill AFTER INSERT on cdr 
# FOR EACH ROW 
# BEGIN
# IF (NEW.dstchannel like "Dongle%" AND NEW.lastdata like "Dongle%" AND NEW.cnum like "8%") 
# then
# INSERT INTO smsqueue (uniqueid,sent) values( NEW.uniqueid,False );
# end if;
# END;
# $

# DELIMITER ;




import MySQLdb
from MySQLdb.cursors import DictCursor
from time import sleep
import os,sys

# JUST IN CASE WE USE WHITELIST
whitelist=('+79999999999','+79999999991','+79999999992')
# translit to Russian
rus_dict={'ANSWERED': 'otvecheno', 'NO ANSWER':'ne otvechno' }

username="PUTUSERNAME_HERE"
password="verysecretpassword"

db=MySQLdb.connect(user=username,db='asteriskcdrdb',passwd=password)
c=db.cursor(DictCursor)

try:
	c.execute('select 1')
	c.fetchall()
except:
	sys.exit(2)

try:
	while 1:
		c.execute("commit")
		c.execute('select calldate,dst,cdr.uniqueid,left(lastdata,27) as DongData, cnum,disposition from cdr join  smsqueue ON cdr.uniqueid=smsqueue.uniqueid where sent = False and cnum <> ""')

		for record in c.fetchall():
			st="Unknown"
			if rus_dict.has_key(record['disposition']):
				st=rus_dict[record['disposition']]
			(trash, device, did) = record['DongData'].split('/')
			print record
			cmd = "/usr/sbin/asterisk -rx 'dongle sms %(dongle)s %(cellphone)s Vam zvonil %(ani)s. data: %(date)s.'" % { "dongle": device,
																				"cellphone": did,	
																				"ani": record['cnum'],
																				"date": str(record['calldate']),
																				"status": st
																				}
			print cmd
			if did in whitelist:
				res = os.system(cmd)
			else:
				print "Please add to whitelist %s. Skipping the value" % did
				continue
			
			if res == 0:
				c.execute("update smsqueue set sent = True where uniqueid = '%(uniqueid)s'" % record)
				c.execute("commit")
				print "smsqueue with uniqID %(uniqueid)s has been marked as done" % record
		sleep(0.5)

except Exception,e:
	print str(e)
	sys.exit(1)



