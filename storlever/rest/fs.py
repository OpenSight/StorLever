from storlever.rest.common import (get_view, post_view, 
                                   put_view, delete_view)
from storlever.lib.exception import StorLeverError
from storlever.mngr.fs.fsmgr import FileSystemManager
from pyramid.response import Response


def includeme(config):
    # filesystem list resource
    # GET:    filesystem list
    # POST:   create filesystem
    config.add_route('fs_list', '/fs_list')
    # filesystem resource
    # GET:    filesystem information
    # PUT:    create filesystem
    # DELETE: remove filesystem
    config.add_route('fs', '/fs_list/{fs}')
    # filesystem share list resource
    # GET:    share list
    # POST:   create/delete share
    config.add_route('share_list', '/fs_list/{fs}/share_list')
    # NFS export list resourceh
    # GET:    NFS export list
    # POST:   create/delete NFS export
    config.add_route('nfs_list', '/nfs_list')
    # NFS export
    # GET:    NFS export information
    # PUT:    create NFS export
    # POST:   change export parameter
    # DELETE: delete NFS export
    config.add_route('nfs', '/nfs_list/{nfs}')
    # SAMBA export list resource
    # GET:    SAMBA export list
    # POST:   create/delete SAMBA export
    config.add_route('smb_list', '/smb_list')
    # SAMBA export
    # GET:    SAMBA export information
    # PUT:    create SAMBA export
    # POST:   change export parameter
    # DELETE: delete SAMBA export
    config.add_route('smb', '/smb_list/{smb}')
    # FTP export list resource
    # GET:    FTP export list
    # POST:   create/delete FTP export
    config.add_route('ftp_list', '/ftp_list')
    # SAMBA export
    # GET:    FTP export information
    # PUT:    create FTP export
    # POST:   change export parameter
    # DELETE: delete FTP export
    config.add_route('ftp', '/ftp_list/{ftp}')

#http://192.168.2.10:6543/storlever/api/v1/fs_list
@get_view(route_name='fs_list')
def get_fs_list(request):
    fs_mrg = FileSystemManager
    file_list = fs_mrg.get_fs_list()
    print file_list
    return file_list
