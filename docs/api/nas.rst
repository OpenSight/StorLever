StorLever Utils API
======================

The following section would describe the API for the NAS server management of StorLever. 
NAS servers in StorLever includes the types of FTP, NFS(v3,v4), Samba/CIFS, which are typical NAS aplication. 

StorLever NAS API has the following structure:

* `1 FTP Management <#1-ftp-management>`_
    * `1.1 Get FTP server global configuration <#11-get-ftp-server-global-configuration>`_
    * `1.2 Set FTP server global configuration <#12-set-ftp-server-global-configuration>`_
    * `1.3 Get FTP user list <#13-get-ftp-user-list>`_
    * `1.4 Get a FTP user configuration <#14-get-a-ftp-user-configuration>`_
    * `1.5 Add FTP user <#15-add-ftp-user>`_
    * `1.6 Modify FTP user <#16-modify-ftp-user>`_
    * `1.7 Delete FTP user <#17-delete-ftp-user>`_

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
    



1 FTP Management
------------------

The following operations are used to manage FTP server configuration of StorLever. 
StorLever make use of vsftpd as its FTP server in current version. 


1.1 Get FTP server global configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the global configuration options of FTP server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/ftp/conf

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
    
    A JSON object to describe the global FTP server configuration. 

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/ftp/conf



1.2 Set FTP server global configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to set the global configuration of the FTP server. 

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/ftp/conf

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +-------------------------+----------+----------+----------------------------------------------------------------+
    |    Fields               |   Type   | Optional |                            Meaning                             |
    +=========================+==========+==========+================================================================+
    |     listen              |   bool   | Optional | ftp service listen on ipv4 port. Default is unchanged          |
    +-------------------------+----------+----------+----------------------------------------------------------------+
    |     listen6             |   bool   | Optional | ftp service listen on ipv6 port. Default is unchanged.         |
    +-------------------------+----------+----------+----------------------------------------------------------------+
    |     listen_port         |   int    | Optional | ftp port number. Default is unchanged.                         |
    +-------------------------+----------+----------+----------------------------------------------------------------+
    | idle_session_timeout    |   int    | Optional | The maximum amount of time (in sec) between commands from a    |
    |                         |          |          | remote client. Once triggered, the connection to the remote    |
    |                         |          |          | client is closed. Default is unchanged.                        |
    +-------------------------+----------+----------+----------------------------------------------------------------+
    | anon_max_rate           |   int    | Optional | the maximum data transfer rate for anonymous users in bytes    |
    |                         |          |          | per second. The default value is 0, which does not limit the   |
    |                         |          |          | transfer rate. Default is unchanged.                           |
    +-------------------------+----------+----------+----------------------------------------------------------------+
    | local_max_rate          |   int    | Optional | the maximum rate data is transferred for local users in bytes  |
    |                         |          |          | per second. The default value is 0, which does not limit the   |
    |                         |          |          | transfer rate. Default is unchanged.                           |
    +-------------------------+----------+----------+----------------------------------------------------------------+    
    | max_clients             |   int    | Optional | the maximum number of simultaneous clients allowed to connect  |
    |                         |          |          | to the server when it is running in standalone mode. Any       |
    |                         |          |          | additional client connections would result in an error         | 
    |                         |          |          | message. The default value is 0, which does not limit          |
    |                         |          |          | connections. Default is unchanged                              |
    +-------------------------+----------+----------+----------------------------------------------------------------+        
    | max_per_ip              |   int    | Optional | the maximum of clients allowed to connected from the same      |
    |                         |          |          | source IP address. The default value is 0, which does not      | 
    |                         |          |          | limit connections. Default is unchanged                        |
    +-------------------------+----------+----------+----------------------------------------------------------------+        
    | download_enable         |   bool   | Optional | When enabled, file downloads are permitted. Default is         |
    |                         |          |          | unchanged.                                                     |
    +-------------------------+----------+----------+----------------------------------------------------------------+        
    | write_enable            |   bool   | Optional | When enabled, FTP commands which can change the file system    |
    |                         |          |          | are allowed. Default is unchanged.                             |
    +-------------------------+----------+----------+----------------------------------------------------------------+      
    | local_enable            |   bool   | Optional | When enabled, local users are allowed to log into the system.  |
    |                         |          |          | Default is unchanged                                           |
    +-------------------------+----------+----------+----------------------------------------------------------------+      
    | userlist_enable         |   bool   | Optional | Only valid when local_enable is true. If userlist_enable ==    |
    |                         |          |          | False, all local user (except for some reserved user, like     |
    |                         |          |          | root, bin) can login ftp. Otherwise, only the users, who is in | 
    |                         |          |          | the user list and is login enabled, can login ftp. Default is  | 
    |                         |          |          | unchanged.                                                     |
    +-------------------------+----------+----------+----------------------------------------------------------------+      
    | local_root              |  string  | Optional | Specifies the directory ftpd changes to after a local user     |
    |                         |          |          | logs in. default is empty, which means the user's home         | 
    |                         |          |          | directory. Default is unchanged                                |
    +-------------------------+----------+----------+----------------------------------------------------------------+      
    | chroot_enable           |   bool   | Optional | When enabled, local users are change-rooted to their home      |
    |                         |          |          | directories after logging in. Default is unchanged             |
    +-------------------------+----------+----------+----------------------------------------------------------------+      
    | chroot_list             |   bool   | Optional | Only valid when chroot_enable is true. If chroot_list ==       |
    |                         |          |          | False, all local user are placed in a chroot jail upon log in. |
    |                         |          |          | Otherwise, only the users, who is in the user list and is      |
    |                         |          |          | chroot enabled, would be placed in a chroot jail upon log in.  |
    |                         |          |          | Default is unchanged                                           |
    +-------------------------+----------+----------+----------------------------------------------------------------+       
    | local_umask             |   int    | Optional | the umask value for file creation. default is 022(18 in        |
    |                         |          |          | 10-based). Default is unchanged                                |
    +-------------------------+----------+----------+----------------------------------------------------------------+       
    | anonymous_enable        |   bool   | Optional | When enabled, anonymous users are allowed to log in. The       |
    |                         |          |          | usernames anonymous and ftp are accepted. Default is unchanged |
    +-------------------------+----------+----------+----------------------------------------------------------------+      
    | anon_mkdir_write_enable |   bool   | Optional | When enabled in conjunction with the write_enable directive,   |
    |                         |          |          | anonymous users are allowed to create new directories within   |
    |                         |          |          | a parent directory which has write permissions. Default is     |
    |                         |          |          | unchanged                                                      |
    +-------------------------+----------+----------+----------------------------------------------------------------+      
    | anon_upload_enable      |   bool   | Optional | When enabled in conjunction with the write_enable directive,   |
    |                         |          |          | anonymous users are allowed to upload files within a parent    |
    |                         |          |          | directory which has write permissions. Default is unchanged    |
    +-------------------------+----------+----------+----------------------------------------------------------------+
    | anon_username           |  string  | Optional | Specifies the local user account (listed in /etc/passwd) used  |
    |                         |          |          | for the anonymous user. The home directory specified in        |
    |                         |          |          | /etc/passwd for the user is the root directory of the          |
    |                         |          |          | anonymous user. Default is unchanged                           |
    +-------------------------+----------+----------+----------------------------------------------------------------+     
    | anon_root               |  string  | Optional | Specifies the directory vsftpd changes to after an anonymous   |
    |                         |          |          | user logs in. default is empty, which means the anon_username  |
    |                         |          |          | user's home directory Default is unchanged                     |
    +-------------------------+----------+----------+----------------------------------------------------------------+       
        
    
4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    No

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"write_enable":true}' http://192.168.1.15:6543/storlever/api/v1/nas/ftp/conf  
 

1.3 Get FTP user list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve the FTP user configure list

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/ftp/user_list

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
    
    A JSON list where its each entry is a JSON object describing one FTP user configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/ftp/user_list
 
 
1.4 Get a FTP user configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to retrieve one FTP user configuration

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/ftp/user_list/[user_name]

    [user_name] is the name of the community to retrieve

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
    
    A JSON object to describe this FTP user configuration

7. Example 

    curl -v -X GET http://192.168.1.15:6543/storlever/api/v1/nas/ftp/user_list/abc



1.5 Add FTP user
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to add a new FTP user to FTP server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/ftp/user_list

2. HTTP Method
    
    POST

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |    user_name    |  string  | Required | new FTP user name                                              |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  login_enable   |  bool    | Optional | When enabled, the user can log in ftp. Default is false        |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  chroot_enable  |  bool    | Optional | When enabled, the user will be placed into the chroot jail.    |
    |                 |          |          | Default is false.                                              |
    +-----------------+----------+----------+----------------------------------------------------------------+



4. Status Code

    201      -   Successful
    
    Others   -   Error

5. Special Response Headers

    The following response header would be added

    Location: [user_url]

    [user_url] is the URL to retrieve the new user configuration info

6. Response Content
    
    NULL

7. Example 

    curl -v -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"user_name":"abc"}' http://[host_ip]:[storlever_port]/storlever/api/v1/nas/ftp/user_list  

    
1.6 Modify FTP user
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to modify a user configuration of FTP server.

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/ftp/user_list/[user_name]

    [user_name] is the name of the community to retrieve

2. HTTP Method
    
    PUT

3. Request Content

    A JSON object with the following field definition. 

    +-----------------+----------+----------+----------------------------------------------------------------+
    |    Fields       |   Type   | Optional |                            Meaning                             |
    +=================+==========+==========+================================================================+
    |  login_enable   |  bool    | Optional | When enabled, the user can log in ftp. Default is unchanged    |
    +-----------------+----------+----------+----------------------------------------------------------------+
    |  chroot_enable  |  bool    | Optional | When enabled, the user will be placed into the chroot jail.    |
    |                 |          |          | Default is unchanged.                                          |
    +-----------------+----------+----------+----------------------------------------------------------------+

4. Status Code

    200      -   Successful
    
    Others   -   Error

5. Special Response Headers

    NULL

6. Response Content
    
    NULL

7. Example 

    curl -v -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{"login_enable": true}' http://[host_ip]:[storlever_port]/storlever/api/v1/nas/ftp/user_list/abc 
    

1.7 Delete FTP user
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API is used to delete a FTP user of FTP server

1. Resource URI

    http://[host_ip]:[storlever_port]/storlever/api/v1/nas/ftp/user_list/[user_name]

    [user_name] is the name of the community to retrieve

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

    curl -v -X DELETE http://192.168.1.15:6543/storlever/api/v1/nas/ftp/user_list/abc  
    



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
    