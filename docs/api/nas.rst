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

* NFS management

* Samba management



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
    
    