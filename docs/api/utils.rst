StorLever Utils API
======================

The following section would describe the API for the utils section of StorLever. 
The utils part of StorLever is to manage some common utility tools of the Linux System.

StorLever utils API has the following structure:

* `1 NTP Management <#1-ntp-management>`_
    * `1.1 Get NTP server list <#11-get-ntp-server-list>`_
    * `1.2 Set NTP server list  <#12-set-ntp-server-list>`_
    * `1.3 Get NTP restrict list  <#13-get-ntp-restrict-list>`_
    * `1.4 Set NTP restrict list  <#14-set-ntp-restrict-list>`_
    * `1.5 Get NTP peer list  <#15-get-ntp-peer-list>`_
    
* `2 Mail Management <#2-mail-management>`_
    * `2.1 Get mail configuration <#21-get-mail-configuration>`_
    * `2.2 Set mail configuration <#22-set-mail-configuration>`_
    * `2.3 Send test mail <#23-send-test-mail>`_

* `3 SMARTD Management <#3-smartd-management>`_
    * `3.1 Get monitor list <#31-get-monitor-list>`_
    * `3.2 Set monitor list <#32-set-monitor-list>`_

* `4 Zabbix Agent Management <#4-zabbix-agent-management>`_
    * `4.1 Get basic configuration <#41-get-basic-configuration>`_
    * `4.2 Set basic configuration <#42-set-basic-configuration>`_
    * `4.3 Get active server list <#43-get-active-server-list>`_
    * `4.4 Set active server list <#44-set-active-server-list>`_
    * `4.5 Get passive server list <#45-get-passive-server-list>`_
    * `4.6 Set passive server list <#46-set-passive-server-list>`_    
    
* `5 SNMP Agent Management <#5-snmp-agent-management>`_
    * `5.1 Get basic configuration <#51-get-basic-configuration>`_
    * `5.2 Set basic configuration <#52-set-basic-configuration>`_
    * `5.3 Get community list <#53-get-community-list>`_
    * `5.4 Get a community configuration <#54-get-a-community-configuration>`_
    * `5.5 Add community <#55-add-community>`_
    * `5.6 Modify community <#56-modify-community>`_
    * `5.7 Delete community <#57-delete-community>`_
    * `5.8 Get trap sink list <#58-get-trap-sink-list>`_
    * `5.9 Set trap sink list <#59-set-trap-sink-list>`_
    * `5.10 Get monitor list <#510-get-monitor-list>`_
    * `5.11 Get a monitor configuration <#511-get-a-monitor-configuration>`_
    * `5.12 Add monitor <#512-add-monitor>`_
    * `5.13 Modify monitor <#513-modify-monitor>`_
    * `5.14 Delete monitor <#514-delete-monitor>`_



1 NTP Management
------------------

The following operations are used to manage NTP configuration of system. 

1.1 Get NTP server list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to return all upper NTP server configuration which the local NTP server would connect to

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/ntp/server_list

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON list where its each entry is a JSON object describing one upper NTP server configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/ntp/server_list


1.2 Set NTP server list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the upper NTP Server configuration 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/ntp/server_list

2. HTTP Method
    
    PUT

3. Request Content

    A JSON list where each entry is JSON object with the following definition: 

    
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |  server_addr    |  string  | Required | The server address, it can be a ipv4 address, ipv6 address,    |
    |                 |          |          | or host DNS name                                               |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     ipv6        |   bool   | Optional | If set to True, it would be forced to resolve the host name to |
    |                 |          |          | ipv6 address in DNS resolution. Default is false               |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     prefer      |   bool   | Optional | Marks the server as preferred.  If all other things being      |
    |                 |          |          | equal, this host will be chosen for synchronization among set  | 
    |                 |          |          | of correctly operating hosts. Default is false.                |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     mode        |   int    | Optional | Specifies a mode number which is interpreted in a device       |
    |                 |          |          | specific fashion.	For instance, it selects a dialing, protocol |
    |                 |          |          | in the ACTS driver and a device subtype in the parse drivers.  |
    |                 |          |          | Only valid for reference clock server, i.e. server_addr is     |
    |                 |          |          | 127.127.t.n. Default is 0                                      |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    stratum      |   int    | Optional | Specifies the stratum number assigned to the driver, an        |
    |                 |          |          | integer between 0 and 15. Only valid for reference clock       |
    |                 |          |          | server, i.e. server_addr is 127.127.t.n  Default is 0          |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     flag1       |   int    | Optional | These four flags are used for customizing the clock driver.    |
    |                 |          |          | The interpretation of these values, and whether they are used  |
    |                 |          |          | at all, is a function of the particular clock driver. However, | 
    |                 |          |          | by convention flag4 is used to enable recording monitoring     | 
    |                 |          |          | data to the clockstats file configured with the filegen        |
    |                 |          |          | command.  Further information on the filegen command can be    | 
    |                 |          |          | found in Monitoring Options. Only valid for reference clock    |
    |                 |          |          | server, i.e. server_addr is 127.127.t.n. The valid value is 0  |
    |                 |          |          | or 1, default is 0.                                            |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     flag2       |   int    | Optional | The same                                                       |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     flag3       |   int    | Optional | The same                                                       |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     flag4       |   int    | Optional | The same                                                       |    
    +-----------------+----------+----------+----------------------------------------------------------------+
 

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '[{"server_addr":"0.centos.pool.ntp.org", "prefer":true}]' http://192.168.1.15:6543/storlever/api/v1/utils/ntp/server_list
 
 
 
1.3 Get NTP restrict list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve all the restrict entries for the local NTP server, 
the restrict entry is used for access control.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/ntp/restrict_list

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON list where its each entry is a JSON object describing one restrict configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/ntp/restrict_list


    

1.4 Set NTP restrict list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the restrict list for the local NTP server, 
the restrict entry is used for access control.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/ntp/restrict_list

2. HTTP Method
    
    PUT

3. Request Content

    A JSON list where each entry is JSON object with the following definition: 

    
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |  restrict_addr  |  string  | Required | The restrict address, it can be a ipv4 address, ipv6 address,  |
    |                 |          |          | or   "default"                                                 |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     ipv6        |   bool   | Optional | If set to True, it would be forced to resolve the host name to |
    |                 |          |          | ipv6 address in DNS resolution. Default is false               |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     mask        |  string  | Optional | mask the restrict_addr to indicate the network address. For    |
    |                 |          |          | ipv4, is xxx.xxx.xxx.xxx. for ipv6 is xxxx:xxxx:xxxx::         |
    |                 |          |          | Default is empty, which is equal to 255.255.255.255            |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    ignore       |   bool   | Optional | Deny packets of all kinds, including ntpq and ntpdc            |
    |                 |          |          | queries. Default is false                                      | 
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    nomodify     |   bool   | Optional | Deny ntpq(8) and ntpdc(8) queries which attempt to modify the  |
    |                 |          |          | state of the server (i.e., run time reconfiguration).          |
    |                 |          |          | Queries which return information are permitted. Default is     |
    |                 |          |          | false.                                                         |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     noquery     |   bool   | Optional | Deny ntpq(8) and ntpdc(8) queries. Time service is not         |
    |                 |          |          | affected. Default is false                                     |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     noserve     |   bool   | Optional | Deny all packets except ntpq(8) and ntpdc(8) queries.          |
    |                 |          |          | Default is false                                               |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     notrap      |   bool   | Optional | Decline to provide mode 6 control message trap service to      |
    |                 |          |          | matching hosts.  The trap service is a subsystem of the        |
    |                 |          |          | ntpdq control message protocol which is intended for use       |
    |                 |          |          | by remote event logging programs                               |
    +-----------------+----------+----------+----------------------------------------------------------------+

 

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '[{"restrict_addr":"192.168.1.0", "mask":"255.255.255.0"}]' http://192.168.1.15:6543/storlever/api/v1/utils/ntp/restrict_list
  


1.5 Get NTP peer list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve all the remote NTP server peer status which the local NTP server is communicating with

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/ntp/peer_list

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON list where its each entry is a JSON object describing one peer communication status

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/ntp/peer_list
 
 
2 Mail Management 
------------------

The following operations are used to configure the email sending system (mailx) of system

2.1 Get mail configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the configuration of the mail sending agent (mailx). 
Mail sending agent (mailx) is used to send the mail of the system warning info to administrator for other subsystem of system

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/mail/conf

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON object to describe the mail sending agent configuration. 

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/mail/conf
 
 
2.2 Set mail configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the configuration of the mail sending agent (mailx). 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/mail/conf

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |  email_addr     |  string  | Optional | The email address, like bob@company.com, from which the mail   |
    |                 |          |          | is sent. And it also be the username of your SMTP server.      |
    |                 |          |          | Default is unchanged                                           |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  smtp_server    |  string  | Optional | SMTP server address.  AUTH LOGIN auth method is used           |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  password       |  string  | Optional | user's password for SMTP. Default is unchanged                 |
    +-----------------+----------+----------+----------------------------------------------------------------+


4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"email_addr":"bob@company.com", "smtp_server":"mail.company.com", "password":"bob"}' http://192.168.1.15:6543/storlever/api/v1/utils/mail/conf
 

2.3 Send test mail 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to send a test email to verify whether mail configuration is correct or not


1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/mail/send_mail

2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |  to             |  string  | Required | The email address to send the mail                             |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  subject        |  string  | Required | Email subject                                                  |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  content        |  string  | Optional | mail' content. Default is empty                                |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  debug          |  bool    | Optional | Enable debug mode or not. If enabled, the response would       |
    |                 |          |          | contain the debug message for sending this mail. Default is    |
    |                 |          |          | false                                                          |
    +-----------------+----------+----------+----------------------------------------------------------------+

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON object to describe the debug output message for sending this mail. 

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"to":"bob@company.com", "subject":"test"}' http://192.168.1.15:6543/storlever/api/v1/utils/mail/send_mail
 

 
3 SMARTD Management
----------------------

The following operations are used to configure the SMART (Self-Monitoring, Analysis and Reporting Technology) daemon in system


3.1 Get monitor list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve all monitor configuration entries of SMARTD 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/smartd/monitor_list

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON list where its each entry is a JSON object describing one SMARTD monitor configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/smartd/monitor_list


3.2 Set monitor list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the monitor configuration list of SMARTD

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/smartd/monitor_list

2. HTTP Method
    
    PUT

3. Request Content

    A JSON list where each entry is JSON object with the following definition: 

    
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |      dev        |  string  | Required | block device file path which would be SMART-enabled and        |
    |                 |          |          | monitor. The device must exist in system and support SMART     |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     mail_to     |  string  | Optional | the (e)mail address to which smartd would send when a error is |
    |                 |          |          | detected. To  send email to more than one user, please use the |
    |                 |          |          | following "comma separated" form for the address: user1@add1,  |
    |                 |          |          | user2@add2,...,userN@addN (with no spaces). Default is empty   |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    mail_test    |   bool   | Optional | test the mail. if true, send a single test email immediately   | 
    |                 |          |          | upon smartd startup. This  allows one to verify that email is  |
    |                 |          |          | delivered correctly Default is false.                          |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    mail_exec    |  string  | Optional | run the executable PATH instead of the default mail command.   |
    |                 |          |          | if this list is empty, smartd would run the default            |
    |                 |          |          | "/bin/mail" utility to send warning email to user in "mail_to" |
    |                 |          |          | option. Otherwise, smartd would run the scripts in this        |
    |                 |          |          | option. See man smartd.conf for more detail. Default is empty  |
    +-----------------+----------+----------+----------------------------------------------------------------+
    | schedule_regexp |  string  | Optional | Run Self-Tests or Offline Immediate Tests, at scheduled times. |
    |                 |          |          | A Self or Offline Immediate Test will be run at the end of     |
    |                 |          |          | periodic device polling, if all 12 characters of the string    |
    |                 |          |          | T/MM/DD/d/HH match the extended regular expression REGEXP. See |
    |                 |          |          | man smartd.conf for detail. if this option is empty, no        |
    |                 |          |          | schedule test at all. Default is empty                         |
    +-----------------+----------+----------+----------------------------------------------------------------+

 
4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '[{"dev":"/dev/sda", "mail_to":"bob@company.com", "mail_test":true}]' http://192.168.1.15:6543/storlever/api/v1/utils/smartd/monitor_list
 
 
 
 
4 Zabbix Agent Management
----------------------

The following operations are used to configure the Zabbix (www.zabbix.com) agent 


4.1 Get basic configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
This API is used to retrieve the basic agent configure options in system

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/zabbix_agent/conf

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON object to describe the Zabbix agent basic configuration options. 

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/zabbix_agent/conf

 
4.2 Set basic configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the basic configuration of the Zabbix agent. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/zabbix_agent/conf

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +----------------------+----------+----------+----------------------------------------------------------------+
    |    Fields            |   Type   | Optional |                            Meaning                             |
    +======================+==========+==========+================================================================+
    |  hostname            |  string  | Optional | used for active check, this name must match the hostname set   |
    |                      |          |          | in the active server. Default is unchanged. If it is empty,    |
    |                      |          |          | system default hostname would be used                          |
    +----------------------+----------+----------+----------------------------------------------------------------+
    | refresh_active_check |   int    | Optional | How often list of active checks is refreshed, in seconds. Note |
    |                      |          |          | that after failing to refresh active checks the next refresh   |
    |                      |          |          | will be attempted after 60 seconds. Valid range is 60~3600.    |
    |                      |          |          | Default is unchanged.                                          |
    +----------------------+----------+----------+----------------------------------------------------------------+



4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"hostname":"test_agent1"}' http://192.168.1.15:6543/storlever/api/v1/utils/zabbix_agent/conf    
 

4.3 Get active server list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve active server address list of Zabbix agent.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/zabbix_agent/active_server_list

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON list where its each entry is a address string of active server

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/zabbix_agent/active_server_list
 
 
4.4 Set active server list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the active server address list of Zabbix agent.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/zabbix_agent/active_server_list

2. HTTP Method
    
    PUT

3. Request Content

    A JSON list where each entry is a IP address string of one active server. IP address format is IP:PORT, IP is also can be a DNS name.


 
4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '["192.168.1.20:7890"]' http://192.168.1.15:6543/storlever/api/v1/utils/zabbix_agent/active_server_list
 
 
 

4.5 Get passive server list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve passive server address list of Zabbix agent.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/zabbix_agent/passive_server_list

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON list where its each entry is a address string of active server

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/zabbix_agent/passive_server_list
 
 
4.6 Set passive server list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the passive server address list of Zabbix agent. 
Passive server address is used to restrict which server can query/control Zabbix agent.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/zabbix_agent/passive_server_list

2. HTTP Method
    
    PUT

3. Request Content

    A JSON list where each entry is a IP address string of one pasive server. IP address format is xxx.xxx.xxx.xxx, but also can be a DNS name.


 
4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '["192.168.1.20"]' http://192.168.1.15:6543/storlever/api/v1/utils/zabbix_agent/passive_server_list

    
5 SNMP Agent Management 
----------------------

The following operations are used to manage the SNMP agent, SNMP agent of StorLever only support SNMP 2/2c, not support SNMP 3

5.1 Get basic configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
This API is used to retrieve the basic agent configure options for SNMP agent

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/conf

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON object to describe the SNMP agent basic configuration options. 

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/conf


5.2 Set basic configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the basic configuration of the Zabbix agent. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/conf

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +------------------------------+----------+----------+----------------------------------------------------------------+
    |    Fields                    |   Type   | Optional |                            Meaning                             |
    +==============================+==========+==========+================================================================+
    | sys_location                 |  string  | Optional | set the system location,  system  contact or system name       |
    |                              |          |          | (sysLocation.0, sysContact.0  and  sysName.0).  for the agent  |
    |                              |          |          | respectively.  Ordinarily these objects are writeable via      |
    |                              |          |          | suitably authorized SNMP SET requests if these object are      |
    |                              |          |          | empty,  However, specifying one of these directives makes the  |
    |                              |          |          | corresponding object read-only, and attempts to SET it will    |
    |                              |          |          | result in a notWritable error response. Default is unchanged   |
    +------------------------------+----------+----------+----------------------------------------------------------------+
    | sys_contact                  |  string  | Optional | Described above                                                |
    +------------------------------+----------+----------+----------------------------------------------------------------+
    | sys_name                     |  string  | Optional | Described above                                                |
    +------------------------------+----------+----------+----------------------------------------------------------------+
    | agent_address                |  string  | Optional | defines a list of listening addresses(separated by commas), on |
    |                              |          |          | which to receive incoming SNMP requests.  See the section      |
    |                              |          |          | LISTENING ADDRESSES in the snmpd(8)  manual  page for more     |
    |                              |          |          | information about the format of listening addresses. If it's   |
    |                              |          |          | empty, it would be the default address and port. Default is    |
    |                              |          |          | unchanged                                                      |
    +------------------------------+----------+----------+----------------------------------------------------------------+    
    | iquery_sec_name              |  string  | Optional | specifies the default SNMPv3 username, to be used when making  |
    |                              |          |          | internal queries to retrieve any necessary information (either |
    |                              |          |          | for evaluating the monitored expression, or building a         |
    |                              |          |          | notification payload). These internal queries always use       |
    |                              |          |          | SNMPv3, even if normal querying  of  the  agent  is  done      |
    |                              |          |          | using SNMPv1 or SNMPv2c. This option cannot be empty, default  |
    |                              |          |          | is unchanged                                                   |
    +------------------------------+----------+----------+----------------------------------------------------------------+      
    | link_up_down_notifications   |  bool    | Optional | monitor the interface link up and down. Default is unchanged   |
    +------------------------------+----------+----------+----------------------------------------------------------------+  
    | default_monitors             |  bool    | Optional | enable the default monitors for system. Default is unchanged   |
    +------------------------------+----------+----------+----------------------------------------------------------------+  
    | load_max                     |  float   | Optional | system one minutes load max threshold for default load         |
    |                              |          |          | monitor, if it's 0, this monitor never report error. Default   |
    |                              |          |          | is unchanged                                                   |
    +------------------------------+----------+----------+----------------------------------------------------------------+      
    | swap_min                     |  int     | Optional | swap space min threshold for default memory monitor, in kB     |
    +------------------------------+----------+----------+----------------------------------------------------------------+ 
    | disk_min_percent             |  int     | Optional | disk space min percent for the default disk usage monitor,     |
    |                              |          |          | 0 means never report error. Valid range is 0 ~ 99              |
    +------------------------------+----------+----------+----------------------------------------------------------------+ 
    
4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"sys_name":"test_snmp_agent"}' http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/conf  
 

5.3 Get community list
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the community configuration list of SNMP agent

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/community_list

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON list with each entry is a JSON object describing one community configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/community_list

    
5.4 Get a community configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve one community configuration info of SNMP agent

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/community_list/[community_name]

    [community_name] is the name of the community to retrieve

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON object to describe this community configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/community_list/abc
    
    
5.5 Add community
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to add a new community to SNMP

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/community_list
	
2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    | community_name  |  string  | Required | new community name, SNMP client, which access this agent, must |
    |                 |          |          | match community name                                           |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |      ipv6       |  bool    | Optional | if set to True, it would be forced to resolve the host name to |
    |                 |          |          | ipv6 address in DNS resolution. Default is false               |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     source      |  string  | Optional | restrict access from the specified source.                     |
    |                 |          |          | A restricted source can either be a specific hostname (or      |
    |                 |          |          | address), or a subnet-represented as IP/MASK (e.g.             |
    |                 |          |          | 10.10.10.0/255.255.255.0), or IP/BITS (e.g. 10.10.10.0/24), or |
    |                 |          |          | the IPv6 equivalents. if it's empty, it would give access to   |
    |                 |          |          | any system, that means "global" range. Default is empty.       |
    +-----------------+----------+----------+----------------------------------------------------------------+	
    |     oid         |  string  | Optional | this field restricts access for that community to  the subtree |
    |                 |          |          | rooted at the given OID. if it's empty, the whole tree would   |
    |                 |          |          | be access. Default is empty                                    |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  read_only      |  bool    | Optional | if set to true, this commnunity can only read the oid tree.    |
    |                 |          |          | Or, it can set the the oid tree. Default is false              |
    +-----------------+----------+----------+----------------------------------------------------------------+	


4. Status Code

    201      -   Successful
    
    Others   -   Error

5. Special Response Headers

    The following response header would be added

    Location: [community_url]

    [community_url] is the URL to retrieve the new community info

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"community_name":"abc"}' http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/community_list

    
    
5.6 Modify community
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to modify a community configuration of SNMP agent.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/community_list/[community_name]

    [community_name] is the name of the community to modify

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |      ipv6       |  bool    | Optional | if set to True, it would be forced to resolve the host name to |
    |                 |          |          | ipv6 address in DNS resolution. Default is unchanged           |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     source      |  string  | Optional | restrict access from the specified source.                     |
    |                 |          |          | A restricted source can either be a specific hostname (or      |
    |                 |          |          | address), or a subnet-represented as IP/MASK (e.g.             |
    |                 |          |          | 10.10.10.0/255.255.255.0), or IP/BITS (e.g. 10.10.10.0/24), or |
    |                 |          |          | the IPv6 equivalents. if it's empty, it would give access to   |
    |                 |          |          | any system, that means "global" range. Default is unchanged.   |
    +-----------------+----------+----------+----------------------------------------------------------------+	
    |     oid         |  string  | Optional | this field restricts access for that community to  the subtree |
    |                 |          |          | rooted at the given OID. if it's empty, the whole tree would   |
    |                 |          |          | be access. Default is unchanged                                |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  read_only      |  bool    | Optional | if set to true, this commnunity can only read the oid tree.    |
    |                 |          |          | Or, it can set the the oid tree. Default is unchanged          |
    +-----------------+----------+----------+----------------------------------------------------------------+	

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"read_only": true, "oid":".1.3"}' http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/community_list/abc
    

5.7 Delete community
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to delete a community of SNMP agent

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/community_list/[community_name]

    [community_name] is the name of the community to delete

2. HTTP Method
    
    DELETE

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/community_list/abc
    

5.8 Get trap sink list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve all the trap sink configuration options of SNMP agent. 
When a trap is trigger at SNMP agent, a trap notification would be sent to each host on this list

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/trap_sink_list

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON list where its each entry is a JSON object describing one sink configuration    
    
7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/trap_sink_list


5.9 Set trap sink list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the trap sink list of SNMP agent

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/trap_sink_list

2. HTTP Method
    
    PUT

3. Request Content

    A JSON list where each entry is JSON object with the following definition: 

    
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     host        |  string  | Required | The host IP address                                            |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     type        |  string  | Optional | trap type, can only be set to trap/trap2/inform, which would   |
    |                 |          |          | send SNMPv1 TRAPs, SNMPv2c TRAP2s, or SNMPv2 INFORM            |
    |                 |          |          | notifications respectively. Default is trap                    |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |   community     |  string  | Optional | community name used by this sink, which must match the         |
    |                 |          |          | community setting of the remote host. Default is set to        |
    |                 |          |          | "public"                                                       |
    +-----------------+----------+----------+----------------------------------------------------------------+

 

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '[{"host":"192.168.1.12", "type":"trap2", "community":"test"}]' http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/trap_sink_list


5.10 Get monitor list
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the monitor list of SNMP agent. Monitor is used to trigger SNMP trap of SNMP agent.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/monitor_list

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON list with each entry is a JSON object describing one monitor configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/monitor_list


5.11 Get a monitor configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve one monitor info of SNMP agent

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/monitor_list/[monitor_name]

    [monitor_name] is the name of the monitor to retrieve

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    A JSON object to describe this monitor configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/monitor_list/test_monitor
    
    
5.12 Add monitor
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to add a new monitor to SNMP agent

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/monitor_list
	
2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |  monitor_name   |  string  | Required | new monitor name                                               |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    option       |  string  | Optional | options to control the monitor's behavior, see monitor option  |
    |                 |          |          | section of man snmpd.conf for more detail. Default is empty    |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  expression     |  string  | Required | expression to check of this monitor, see monitor expression of |
    |                 |          |          | man snmpd.conf for more detail                                 |
    +-----------------+----------+----------+----------------------------------------------------------------+	

    

4. Status Code

    201      -   Successful
    
    Others   -   Error

5. Special Response Headers

    The following response header would be added

    Location: [monitor_url]

    [monitor_url] is the URL to retrieve the new monitor info

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"monitor_name":"test_monitor", "expression":".1.3.4"}' http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/monitor_list

    
    
5.13 Modify monitor
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to modify a monitor of SNMP agent.

1. Resource URI


    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/monitor_list/[monitor_name]

    [monitor_name] is the name of the monitor to retrieve


2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |    option       |  string  | Optional | options to control the monitor's behavior, see monitor option  |
    |                 |          |          | section of man snmpd.conf for more detail. Default is          |
    |                 |          |          | unchanged.                                                     |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  expression     |  string  | Optional | expression to check of this monitor, see monitor expression of |
    |                 |          |          | man snmpd.conf for more detail. Default is unchanged           |
    +-----------------+----------+----------+----------------------------------------------------------------+	

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"expression":".1.3.8"}' http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/monitor_list/test_monitor


5.14 Delete monitor
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to delete a monitor of SNMP agent

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/utils/snmp_agent/monitor_list/[monitor_name]

    [monitor_name] is the name of the monitor to delete

2. HTTP Method
    
    DELETE

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/utils/snmp_agent/monitor_list/test_monitor
  

    
    

    