StorLever System API
======================

The following section would describe the API for the system section of StorLever. 
StorLever system API has the following group:

* `System Info <#1-system-info>`_
* Maintenance
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
