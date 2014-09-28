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

* `2 NFS Management <#2-nfs-management>`_
    * `2.1 Get NFS export list <#21-get-nfs-export-list>`_
    * `2.2 Get a export point configuration <#22-get-a-export-point-configuration>`_
    * `2.3 Add export point <#23-add-export-point>`_
    * `2.4 Modify export point <#24-modify-export-point>`_
    * `2.5 Delete export point <#25-delete-export-point>`_

* `3 Samba Management <#3-samba-management>`_
    * `3.1 Get global configuration <#31-get-global-configuration>`_
    * `3.2 Set global configuration <#32-set-global-configuration>`_
    * `3.3 Get share list <#33-get-share-list>`_
    * `3.4 Get a share configuration <#34-get-a-share-configuration>`_
    * `3.5 Add share <#35-add-share>`_
    * `3.6 Modify share <#36-modify-share>`_
    * `3.7 Delete share <#37-delete-share>`_
    * `3.8 Get connection list <#38-get-connection-list>`_
    * `3.9 Get account list <#39-get-account-list>`_
    * `3.10 Add account <#310-add-account>`_
    * `3.11 Modify account <#311-modify-account>`_
    * `3.12 Delete account <#312-delete-account>`_
    



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

    Location: [user_url]

    [user_url] is the URL to retrieve the new target info

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
    | initiator_name_list | string[] | Optional | each entry in list is a initiator iqn, like             |
    |                     |          |          | iqn.2014-09.com.example:test_initiator.                                                  |
    +---------------------+----------+----------+----------------------------------------------------------------+


4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"state": ready, "initiator_addr_list":["192.168.1.10"]}' http://192.168.1.15:6543/storlever/api/v1/san/tgt/target_list/iqn.2014-09.com.example:test
    

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
    


    
    

2 NFS Management
------------------

The following operations are used to manage NFS export 

2.1 Get NFS export list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to return all NFS export path and their configuration

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/nfs/export_list

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
    
    A JSON list where its each entry is a JSON object describing one NFS export configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/nfs/export_list

    
2.2 Get a export point configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve one NFS export entry configuration

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/nfs/export_list/[export_name]

    [export_name] is the name of the export entry to retrieve

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
    
    A JSON object to describe this export entry configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/nfs/export_list/abc


2.3 Add export point
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to add a new export point to NFS server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/nfs/export_list

2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     name        |  string  | Required | new export point name                                          |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     path        |  string  | Optional | the absolute path for this export point Default is /           |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    clients      |  list    | Optional | A list where each entry is a JSON object to describe one       |
    |                 |          |          | client configuration for this export point. Default is []. The |
    |                 |          |          | entry JSON object is defined below.                            |
    +-----------------+----------+----------+----------------------------------------------------------------+

    
    The client JSON object with the following field definition.
    
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     host        |  string  | Required | The host or network to which the export is being shared the    |
    |                 |          |          | host can be. Refer to man exports for more format detail.      |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     options     |  string  | Optional | The options to be used for host. Default is empty. Refer to    |
    |                 |          |          | man exports for more detail                                    |
    +-----------------+----------+----------+----------------------------------------------------------------+



4. Status Code

    201      -   Successful
    
    Others   -   Error

5. Special Response Headers

    The following response header would be added

    Location: [export_url]

    [export_url] is the URL to retrieve the new export point configuration info

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"name":"abc", "path": "/home", "clients":[{"host":"*", "options":"rw"}]}' http://[host_ip]:[storlever_port]/storlever/api/v1/nas/nfs/export_list 


2.4 Modify export point
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to modify a export point of NFS server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/nfs/export_list/[export_name]

    [export_name] is the name of the export entry to modify

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     path        |  string  | Optional | the absolute path for this export point Default is /           |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    clients      |  list    | Optional | A list where each entry is a JSON object to describe one       |
    |                 |          |          | client configuration for this export point. Default is []. The |
    |                 |          |          | entry JSON object is defined below.                            |
    +-----------------+----------+----------+----------------------------------------------------------------+

    
    The client JSON object with the following field definition.
    
    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |     host        |  string  | Required | The host or network to which the export is being shared the    |
    |                 |          |          | host can be. Refer to man exports for more format detail.      |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |     options     |  string  | Optional | The options to be used for host. Default is empty. Refer to    |
    |                 |          |          | man exports for more detail                                    |
    +-----------------+----------+----------+----------------------------------------------------------------+

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"path": "/home", "clients":[{"host":"*", "options":"rw"}]}' http://192.168.1.15:6543/storlever/api/v1/nas/nfs/export_list/abc 
    


2.5 Delete export point
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to delete a export point of NFS server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/nfs/export_list/[export_name]

    [export_name] is the name of the export entry to delete

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

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/nas/nfs/export_list/abc 
    


3 Samba Management 
----------------------

The following operations are used to manage the Samba/CIFS Server 

3.1 Get global configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
This API is used to retrieve the global configuration options of SMB server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/conf

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
    
    A JSON object to describe the SMB server global configuration options. 

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/smb/conf
    
    
    
3.2 Set global configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the global configuration for SMB server. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/conf

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +------------------------------+----------+----------+----------------------------------------------------------------+
    |    Fields                    |   Type   | Optional |                            Meaning                             |
    +==============================+==========+==========+================================================================+
    | workgroup                    |  string  | Optional | workgroup controls what workgroup your server will appear to   |
    |                              |          |          | be in when queried by clients. Note that this parameter also   |
    |                              |          |          | controls the Domain name used with the security = domain       |
    |                              |          |          | setting, Default is unchanged                                  |
    +------------------------------+----------+----------+----------------------------------------------------------------+
    | server_string                |  string  | Optional | This controls what string will show up in the printer comment  |
    |                              |          |          | box in print manager and next to the IPC connection in net     |
    |                              |          |          | view. It can be any string that you wish to show to your       |
    |                              |          |          | users.                                                         |
    +------------------------------+----------+----------+----------------------------------------------------------------+
    | netbios_name                 |  string  | Optional | This sets the NetBIOS name by which a Samba server is known.   |
    |                              |          |          | By default it is empty, means the same as the first component  |
    |                              |          |          | of the host's DNS name. If a machine is a browse server or     |
    |                              |          |          | logon server this name (or the first component of the hosts    |
    |                              |          |          | DNS name) will be the name that these services are advertised  |
    |                              |          |          | under                                                          |
    +------------------------------+----------+----------+----------------------------------------------------------------+
    | hosts_allow                  |  string  | Optional | This parameter is a comma, space, or tab delimited set of      |
    |                              |          |          | hosts which are permitted to access a service. Default is      |
    |                              |          |          | empty, means all hosts can access                              |
    +------------------------------+----------+----------+----------------------------------------------------------------+    
    | security                     |  string  | Optional | This option affects how clients respond to Samba, which can    |
    |                              |          |          | share/user/server/domain/ads default is user, default is       |
    |                              |          |          | unchanged                                                      |
    +------------------------------+----------+----------+----------------------------------------------------------------+      
    | passdb_backend               |  string  | Optional | This option allows the administrator to chose which backend    |
    |                              |          |          | will be used for storing user and possibly group information.  |
    |                              |          |          | This allows you to swap between different storage mechanisms   |
    |                              |          |          | without recompile. default is tdbsam. Default is unchanged     |
    +------------------------------+----------+----------+----------------------------------------------------------------+  
    | password_server              |  string  | Optional | specifying the name of another SMB server or Active Directory  |
    |                              |          |          | domain controller with this option, and using                  |
    |                              |          |          | security = [ads|domain|server] it is possible to get Samba to  |
    |                              |          |          | do all its username/password validation using a specific       |
    |                              |          |          | remote server. Default is empty, means auto locate. Default is |
    |                              |          |          | unchanged.                                                     |
    +------------------------------+----------+----------+----------------------------------------------------------------+  
    | realm                        |  string  | Optional | This option specifies the kerberos realm to use. The realm is  |
    |                              |          |          | used as the ADS equivalent of the NT4 domain. It is usually    |
    |                              |          |          | set to the DNS name of the kerberos server. Default is         |
    |                              |          |          | unchanged                                                      |
    +------------------------------+----------+----------+----------------------------------------------------------------+      
    | guest_account                |  string  | Optional | This is a username which will be used for access to services   |
    |                              |          |          | which are specified as guest ok (see below). Whatever          | 
    |                              |          |          | privileges this user has will be available to any client       |
    |                              |          |          | connecting to the guest service. This user must exist in the   |
    |                              |          |          | password file, but does not require a valid login              |
    +------------------------------+----------+----------+----------------------------------------------------------------+ 
    | browseable                   |  bool    | Optional | This controls whether the auto-home share is seen in the list  |
    |                              |          |          | of available shares in a net view and in the browse list       |
    +------------------------------+----------+----------+----------------------------------------------------------------+ 
    
4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"server_string":"test_computer"}' http://192.168.1.15:6543/storlever/api/v1/nas/smb/conf  
    

    
3.3 Get share list
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the share service list of Samba server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/share_list

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
    
    A JSON list with each entry is a JSON object describing one share service configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/smb/share_list
    
    
3.4 Get a share configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve one share service configuration of Samba server. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/share_list/[share_name]

    [share_name] is the name of the share service to retrieve

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
    
    A JSON object to describe this share service configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/smb/share_list/abc
    

3.5 Add share
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to add a new share service to Samba server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/share_list
	
2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------------+----------+----------+----------------------------------------------------------------+
    |    Fields             |   Type   | Optional |                            Meaning                             |
    +=======================+==========+==========+================================================================+
    |     share_name        |  string  | Required | new share name                                                 |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |      path             |  string  | Optional | This parameter specifies a directory to which the user of the  |
    |                       |          |          | service is to be given access. Default is empty, means the     |
    |                       |          |          | user's home directory.                                         |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     comment           |  string  | Optional | This is a text field that is seen next to a share when a       |
    |                       |          |          | client does a queries the server, either via the network       |
    |                       |          |          | neighborhood or via net view to list what shares are           |
    |                       |          |          | available. Default is empty.                                   |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     create_mask       |  int     | Optional | When a file is created, the necessary permissions are          |
    |                       |          |          | calculated according to the mapping from DOS modes to UNIX     |
    |                       |          |          | permissions, and the resulting UNIX mode is then bit-wise      |
    |                       |          |          | ?AND?ed with this parameter. This parameter may be thought of  |
    |                       |          |          | as a bit-wise MASK for the UNIX modes of a file. Any bit not   |
    |                       |          |          | set here will be removed from the modes set on a file when it  |
    |                       |          |          | is created. Default is 0744, which means  removes the group    |
    |                       |          |          | and other write and execute bits from the UNIX modes.          |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     directory_mask    |  int     | Optional | This parameter is the octal modes which are used when          |
    |                       |          |          | converting DOS modes to UNIX modes when creating UNIX          |
    |                       |          |          | directories. When a directory is created, the necessary        |
    |                       |          |          | permissions are calculated according to the mapping from DOS   |
    |                       |          |          | modes to UNIX permissions, and the resulting UNIX mode is then |
    |                       |          |          | bit-wise ANDed with this parameter. This parameter may be      |
    |                       |          |          | thought of as a bit-wise MASK for the UNIX modes of a          |
    |                       |          |          | directory. Any bit not set here will be removed from the modes |
    |                       |          |          | set on a directory when it is created default is 755, which    |
    |                       |          |          | means removes the ?group? and ?other? write bits from the UNIX |
    |                       |          |          | mode, allowing only the user who owns the directory to modify  |
    |                       |          |          | it.                                                            |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |       guest_ok        |  bool    | Optional | If this parameter is True for a share, then no password is     |
    |                       |          |          | required to connect to the share. Privileges will be those of  |
    |                       |          |          | the guest account. Default is false                            |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |      read_only        |  bool    | Optional | If this parameter is true, then users of a service may not     |
    |                       |          |          | create or modify files in the service?s directory. Default is  |
    |                       |          |          | true                                                           |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |      browseable       |  bool    | Optional | This controls whether this share is seen in the list of        |
    |                       |          |          | available shares in a net view and in the browse list. Default |
    |                       |          |          | is  true                                                       |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     valid_users       |  string  | Optional | This is a list of users (seperated by space) that should be    |
    |                       |          |          | allowed to login to this service. If this is empty             |
    |                       |          |          | (the default) then any user can login                          |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     write_list        |  string  | Optional | This is a list of users (seperated by space) that are given    |
    |                       |          |          | read-write access to a service. If the connecting user is in   |
    |                       |          |          | this list then they will be given write access, no matter what |
    |                       |          |          | the read only option is set to. Default is empty               |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     veto_files        |  string  | Optional | This is a list of files and directories that are neither       |
    |                       |          |          | Visible nor accessible. Each entry in the list must be         |
    |                       |          |          | separated by a /, which allows spaces to be included in the    |
    |                       |          |          | entry. * and ? can be used to specify multiple files or        |
    |                       |          |          | directories as in DOS wildcards. Each entry must be a unix     |
    |                       |          |          | path, not a DOS path and must not include the unix directory   |
    |                       |          |          | separator /. Default is empty                                  |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |  force_create_mode    |  int     | Optional | This parameter specifies a set of UNIX mode bit permissions    |
    |                       |          |          | that will always be set on a file created by Samba. This is    |
    |                       |          |          | done by bitwise ORing these bits onto the mode bits of a file  |
    |                       |          |          | that is being created. The default for this parameter is (in   |
    |                       |          |          | octal) 000. The modes in this parameter are bitwise ORed onto  |
    |                       |          |          | the file mode after the mask set in the create mask parameter  |
    |                       |          |          | is applied.                                                    |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |  force_directory_mode |  bool    | Optional | This parameter specifies a set of UNIX mode bit permissions    |
    |                       |          |          | that will always be set on a directory created by Samba. This  |
    |                       |          |          | is done by bitwise ?OR?ing these bits onto the mode bits of a  |
    |                       |          |          | directory that is being created. The default for this          |
    |                       |          |          | parameter is (in octal) 0000 which will not add any extra      |
    |                       |          |          | permission bits to a created directory. This operation is done |
    |                       |          |          | after the mode mask in the parameter directory mask is applied |     
    +-----------------------+----------+----------+----------------------------------------------------------------+


4. Status Code

    201      -   Successful
    
    Others   -   Error

5. Special Response Headers

    The following response header would be added

    Location: [share_url]

    [share_url] is the URL to retrieve the new share service info

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"share_name":"abc", "path":"/home"}' http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/share_list

        
3.6 Modify share
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to modify a share service configuration of Samba server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/share_list/[share_name]

    [share_name] is the name of the share service to modify

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +-----------------------+----------+----------+----------------------------------------------------------------+
    |    Fields             |   Type   | Optional |                            Meaning                             |
    +=======================+==========+==========+================================================================+
    |      path             |  string  | Optional | This parameter specifies a directory to which the user of the  |
    |                       |          |          | service is to be given access. Default is empty, means the     |
    |                       |          |          | user's home directory.                                         |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     comment           |  string  | Optional | This is a text field that is seen next to a share when a       |
    |                       |          |          | client does a queries the server, either via the network       |
    |                       |          |          | neighborhood or via net view to list what shares are           |
    |                       |          |          | available. Default is empty.                                   |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     create_mask       |  int     | Optional | When a file is created, the necessary permissions are          |
    |                       |          |          | calculated according to the mapping from DOS modes to UNIX     |
    |                       |          |          | permissions, and the resulting UNIX mode is then bit-wise      |
    |                       |          |          | ?AND?ed with this parameter. This parameter may be thought of  |
    |                       |          |          | as a bit-wise MASK for the UNIX modes of a file. Any bit not   |
    |                       |          |          | set here will be removed from the modes set on a file when it  |
    |                       |          |          | is created. Default is 0744, which means  removes the group    |
    |                       |          |          | and other write and execute bits from the UNIX modes.          |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     directory_mask    |  int     | Optional | This parameter is the octal modes which are used when          |
    |                       |          |          | converting DOS modes to UNIX modes when creating UNIX          |
    |                       |          |          | directories. When a directory is created, the necessary        |
    |                       |          |          | permissions are calculated according to the mapping from DOS   |
    |                       |          |          | modes to UNIX permissions, and the resulting UNIX mode is then |
    |                       |          |          | bit-wise ANDed with this parameter. This parameter may be      |
    |                       |          |          | thought of as a bit-wise MASK for the UNIX modes of a          |
    |                       |          |          | directory. Any bit not set here will be removed from the modes |
    |                       |          |          | set on a directory when it is created default is 755, which    |
    |                       |          |          | means removes the ?group? and ?other? write bits from the UNIX |
    |                       |          |          | mode, allowing only the user who owns the directory to modify  |
    |                       |          |          | it.                                                            |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |       guest_ok        |  bool    | Optional | If this parameter is True for a share, then no password is     |
    |                       |          |          | required to connect to the share. Privileges will be those of  |
    |                       |          |          | the guest account. Default is false                            |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |      read_only        |  bool    | Optional | If this parameter is true, then users of a service may not     |
    |                       |          |          | create or modify files in the service?s directory. Default is  |
    |                       |          |          | true                                                           |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |      browseable       |  bool    | Optional | This controls whether this share is seen in the list of        |
    |                       |          |          | available shares in a net view and in the browse list. Default |
    |                       |          |          | is  true                                                       |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     valid_users       |  string  | Optional | This is a list of users (seperated by space) that should be    |
    |                       |          |          | allowed to login to this service. If this is empty             |
    |                       |          |          | (the default) then any user can login                          |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     write_list        |  string  | Optional | This is a list of users (seperated by space) that are given    |
    |                       |          |          | read-write access to a service. If the connecting user is in   |
    |                       |          |          | this list then they will be given write access, no matter what |
    |                       |          |          | the read only option is set to. Default is empty               |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |     veto_files        |  string  | Optional | This is a list of files and directories that are neither       |
    |                       |          |          | Visible nor accessible. Each entry in the list must be         |
    |                       |          |          | separated by a /, which allows spaces to be included in the    |
    |                       |          |          | entry. * and ? can be used to specify multiple files or        |
    |                       |          |          | directories as in DOS wildcards. Each entry must be a unix     |
    |                       |          |          | path, not a DOS path and must not include the unix directory   |
    |                       |          |          | separator /. Default is empty                                  |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |  force_create_mode    |  int     | Optional | This parameter specifies a set of UNIX mode bit permissions    |
    |                       |          |          | that will always be set on a file created by Samba. This is    |
    |                       |          |          | done by bitwise ORing these bits onto the mode bits of a file  |
    |                       |          |          | that is being created. The default for this parameter is (in   |
    |                       |          |          | octal) 000. The modes in this parameter are bitwise ORed onto  |
    |                       |          |          | the file mode after the mask set in the create mask parameter  |
    |                       |          |          | is applied.                                                    |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |  force_directory_mode |  bool    | Optional | This parameter specifies a set of UNIX mode bit permissions    |
    |                       |          |          | that will always be set on a directory created by Samba. This  |
    |                       |          |          | is done by bitwise ?OR?ing these bits onto the mode bits of a  |
    |                       |          |          | directory that is being created. The default for this          |
    |                       |          |          | parameter is (in octal) 0000 which will not add any extra      |
    |                       |          |          | permission bits to a created directory. This operation is done |
    |                       |          |          | after the mode mask in the parameter directory mask is applied |     
    +-----------------------+----------+----------+----------------------------------------------------------------+    

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"path": "/home", "comment":"test"}' http://192.168.1.15:6543/storlever/api/v1/nas/smb/share_list/abc


    
3.7 Delete share
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to delete a share service of Samba server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/share_list/[share_name]

    [share_name] is the name of the share service to delete

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

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/nas/smb/share_list/abc
    

3.8 Get connection list
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the current connections to the Samba server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/connection_list

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
    
    A JSON list with each entry is a JSON object describing one current client connection info

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/smb/connection_list
    
    
3.9 Get account list
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the account list of Samba server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/account_list

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
    
    A JSON list with each entry is a JSON object describing one account info

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/smb/account_list
    
        
3.10 Add account
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to add a new account to Samba server. The new account must be a Linux system user. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/account_list
	
2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------------+----------+----------+----------------------------------------------------------------+
    |    Fields             |   Type   | Optional |                            Meaning                             |
    +=======================+==========+==========+================================================================+
    |   account_name        |  string  | Required | new account name. The same Linux system user must exist        |
    +-----------------------+----------+----------+----------------------------------------------------------------+
    |   password            |  string  | Required | Password for the account                                       |
    +-----------------------+----------+----------+----------------------------------------------------------------+


4. Status Code

    201      -   Successful
    
    Others   -   Error

5. Special Response Headers

    The following response header would be added

    Location: [account_url]

    [share_url] is the URL to modify/delete the new account

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"account_name":"abc", "password":"123456"}' http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/account_list
    
    
3.11 Modify account
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to modify a account's configuration of Samba server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/account_list/[account_name]

    [account_name] is the name of the samba account to modify

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +-----------------------+----------+----------+----------------------------------------------------------------+
    |    Fields             |   Type   | Optional |                            Meaning                             |
    +=======================+==========+==========+================================================================+
    |      password         |  string  | required | new password for the account                                   |
    +-----------------------+----------+----------+----------------------------------------------------------------+


4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"password":"test"}' http://192.168.1.15:6543/storlever/api/v1/nas/smb/account_list/abc
    
    
    
3.12 Delete account
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to delete an account of Samba server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/smb/account_list/[account_name]

    [account_name] is the name of the samba account to delete


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

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/nas/smb/account_list/abc
    