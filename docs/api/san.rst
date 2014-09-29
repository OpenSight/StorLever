StorLever SAN API
======================

The following section would describe the API for the SAN server management of StorLever. 
SAN servers in StorLever includes the TGT server(iscsi) for now

StorLever SAN API has the following structure:



* `1 TGT management  <#1-tgt-management>`_
    * `1.1 Get TGT global configuration <#11-get-tgt-global-configuration>`_
    * `1.2 Set TGT global configuration  <#12-set-tgt-global-configuration>`_
    * `1.3 Get target list <#13-get-target-list>`_
    * `1.4 Get a target info <#14-get-a-target-info>`_
    * `1.5 Add target <#15-add-target>`_
    * `1.6 Modify target configuration <#16-modify-target-configuration>`_
    * `1.7 Delete target <#17-delete-target>`_
    * `1.8 Get incoming user list <#18-get-incoming-user-list>`_
    * `1.9 Add incoming user <#19-add-incoming-user>`_
    * `1.10 Modify incoming user password <#110-modify-incoming-user-password>`_
    * `1.11 Delete incoming user <#111-delete-incoming-user>`_
    * `1.12 Get outgoing user list <#112-get-outgoing-user-list>`_
    * `1.13 Add outgoing user <#113-add-outgoing-user>`_
    * `1.14 Modify outgoing user password <#114-modify-outgoing-user-password>`_
    * `1.15 Delete outgoing user <#115-delete-outgoing-user>`_
    * `1.16 Get LUN list <#116-get-lun-list>`_



1 TGT management
------------------

The following operations are used to manage TGT IPSAN server of StorLever. 
StorLever make use of TGT as its IPSAN server implementation in current version. 


1.1 Get TGT global configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This API is used to retrieve the global configuration options of TGT

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/conf

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
    
    A JSON object to describe the global TGT server configuration. 

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/san/tgt/conf



1.2 Set TGT global configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the global configuration of the TGT. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/conf

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +-------------------------+----------+----------+----------------------------------------------------------------+
    |    Fields               |   Type   | Optional |                            Meaning                             |
    +=========================+==========+==========+================================================================+
    |  incomingdiscoveryuser  |  string  | Optional | Define iscsi incoming discovery authentication setting. If it  |
    |                         |          |          | is empty, no authentication is performed. The format is        |
    |                         |          |          | username:passwd Default is unchanged                           | 
    +-------------------------+----------+----------+----------------------------------------------------------------+
    |  outgoingdiscoveryuser  |  string  | Optional | Define iscsi outgoing discovery authentication setting. If it  |
    |                         |          |          | is empty, no authentication is performed. The format is        |
    |                         |          |          | username:passwd Default is unchanged                           | 
    +-------------------------+----------+----------+----------------------------------------------------------------+     
        
    
4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"incomingdiscoveryuser":"test:123456"}' http://192.168.1.15:6543/storlever/api/v1/san/tgt/conf
 

1.3 Get target list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the target iqn list of tgt

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list

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
    
    A JSON list where its each entry is a target IQN string

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list
 
 
1.4 Get a target info
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve one target info, including the configuration and state

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]

    [target_iqn] is the IQN of the target to retrieve

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
    
    A JSON object to describe this target info

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test



1.5 Add target
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to add a new target to TGT server. The new target has the "empty" configuration by default

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list

2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |      iqn        |  string  | Required | new target IQN                                                 |
    +-----------------+----------+----------+----------------------------------------------------------------+


4. Status Code

    201      -   Successful
    
    Others   -   Error

5. Special Response Headers

    The following response header would be added

    Location: [target_url]

    [target_url] is the URL to retrieve the new target info

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"iqn":"iqn.2014-09.com.example:test"}' http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list

    
1.6 Modify target configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to modify a target configuration of TGT.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]

    [target_iqn] is the IQN of the target to modify

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +---------------------+----------+----------+----------------------------------------------------------------+
    |    Fields           |   Type   | Optional |                            Meaning                             |
    +=====================+==========+==========+================================================================+
    |  state              |  string  | Optional | target state, can only set to offline or ready, if present     |
    +---------------------+----------+----------+----------------------------------------------------------------+
    | initiator_addr_list | string[] | Optional | each entry in list is a initiator IP address, like             |
    |                     |          |          | 192.168.1.10.                                                  |
    +---------------------+----------+----------+----------------------------------------------------------------+
    | initiator_name_list | string[] | Optional | each entry in list is a initiator iqn, like                    |
    |                     |          |          | iqn.2014-09.com.example:test_initiator.                        |
    +---------------------+----------+----------+----------------------------------------------------------------+


4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"state": "ready", "initiator_addr_list":["192.168.1.10"]}' http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test
    

1.7 Delete target
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to delete a target of TGT. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]

    [target_iqn] is the IQN of the target to delete

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

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test
    
    

1.8 Get incoming user list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the incoming user list of the specific target

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]/incominguser_list

    [target_iqn] is the IQN of the target    

    
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
    
    A JSON list where its each entry is a incoming user name

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test/incominguser_list


1.9 Add incoming user
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to add a new incoming user to the specific target 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]/incominguser_list

    [target_iqn] is the IQN of the target    

2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |      username   |  string  | Required | new incoming user name                                         |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |      password   |  string  | Required | new incoming user password                                     |
    +-----------------+----------+----------+----------------------------------------------------------------+

    
4. Status Code

    201      -   Successful
    
    Others   -   Error

5. Special Response Headers

    The following response header would be added

    Location: [user_url]

    [user_url] is the URL to operate the new incoming user

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"username":"test", "password":"123456"}' http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test/incominguser_list
    
    
1.10 Modify incoming user password
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to modify a incoming user password

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]/incominguser_list/[user_name]

    [target_iqn] is the IQN of the target to modify
    
    [user_name] is the user name to modify

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +---------------------+----------+----------+----------------------------------------------------------------+
    |    Fields           |   Type   | Optional |                            Meaning                             |
    +=====================+==========+==========+================================================================+
    |      password       |  string  | Required | new incoming user password                                     |
    +---------------------+----------+----------+----------------------------------------------------------------+


4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"password": "123456"}' http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test/incominguser_list/test



1.11 Delete incoming user
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to delete a incoming user

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]/incominguser_list/[user_name]

    [target_iqn] is the IQN of the target 
    
    [user_name] is the user name to delete
    
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

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test/incominguser_list/test
    

1.12 Get outgoing user list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the outgoing user list of the specific target

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]/outgoinguser_list

    [target_iqn] is the IQN of the target    

    
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
    
    A JSON list where its each entry is a outgoing user name

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test/outgoinguser_list


1.13 Add outgoing user
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to add a new outgoing user to the specific target 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]/outgoinguser_list

    [target_iqn] is the IQN of the target    

2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |      username   |  string  | Required | new outgoing user name                                         |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |      password   |  string  | Required | new outgoing user password                                     |
    +-----------------+----------+----------+----------------------------------------------------------------+

    
4. Status Code

    201      -   Successful
    
    Others   -   Error

5. Special Response Headers

    The following response header would be added

    Location: [user_url]

    [user_url] is the URL to operate the new outgoing user

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"username":"test", "password":"123456"}' http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test/outgoinguser_list
    
    
1.14 Modify outgoing user password
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to modify a outgoing user password

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]/outgoinguser_list/[user_name]

    [target_iqn] is the IQN of the target to modify
    
    [user_name] is the user name to modify

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +---------------------+----------+----------+----------------------------------------------------------------+
    |    Fields           |   Type   | Optional |                            Meaning                             |
    +=====================+==========+==========+================================================================+
    |      password       |  string  | Required | new incoming user password                                     |
    +---------------------+----------+----------+----------------------------------------------------------------+


4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"password": "123456"}' http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test/outgoinguser_list/test



1.15 Delete outgoing user
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to delete a outgoing user

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]/outgoinguser_list/[user_name]

    [target_iqn] is the IQN of the target 
    
    [user_name] is the user name to delete
    
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

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test/outgoinguser_list/test
    
    
1.16 Get LUN list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the LUN list of the specific target

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/san/tgt/target_list/[target_iqn]/lun_list

    [target_iqn] is the IQN of the target    

    
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
    
    A JSON list where its each entry is a JSON object describing one LUN configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test/lun_list

        
    



        