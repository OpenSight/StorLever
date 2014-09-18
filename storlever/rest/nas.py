"""
storlever.rest.nas
~~~~~~~~~~~~~~~~

This module implements the rest API for NAS servers.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""



from storlever.rest.common import get_view, post_view, put_view, delete_view
from pyramid.response import Response

from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError, BoolVal, StrRe, ListVal
from storlever.lib.exception import StorLeverError
from storlever.mngr.nas import ftpmgr
from storlever.mngr.nas import nfsmgr
from storlever.mngr.nas import smbmgr

from storlever.rest.common import get_params_from_request

def includeme(config):

    config.add_route('ftp_conf', '/nas/ftp/conf')
    config.add_route('ftp_user_list', '/nas/ftp/user_list')
    config.add_route('ftp_user_conf', '/nas/ftp/user_list/{user_name}')


    config.add_route('nfs_export_list', '/nas/nfs/export_list')
    config.add_route('nfs_export_info', '/nas/nfs/export_list/{export_name}')

    config.add_route('smb_conf', '/nas/smb/conf')
    config.add_route('smb_share_list', '/nas/smb/share_list')
    config.add_route('smb_share_conf', '/nas/smb/share_list/{share_name}')
    config.add_route('smb_connection_list', '/nas/smb/connection_list')
    config.add_route('smb_account_list', '/nas/smb/account_list')
    config.add_route('smb_account_conf', '/nas/smb/account_list/{account_name}')


@get_view(route_name='ftp_conf')
def get_ftp_conf(request):
    ftp_mgr = ftpmgr.FtpManager
    return ftp_mgr.get_ftp_conf()


ftp_conf_schema = Schema({
    Optional("listen"): BoolVal(),     # ftp service listen on ipv4 port
    Optional("listen6"): BoolVal(),    # ftp service listen on ipv6 port
    Optional("listen_port"): IntVal(min=1, max=65535),  # ftp port number

    # The maximum amount of time between commands from a remote client.
    # Once triggered, the connection to the remote client is closed
    Optional("idle_session_timeout"): Use(int),

    # the maximum data transfer rate for anonymous users in bytes per second.
    # The default value is 0, which does not limit the transfer rate.
    Optional("anon_max_rate"):Use(int),
    # the maximum rate data is transferred for local users in bytes per second.
    # The default value is 0, which does not limit the transfer rate.
    Optional("local_max_rate"): Use(int),

    # the maximum number of simultaneous clients allowed to connect to
    # the server when it is running in standalone mode. Any additional client
    # connections would result in an error message.
    # The default value is 0, which does not limit connections.
    Optional("max_clients"): Use(int),

    # the maximum of clients allowed to connected from the same source IP address.
    # The default value is 0, which does not limit connections.
    Optional("max_per_ip"):Use(int),

    # When enabled, file downloads are permitted
    Optional("download_enable"): BoolVal(),
    # When enabled, FTP commands which can change the file system are allowed
    Optional("write_enable"): BoolVal(),

    # When enabled, local users are allowed to log into the system
    Optional("local_enable"): BoolVal(),
    # Only valid when local_enable is true. If userlist_enable == False,
    # all local user (except for some reserved user, like root, bin) can login ftp.
    # Otherwise, only the users, who is in the user list and is login enabled, can
    # login ftp
    Optional("userlist_enable"): BoolVal(),
    # Specifies the directory ftpd changes to after a local user logs in. default is
    # empty, which means the user's home directory
    Optional("local_root"): StrRe(r"^\S*$"),

    # When enabled, local users are change-rooted to their home directories after logging in.
    Optional("chroot_enable"): BoolVal(),
    # Only valid when chroot_enable is true. If chroot_list == False,
    # all local user are placed in a chroot jail upon log in.
    # Otherwise, only the users, who is in the user list and is chroot enabled, would be
    # placed in a chroot jail upon log in.
    Optional("chroot_list"): BoolVal(),

    # the umask value for file creation. default is 022(18 in 10-based)
    Optional("local_umask"): IntVal(min=0, max=0777),



    # When enabled, anonymous users are allowed to log in.
    # The usernames anonymous and ftp are accepted.
    Optional("anonymous_enable"): BoolVal(),

    # When enabled in conjunction with the write_enable directive,
    # anonymous users are allowed to create new directories within
    # a parent directory which has write permissions
    Optional("anon_mkdir_write_enable"): BoolVal(),
    # When enabled in conjunction with the write_enable directive,
    # anonymous users are allowed to upload files within
    # a parent directory which has write permissions.
    Optional("anon_upload_enable"): BoolVal(),

    # Specifies the local user account (listed in /etc/passwd) used for the anonymous user.
    # The home directory specified in /etc/passwd for the user is the root directory of the anonymous user.
    Optional("anon_username"): StrRe(r"^\w+$"),

    # Specifies the directory vsftpd changes to after an anonymous user logs in. default is
    # empty, which means the anon_username user's home directory
    Optional("anon_root"): StrRe(r"^\S*$"),

    DoNotCare(Use(str)): object  # for all other key we don't care
})


@put_view(route_name='ftp_conf')
def put_ftp_conf(request):
    ftp_mgr = ftpmgr.FtpManager
    ftp_conf = get_params_from_request(request, ftp_conf_schema)
    ftp_mgr.set_ftp_conf(ftp_conf, operator=request.client_addr)
    return Response(status=200)


@get_view(route_name='ftp_user_list')
def get_ftp_user_list(request):
    ftp_mgr = ftpmgr.FtpManager
    return ftp_mgr.get_user_conf_list()



ftp_user_schema = Schema({
    "user_name": StrRe(r"^\w+$"),
    # When enabled, the user can log in ftp
    Optional("login_enable"): BoolVal(),
    # When enabled, the user will be placed into the chroot jail
    Optional("chroot_enable"): BoolVal(),

    DoNotCare(Use(str)): object  # for all other key we don't care
})

@post_view(route_name='ftp_user_list')
def post_ftp_user_list(request):
    ftp_mgr = ftpmgr.FtpManager
    new_user_conf = get_params_from_request(request, ftp_user_schema)
    ftp_mgr.add_user_conf(new_user_conf["user_name"],
                          new_user_conf.get("login_enable", False),
                          new_user_conf.get("chroot_enable", False),
                          operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('ftp_user_conf',
                                      user_name=new_user_conf["user_name"])
    return resp


@get_view(route_name='ftp_user_conf')
def get_ftp_user_conf(request):
    user_name = request.matchdict['user_name']
    ftp_mgr = ftpmgr.FtpManager
    return ftp_mgr.get_user_conf(user_name)


@put_view(route_name='ftp_user_conf')
def put_ftp_user_conf(request):
    user_name = request.matchdict['user_name']
    ftp_mgr = ftpmgr.FtpManager
    user_conf = get_params_from_request(request)
    user_conf["user_name"] = user_name
    user_conf = ftp_user_schema.validate(user_conf)

    ftp_mgr.set_user_conf(user_conf["user_name"],
                          user_conf.get("login_enable"),
                          user_conf.get("chroot_enable"),
                          operator=request.client_addr)

    return Response(status=200)


@delete_view(route_name='ftp_user_conf')
def delete_ftp_user_conf(request):
    user_name = request.matchdict['user_name']
    ftp_mgr = ftpmgr.FtpManager
    ftp_mgr.del_user_conf(user_name, operator=request.client_addr)
    return Response(status=200)






@get_view(route_name='nfs_export_list')
def get_nfs_export_list(request):
    nfs_mgr = nfsmgr.NfsManager
    return nfs_mgr.get_export_list()

nfs_client_schema = Schema({
    # The host or network to which the export is being shared
    # the host can be
    #  single host
    #         You may specify a host either by an abbreviated name recognized  be  the
    #         resolver,  the  fully qualified domain name, an IPv4 address, or an IPv6
    #         address.  IPv6  addresses  must  not  be  inside  square   brackets   in
    #         /etc/exports   lest  they  be  confused  with  character-class  wildcard
    #         matches.
    #
    #   netgroups
    #         NIS netgroups may be given as @group.  Only the host part of  each  net-
    #         group  members is consider in checking for membership.  Empty host parts
    #         or those containing a single dash (-) are ignored.
    #
    #   wildcards
    #         Machine names may contain the wildcard characters * and ?, or may  con-
    #         tain  character  class lists within [square brackets].  This can be used
    #         to make the  exports  file  more  compact;  for  instance,  *.cs.foo.edu
    #         matches  all  hosts  in the domain cs.foo.edu.  As these characters also
    #         match the dots in a domain name, the given pattern will also  match  all
    #         hosts within any subdomain of cs.foo.edu.
    #
    #   IP networks
    #          You  can  also  export  directories to all hosts on an IP (sub-) network
    #          simultaneously. This is done by specifying an  IP  address  and  netmask
    #          pair  as  address/netmask  where the netmask can be specified in dotted-
    #          decimal format, or as a contiguous mask  length.   For  example,  either
    #          255.255.252.0 or  22 appended  to  the network base IPv4 address
    #          results in identical subnetworks with 10 bits of  host.  IPv6  addresses
    #          must use a contiguous mask length and must not be inside square brackets
    #          to avoid confusion with character-class wildcards.  Wildcard  characters
    #          generally  do not work on IP addresses, though they may work by accident
    #          when reverse DNS lookups fail.
    "host": StrRe("^(\S)*$"),

    # The options to be used for host
    Optional("options"): Default(StrRe("^(\S)*$"), default=""),

    DoNotCare(Use(str)): object  # for all other key we don't care
})


nfs_export_schema = Schema({
    # export point name
    "name": StrRe(r"^\w+$"),

    # absolute path
    Optional("path"): StrRe(r"^\S+$"),

    # client list for this export point
    Optional("clients"): [nfs_client_schema],

    DoNotCare(Use(str)): object  # for all other key we don't care

})



@post_view(route_name='nfs_export_list')
def post_nfs_export_list(request):
    nfs_mgr = nfsmgr.NfsManager
    new_export_conf = get_params_from_request(request, nfs_export_schema)
    nfs_mgr.append_export_conf(new_export_conf["name"],
                               new_export_conf.get("path", "/"),
                               new_export_conf.get("clients", []),
                               operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('nfs_export_info',
                                      export_name=new_export_conf["name"])
    return resp


@get_view(route_name='nfs_export_info')
def get_nfs_export_info(request):
    export_name = request.matchdict['export_name']
    nfs_mgr = nfsmgr.NfsManager
    return nfs_mgr.get_export_conf(export_name)



@put_view(route_name='nfs_export_info')
def put_nfs_export_info(request):
    export_name = request.matchdict['export_name']
    nfs_mgr = nfsmgr.NfsManager
    export_conf = get_params_from_request(request)
    export_conf["name"] = export_name
    export_conf = nfs_export_schema.validate(export_conf)

    nfs_mgr.set_export_conf(export_name,
                            export_conf.get("path"),
                            export_conf.get("clients"),
                            operator=request.client_addr)

    return Response(status=200)




@delete_view(route_name='nfs_export_info')
def delete_nfs_export_info(request):
    export_name = request.matchdict['export_name']
    nfs_mgr = nfsmgr.NfsManager
    nfs_mgr.del_export_conf(export_name, operator=request.client_addr)
    return Response(status=200)




@get_view(route_name='smb_conf')
def get_smb_conf(request):
    smb_mgr = smbmgr.SmbManager
    return smb_mgr.get_smb_conf()



smb_conf_schema = Schema({
    # workgroup controls what workgroup your server will appear to be in when queried
    # by clients. Note that this parameter also controls the Domain name used
    #  with the security = domain setting,
    Optional("workgroup"): StrRe(r"^\w+$"),

    # This controls what string will show up in the printer comment box in print
    # manager and next to the IPC connection in net view. It can be any string
    # that you wish to show to your users.
    Optional("server_string"): Use(str),

    #  This sets the NetBIOS name by which a Samba server is known. By default it
    # is empty, means the same as the first component of the host's DNS name. If a machine is
    # a browse server or logon server this name (or the first component of the
    # hosts DNS name) will be the name that these services are advertised under
    Optional("netbios_name"): StrRe(r"^(\S)*$"),

    # This parameter is a comma, space, or tab delimited set of hosts which are
    # permitted to access a service. Default is empty, means all hosts can access
    Optional("hosts_allow"): Use(str),

    # This option affects how clients respond to Samba, which can share/user/server/domain/ads
    # default is user
    Optional("security"): StrRe(r"^(share|user|server|domain|ads)$"),

    # This option allows the administrator to chose which backend will be used
    # for storing user and possibly group information. This allows you to swap
    # between different storage mechanisms without recompile. default is tdbsam
    Optional("passdb_backend"): Use(str),

    # specifying the name of another SMB server or Active Directory domain
    # controller with this option, and using security = [ads|domain|server] it is
    # possible to get Samba to do all its username/password validation using a
    # specific remote server. Default is empty, means auto locate.
    Optional("password_server"): Use(str),

    # This option specifies the kerberos realm to use. The realm is used as the
    # ADS equivalent of the NT4 domain. It is usually set to the DNS name of the
    # kerberos server. Default is empty
    Optional("realm"): StrRe(r"^(\S)*$"),

    #  This is a username which will be used for access to services which are
    # specified as guest ok (see below). Whatever privileges this user has will
    # be available to any client connecting to the guest service. This user must
    # exist in the password file, but does not require a valid login..
    Optional("guest_account"): Use(str),

    # This controls whether the auto-home share is seen in the list of available shares in
    # a net view and in the browse list
    Optional("browseable"): BoolVal(),

    DoNotCare(Use(str)): object  # for all other key we don't care

})



@put_view(route_name='smb_conf')
def put_smb_conf(request):
    smb_mgr = smbmgr.SmbManager
    smb_conf = get_params_from_request(request, smb_conf_schema)
    smb_mgr.set_smb_conf(smb_conf, operator=request.client_addr)
    return Response(status=200)





@get_view(route_name='smb_share_list')
def get_smb_share_list(request):
    smb_mgr = smbmgr.SmbManager
    return smb_mgr.get_share_conf_list()



smb_share_schema = Schema({
    # Name of this share
    "share_name": Use(str),

    # This parameter specifies a directory to which the user of the service is to
    # be given access.default is empty, means the user's home directory
    Optional("path"): Use(str),

    # This is a text field that is seen next to a share when a client does a
    # queries the server, either via the network neighborhood or via net view to
    # list what shares are available. Default is empty
    Optional("comment"): Use(str),


    # When a file is created, the necessary permissions are calculated according
    # to the mapping from DOS modes to UNIX permissions, and the resulting UNIX
    # mode is then bit-wise ?AND?ed with this parameter. This parameter may be
    # thought of as a bit-wise MASK for the UNIX modes of a file. Any bit not set
    # here will be removed from the modes set on a file when it is created.
    # Default is 0744, which means  removes the group and other write and
    # execute bits from the UNIX modes.
    Optional("create_mask"): IntVal(min=0, max=0777),

    # This parameter is the octal modes which are used when converting DOS modes
    # to UNIX modes when creating UNIX directories.
    # When a directory is created, the necessary permissions are calculated
    # according to the mapping from DOS modes to UNIX permissions, and the
    # resulting UNIX mode is then bit-wise ANDed with this parameter. This
    # parameter may be thought of as a bit-wise MASK for the UNIX modes of a
    # directory. Any bit not set here will be removed from the modes set on a
    # directory when it is created
    # default is 755, which means removes the ?group? and ?other? write
    # bits from the UNIX mode, allowing only the user who owns the directory to
    # modify it.
    Optional("directory_mask"): IntVal(min=0, max=0777),

    #  If this parameter is True for a share, then no password is required to
    # connect to the share. Privileges will be those of the guest account..
    Optional("guest_ok"): BoolVal(),

    #  If this parameter is true, then users of a service may not create or modify
    # files in the service?s directory..
    Optional("read_only"): BoolVal(),

    # This controls whether this share is seen in the list of available shares in
    # a net view and in the browse list..
    Optional("browseable"): BoolVal(),


    # This is a list of users that should be allowed to login to this service.
    # If this is empty (the default) then any user can login
    Optional("valid_users"): Use(str),

    # This is a list of users that are given read-write access to a service. If
    # the connecting user is in this list then they will be given write access,
    # no matter what the read only option is set to.
    Optional("write_list"): Use(str),

    # This is a list of files and directories that are neither visible nor
    # accessible. Each entry in the list must be separated by a /, which allows
    # spaces to be included in the entry. * and ? can be used to specify
    # multiple files or directories as in DOS wildcards.
    # Each entry must be a unix path, not a DOS path and must not include the
    # unix directory separator /
    Optional("veto_files"): Use(str),

    # This parameter specifies a set of UNIX mode bit permissions that will
    # always be set on a file created by Samba. This is done by bitwise ORing
    # these bits onto the mode bits of a file that is being created. The default
    # for this parameter is (in octal) 000. The modes in this parameter are
    # bitwise ORed onto the file mode after the mask set in the create mask
    # parameter is applied.
    Optional("force_create_mode"): IntVal(min=0, max=0777),

    # This parameter specifies a set of UNIX mode bit permissions that will
    # always be set on a directory created by Samba. This is done by bitwise
    # ?OR?ing these bits onto the mode bits of a directory that is being created.
    # The default for this parameter is (in octal) 0000 which will not add any
    # extra permission bits to a created directory. This operation is done after
    # the mode mask in the parameter directory mask is applied
    Optional("force_directory_mode"): IntVal(min=0, max=0777),

    DoNotCare(Use(str)): object  # for all other key we don't care

})

@post_view(route_name='smb_share_list')
def post_smb_share_list(request):
    smb_mgr = smbmgr.SmbManager
    new_share_conf = get_params_from_request(request, smb_share_schema)
    smb_mgr.add_share_conf(new_share_conf["share_name"],
                           new_share_conf.get("path", ""),
                           new_share_conf.get("comment", ""),
                           new_share_conf.get("create_mask", 0744),
                           new_share_conf.get("directory_mask", 0755),
                           new_share_conf.get("guest_ok", False),
                           new_share_conf.get("read_only", True),
                           new_share_conf.get("browseable", True),
                           new_share_conf.get("force_create_mode", 0),
                           new_share_conf.get("force_directory_mode", 0),
                           new_share_conf.get("valid_users", ""),
                           new_share_conf.get("write_list", ""),
                           new_share_conf.get("veto_files", ""),
                           operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('smb_share_conf',
                                      share_name=new_share_conf["share_name"])
    return resp


@get_view(route_name='smb_share_conf')
def get_smb_share_conf(request):
    share_name = request.matchdict['share_name']
    smb_mgr = smbmgr.SmbManager
    return smb_mgr.get_share_conf(share_name)


@put_view(route_name='smb_share_conf')
def put_smb_share_conf(request):
    share_name = request.matchdict['share_name']
    smb_mgr = smbmgr.SmbManager
    share_conf = get_params_from_request(request)

    share_conf["share_name"] = share_name
    share_conf = smb_share_schema.validate(share_conf)

    smb_mgr.set_share_conf(share_conf["share_name"],
                           share_conf.get("path"),
                           share_conf.get("comment"),
                           share_conf.get("create_mask"),
                           share_conf.get("directory_mask"),
                           share_conf.get("guest_ok"),
                           share_conf.get("read_only"),
                           share_conf.get("browseable"),
                           share_conf.get("force_create_mode"),
                           share_conf.get("force_directory_mode"),
                           share_conf.get("valid_users"),
                           share_conf.get("write_list"),
                           share_conf.get("veto_files"),
                           operator=request.client_addr)

    return Response(status=200)


@delete_view(route_name='smb_share_conf')
def delete_smb_share_conf(request):
    share_name = request.matchdict['share_name']
    smb_mgr = smbmgr.SmbManager
    smb_mgr.del_share_conf(share_name, operator=request.client_addr)
    return Response(status=200)



@get_view(route_name='smb_connection_list')
def get_smb_connection_list(request):
    smb_mgr = smbmgr.SmbManager
    return smb_mgr.get_connection_list()




@get_view(route_name='smb_account_list')
def get_smb_account_list(request):
    smb_mgr = smbmgr.SmbManager
    return smb_mgr.get_smb_account_list()

smb_account_schema = Schema({
    # Name of this account
    "account_name": Use(str),

    # password
    "password": Use(str),

})

@post_view(route_name='smb_account_list')
def post_smb_account_list(request):
    smb_mgr = smbmgr.SmbManager
    new_account_conf = get_params_from_request(request, smb_account_schema)

    smb_mgr.add_smb_account(new_account_conf["account_name"],
                            new_account_conf["password"],
                            operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('smb_account_conf',
                                      account_name=new_account_conf["account_name"])
    return resp




@put_view(route_name='smb_account_conf')
def put_smb_account_conf(request):
    account_name = request.matchdict['account_name']
    smb_mgr = smbmgr.SmbManager
    account_conf = get_params_from_request(request)


    account_conf["account_name"] = account_name
    account_conf = smb_account_schema.validate(account_conf)

    smb_mgr.set_smb_account_passwd(account_conf["account_name"],
                                   account_conf["password"],
                                   operator=request.client_addr)


    return Response(status=200)



@delete_view(route_name='smb_account_conf')
def delete_smb_account_conf(request):
    account_name = request.matchdict['account_name']
    smb_mgr = smbmgr.SmbManager
    smb_mgr.del_smb_account(account_name, operator=request.client_addr)
    return Response(status=200)