StorLever System API
======================

The following section would describe the API for the system section of StorLever. 
StorLever system API has the following structure:

* `1 System Info <#1-system-info>`_
    * `1.1 Get General System Info <#11-get-general-system-info>`_
    * `1.2 Configure the Host Name  <#12-configure-the-host-name>`_
    * `1.3 Get CPU info  <#13-get-cpu-info>`_
    * `1.4 Measure total CPU usage percent  <#14-measure-total-cpu-usage-percent>`_
    * `1.5 Measure per CPU usage percent  <#15-measure-per-cpu-usage-percent>`_
    * `1.6 Get Memory info  <#16-get-memory-info>`_
    * `1.7 Get process list <#17-get-process-list>`_
* `2 Maintenance <#2-maintenance>`_
    * `2.1 Flush page cache <#21-flush-page-cache>`_
    * `2.2 Get SELinux state <#22-get-selinux-state>`_
    * `2.3 Set SELinux state <#23-set-selinux-state>`_
    * `2.4 Get system date time <#24-get-system-date-time>`_
    * `2.5 Set system date time <#25-set-system-date-time>`_
    * `2.6 Get system timestamp <#26-get-system-timestamp>`_
    * `2.7 Power off system <#27-power-off-system>`_
    * `2.8 Reboot system <#28-reboot-system>`_
    * `2.9 Download system log <#29-download-system>`_	
* Statistic Info
* User Management 
* Service Management
* Module Management
* Configuration Management


1 System Info
------------------

The following operations are used to Get/Set system general information.

1.1 Get General System Info
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/localhost

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
    
    A JSON object to describe the system general information. 

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/localhost
	
	

1.2 Configure the Host Name 
~~~~~~~~~~~~~~~~~~~~~~~~~~~	

This API is used to set the host name to a special string, 
and the new name would be add to hosts list with 127.0.0.1 automatically

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/localhost

2. HTTP Method
    
    PUT
	
3. Request Content

    A JSON object with the following field definition. 
	
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     hostname    |  string  |   Yes    | The host name of the remote system. If absent, the host name   |
    |                 |          |          | would not be changed                                           |
    +-----------------+----------+----------+----------------------------------------------------------------+
	
4. Status Code

    200      -   Successful
    Others   -   Error	
	
5. Special Response Headers
	
    No	
	
6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"hostname":"localhost"}' http://192.168.1.15:6543/storlever/api/v1/system/localhost



1.3 Get CPU info 
~~~~~~~~~~~~~~~~~~~~~~~~~~~	

This API is used to get the cpu info, like model, frequency, cache, 
in system

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/cpu_list

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
    
    A JSON object to describe the CPU info. 

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/cpu_list
	

1.4 Measure total CPU usage percent 
~~~~~~~~~~~~~~~~~~~~~~~~~~~	

This API is used to measure the CPU usage percent in the given interval, and return the 
measure result

Note: the response would return in your given interval time


1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/cpu_percent

2. HTTP Method
    
    GET
	
3. Request Content

    A JSON object with the following field definition. 
	
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     interval    |  number  |   Yes    | The measure time in seconds. If absent, default to 1 sec       |
    +-----------------+----------+----------+----------------------------------------------------------------+
	
4. Status Code

    200      -   Successful
    Others   -   Error	
	
5. Special Response Headers
	
    No	
	
6. Response Content
    
    A JSON number to indicate the usage percent of total CPU

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/cpu_percent


1.5 Measure per CPU usage percent 
~~~~~~~~~~~~~~~~~~~~~~~~~~~	

This API is used to measure the each CPU usage percent in the given interval, and return the 
measure result

Note: the response would return in your given interval time

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/per_cpu_percent

2. HTTP Method
    
    GET
	
3. Request Content

    A JSON object with the following field definition. 
	
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     interval    |  number  |   Yes    | The measure time in seconds. If absent, default to 1 sec       |
    +-----------------+----------+----------+----------------------------------------------------------------+
	
4. Status Code

    200      -   Successful
    Others   -   Error	
	
5. Special Response Headers
	
    No	
	
6. Response Content
    
    A JSON list to indicate the usage percent of per CPU

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/per_cpu_percent	



1.6 Get Memory info 
~~~~~~~~~~~~~~~~~~~~~~~~~~~	

This API is used to get the memory usage info, the return value is presented in byte unit.


1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/memory

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
    
    A JSON object to describe the memory usage info, present in bytes

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/memory
	


1.7 Get process list
~~~~~~~~~~~~~~~~~~~~~~~~~~~	

This API is used to retrieve the current running process list in system

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/ps

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
    
    A JSON list where its each entry is a JSON object describing one process running info

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/ps
	

2 Maintenance
------------------

The following operations are used to maintain the system

2.1 Flush page cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to flush out all the page cache of system. After that, the page cache would be recycled to free memory

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/flush_page_cache

2. HTTP Method
    
    POST
	
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

    curl -v -X POST http://192.168.1.15:6543/storlever/api/v1/system/flush_page_cache
	
	
2.2 Get SELinux state
~~~~~~~~~~~~~~~~~~~~~~~~~~~

SELinux is a access control tool in Linux. With it, many storage task would be failed. 
StorLever realize this fact and provide API to monitor & control SELinux state

This API is used to retrieve the current SELinux running info including state

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/selinux

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
    
    A JSON object to describe the SELinux running info

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/selinux

	
2.3 Set SELinux state
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to control the SELinux running state. After the state is changed, 
administrator must restart the system to make it in effect

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/selinux

2. HTTP Method
    
    PUT
	
3. Request Content

    A JSON object with the following field definition. 
	
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     state       |  string  |   Yes    | can only be enforcing|permissive|disabled. If absent,          |
    |                 |          |          | the state would not be changed                                 |
    +-----------------+----------+----------+----------------------------------------------------------------+

4. Status Code

    200      -   Successful
    Others   -   Error	
	
5. Special Response Headers
	
    No	
	
6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"state":"disabled"}' http://192.168.1.15:6543/storlever/api/v1/system/selinux	
	
	
2.4 Get system date time
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to get the current date and time in the system

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/datetime

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
    
    A JSON object to describe the system date & time in ISO format

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/datetime
	

2.5 Set system date time
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the date and time in the system

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/datetime

2. HTTP Method
    
    PUT
	
3. Request Content

    A JSON object with the following field definition. 
	
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     datetime    |  string  |   No     | date and time in ISO format, e.g YYYY-MM-DDThh:mm:ss[+HHMM]    |
    +-----------------+----------+----------+----------------------------------------------------------------+

4. Status Code

    200      -   Successful
    Others   -   Error	
	
5. Special Response Headers
	
    No	
	
6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"datetime":"2014-07-18T10:55:37+0800"}' http://192.168.1.15:6543/storlever/api/v1/system/datetime	
	

2.6 Get system timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the time from from Epoch, measure in seconds

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/timestamp

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
    
    A JSON object to describe the timestamp in its timestamp field

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/timestamp
	
	
2.7 Power off system
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to power off the system. In one seconds after response is return,
the system would start power off procedure

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/poweroff

2. HTTP Method
    
    POST
	
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

    curl -v -X POST http://192.168.1.15:6543/storlever/api/v1/system/poweroff
	
	
2.8 Reboot system
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to reboot the system. In one seconds after response is return,
the system would start reboot procedure

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/reboot

2. HTTP Method
    
    POST
	
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

    curl -v -X POST http://192.168.1.15:6543/storlever/api/v1/system/reboot
	
	
	
2.9 Download system log
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to download the system log. The system /var/log directory would tar and gzip, 
then return in response. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/log_download

2. HTTP Method
    
    GET
	
3. Request Content

    NULL

4. Status Code

    200      -   Successful
    Others   -   Error	
	
5. Special Response Headers
	
    The following header would be in response:
	
    Content-Type: application/force-download	
	
	Content-Type header indicate this response include a file download content
	
	Content-Disposition: attachment; filename=%s
	
	Content-Disposition header give extra infomation about the response content, like filename.
	
6. Response Content
    
    The tar.gz file content

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/log_download
	