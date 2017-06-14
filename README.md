# chan_dongle_Text_message_sender


If you use FreePBX, Asterisk and chan_dongle for connecting calls SIP->GSM, at least in Russia ANI will be gotten form GSM SIM card. To deliver real ANI  I have created script for sending text message with ANI from SIP.

It was tested on Asterisk 11.13.1 and FreePBX 13.

Callflow:
Inbound SIP(real ANI) -> Asterisk(some int ext.) ->chan_dongle(GSM ANI)-> external DNIS.


To install and run systemd unit:
copy to /etc/systemd/system/ and run systemctl daemon-reload;
systemctl enable SMS;
systemctl start SMS;
systemctl status SMS;





To modify cdr DB schema:
mysql -uUSER -ppassword asteriskcdrdb < db_schema.sql

