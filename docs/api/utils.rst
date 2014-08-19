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
    
* 2 Mail Management 

* 3 SMARTD Management

* 4 Zabbix Agent Management

* 5 SNMP Agent Management



1 NTP Management
------------------

The following operations are used to management NTP configuration of system. 

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
 
 