StorLever API Overview 
======================

StorLever highlights its RESTful Style Web API. RESTful Style means the API is based on HTTP 1.1 protocol, 
with JSON content format. All the content of communication data, whether the result or parameters, 
are presented in JSON format. Each resource in Linux system, like file system, block device, and etc, 
has its individual URI to operate on. User should use HTTP standard Method, like GET, PUT, POST, 
on the specific URI to handle the corresponding resource. 

All the resource URIs in StorLever would have the following pattern: 

    http://[host_ip]:[storlever_port]/storlever/api/v1/[sub_path]

Where [host_ip] is IP address of the managed system, [storlever_port] is the listen port of StorLever, 
[sub_path] is the sub path of the specific resource.

HTTP Methods
------------------

StorLever's API supports the following HTTP standard methods with its original meaning. 

1. GET 

    GET method is used to get the information of the specific resource. the response content may be JSON object, 
    or JSON object list, which describe the configuration and running state of the corresponding resource. 
	
2. PUT
    
    PUT method is used to modify the configuration of the resource. The content in the request should be JSON object,
    or JSON object list, with its properties representing the options to be modified. 
    If some options does not need to be changed, the JSON object should omit the property of this option. 

3. POST

    POST method is used to create a new resource in the system.  The content in the request should be JSON object,
    or JSON object list, with its properties representing the configuration options of the new resource.  
	
4. DELETE

    DELETE method is used to delete a resource in the system. 
	
	
Content Type
-----------------

StorLever's API make use of **JSON** as its content type, and UTF-8 as its encoding, 
so the the HTTP request/response should contains the following content type header if presents. 

    Content-Type: application/json; charset=UTF-8

	
Parameter Format
--------------------	
	
To create or modify a resource, user should pack its configuration options into a JSON object, 
then put this JSON object into a HTTP request with POST/PUT method, and send it to the StorLever's Web Server. 

When create a resource, if the corresponding JSON object miss some options of the resource, 
these options would use the default value defined in API. 

When modify a resource, if the corresponding JSON object miss some options of the resource, 
these options would never changed. 

Encoding
------------------

StorLever use **UTF-8** in all its API, and all the characters in the HTTP content should be ascii character


Status Code 
-------------------

StorLever's API use the same status code definition with HTTP protocol in its response. 
The status code used by StorLever currently lists below: 

* 200    Successful
* 201    Create a new resource successfully, and the new resource URI is given in Location header
* 4xx    Client input error
* 5xx    Server Internal error


Error Handling
--------------------

If a error occurs when StorLever processes a request, StorLever would return a response with error status code at once. 
And the content of this response contains a JSON object describing this error, with the following definition. 

+-----------------+----------+------------------------------------------------------------------+
|    Fields       |   Type   |                              Meaning                             |
+=================+==========+==================================================================+
|     info        |  string  |  The text description of the error                               |
+-----------------+----------+------------------------------------------------------------------+
|    exception    |  string  |  The python exception type (for debug)                           |
+-----------------+----------+------------------------------------------------------------------+
|   traceback     |  list    |  calling stack trace back, each entry is of string type and      |
|                 |          |  represent one entry in calling stack. The last entry of list    |
|                 |          |  is the latest position which produce the python exception       |
+-----------------+----------+------------------------------------------------------------------+ 	

CORS
-----------------------

StorLever adopt CORS approach to support AJAX Cross-domain request. 
CORS is a W3C recommendation and supported by all major browsers. 
It makes use of HTTP headers to help browser decide if a cross-domain AJAX request is secure. 
All the HTTP response return by StorLever would contain the following header: 

    Access-Control-Allow-Origin: *


Example Format
------------------------

In the other section of API manual, we give a example shell command to invoke the corresponding API.
We prefer to use curl utility to perform HTTP communication, because curl is the most popular CLI tool of HTTP client in Linux.
User may also choose other utility, like some GUI HTTP tools, to perform the same operation.

