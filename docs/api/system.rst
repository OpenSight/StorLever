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
    * `2.9 Download system log <#29-download-system-log>`_
* `3 Statistic Info <#3-statistic-info>`_ 
    * `3.1 Get total CPU times <#31-get-total-cpu-times>`_
    * `3.2 Get per CPU times <#32-get-per-cpu-times>`_
    * `3.3 Get total Disk IO Counter <#33-get-total-disk-io-counter>`_
    * `3.4 Get per Disk IO Counter <#34-get-per-disk-io-counter>`_
    * `3.5 Get total Network IO Counter <#35-get-total-network-io-counter>`_
    * `3.6 Get per Network IO Counter <#36-get-per-network-io-counter>`_   
* `4 Configuration Management <#4-configuration-management>`
    * `4.1 Download configuration <#41-download-configuration>`
    * `4.2 Upload configuration <#42-upload-configuration>`
    * `4.3 Clear configuration <#43-clear-configuration>`
    * `4.4 Backup configuration <#44-backup-configuration>`
    * `4.5 Restore configuration <#45-restore-configuration>`
* User Management 
* Service Management
* Module Management



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


3 Statistic Info
------------------

The following operations are used to retrieve some statistic info from the system


3.1 Get total CPU times
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the total CPU time (in seconds) in each working mode. 
User can make use this API to measure each working mode's 
occupation percent for a specific period.

This API is more user-friendly than the measuring CPU usage by StorLever. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/cpu_times

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
    
    A JSON object to describe the total CPU time (in seconds, float type) in each mode

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/cpu_times
	

3.2 Get per CPU times
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the per CPU time (in seconds) in each working mode. 
User can make use this API to measure each working mode's 
occupation percent for a specific period for each CPU.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/per_cpu_times

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
    
    A JSON list where each entry is JSON object to describe each CPU time (in seconds) in each mode 

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/per_cpu_times


3.3 Get total Disk IO Counter
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the disk IO counter for all disk in the system.
User can make use this API to measure the total disk IO in the specific period. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/disk_io_counters

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
    
    A JSON object to describe each IO counter for all the disk device

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/disk_io_counters
	

3.4 Get per Disk IO Counter
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the disk IO counter for each disk device in the system.
User can make use this API to measure the disk IO for each disk device in the specific period. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/per_disk_io_counters

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
    
    A JSON list with each entry to describe each IO counter for each disk device

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/per_disk_io_counters	
	


3.5 Get total Network IO Counter
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the network IO counter for all interface in the system.
User can make use this API to measure the total network IO in the specific period. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/net_io_counters

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
    
    A JSON object to describe each IO counter for all network interface

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/net_io_counters
	

3.6 Get per Network IO Counter
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the network IO counter for each network interface in the system.
User can make use this API to measure the network IO for each network interface in the specific period. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/per_net_io_counters

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
    
    A JSON list with each entry to describe each IO counter for each network interface

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/per_net_io_counters
	

4 Configuration Management
------------------

The following operations are used to handle the configuration of StorLever

4.1 Download configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to download the configuration file from StorLever, the configuration file 
is of the form of tar.gz, which includes all the files and directory structure related to StorLever.
User can download the configuration to verify or backup for future configuration restore


1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/conf_tar

2. HTTP Method
    
    GET

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    Others   -   Error

5. Special Response Headers
	
    The following response header would be added
    
    * Content-Type: application/force-download

    This header is used to tell the browser that the context in response is to download and save as a file, 
    not for display. 

    * Content-Disposition: attachment; filename=%s
	
    This header is to give the filename info about the download file

6. Response Content
    
    A tar.gz file which contains all the configuration file about StorLever

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/system/conf_tar > storlever_conf.tar.gz
	

4.2 Upload configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to upload the configuration file to StorLever, the configuration file 
must be a tar.gz file which is download from StorLever before.


1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/conf_tar

2. HTTP Method
    
    PUT

3. Request Content

    A tar.gz file

4. Status Code

    200      -   Successful
    Others   -   Error

5. Special Response Headers
	
    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT --data-binary @storlever_conf.tar.gz http://192.168.1.15:6543/storlever/api/v1/system/conf_tar


4.3 Clear configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to clear the application server configuration of StorLever, 
which reset them to init state. These configuration to reset restricts to application configuration, exclude:

1) block device configuration
2) system related configuration
3) network related configuration


1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/conf_tar

2. HTTP Method
    
    DELETE

3. Request Content

    NULL

4. Status Code

    200      -   Successful
    Others   -   Error

5. Special Response Headers
	
    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/system/conf_tar


4.4 Backup configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to back up the configuration to the specific path in the system


1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/backup_conf

2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     file        |  string  |   No     | The file path name to save the configuration, it would be of   |
	|                 |          |          | form of tar.gz
    +-----------------+----------+----------+----------------------------------------------------------------+

4. Status Code

    200      -   Successful
    Others   -   Error

5. Special Response Headers
	
    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"file":"/root/storlever.tar.gz"}' http://192.168.1.15:6543/storlever/api/v1/system/backup_conf


4.5 Restore configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to restore the configuration with the specific file in the system. 
This file must exists and should be the back up from StorLever before


1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/system/restore_conf

2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     file        |  string  |   No     | The file path to restore from                                  |
    +-----------------+----------+----------+----------------------------------------------------------------+

4. Status Code

    200      -   Successful
    Others   -   Error

5. Special Response Headers
	
    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"file":"/root/storlever.tar.gz"}' http://192.168.1.15:6543/storlever/api/v1/system/restore_conf






	

	