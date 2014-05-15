"""
storlever.mngr.nas.nfsmgr
~~~~~~~~~~~~~~~~

This module implements NFS server management.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path


from storlever.lib.config import Config
from storlever.lib.command import check_output, set_selinux_permissive
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
from storlever.lib.utils import filter_dict
import logging
from storlever.lib.schema import Schema, Use, Optional, \
    Default, DoNotCare, BoolVal, IntVal, StrRe
from storlever.lib.lock import lock
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR, cfg_mgr
from storlever.mngr.system.servicemgr import service_mgr
from storlever.mngr.system.modulemgr import ModuleManager


MODULE_INFO = {
    "module_name": "NFS_export",
    "rpms": [
        "nfs-utils",
        "setup"
    ],
    "comment": "Provides the management functions for NFS server/export"
}


NFS_CONF_FILE_NAME = "nfs_conf.yaml"
NFS_ETC_CONF_DIR = "/etc/"
NFS_ETC_CONF_FILE = "exports"

EXPORT_CLIENT_CONF_SCHEMA = Schema({
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

    DoNotCare(str): object  # for all those key we don't care
})


EXPORT_POINT_CONF_SCHEMA = Schema({
    # absolute path
    "path": Use(str),

    # client list for this export point
    "clients": Default([EXPORT_CLIENT_CONF_SCHEMA],default=[]),

    DoNotCare(str): object  # for all those key we don't care

})

NFS_CONF_SCHEMA = Schema([EXPORT_POINT_CONF_SCHEMA])

class NfsManager(object):
    """contains all methods to manage ethernet interface in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.conf_file = os.path.join(STORLEVER_CONF_DIR, NFS_CONF_FILE_NAME)
        self.client_conf_schema = EXPORT_CLIENT_CONF_SCHEMA
        self.export_point_conf_schema = EXPORT_POINT_CONF_SCHEMA
        self.nfs_conf_schema = NFS_CONF_SCHEMA

    def _load_conf(self):
        nfs_conf = []
        cfg_mgr().check_conf_dir()
        if os.path.exists(self.conf_file):
            nfs_conf = \
                Config.from_file(self.conf_file, self.nfs_conf_schema).conf
        else:
            nfs_conf = self.nfs_conf_schema.validate(nfs_conf)
        return nfs_conf

    def _save_conf(self, nfs_conf):
        cfg_mgr().check_conf_dir()
        Config.to_file(self.conf_file, nfs_conf)

    def _export_point_to_file_line(self, export_point):

        export_line = export_point["path"];
        if len(export_point["clients"]) > 0:
            sep = "\t"
            for client in export_point["clients"]:
                client_line = client["host"]
                if len(client["options"]) > 0:
                    client_line += "(" + client["options"] + ")"
                export_line += sep + client_line
                sep = " "
        export_line += "\n"

        return export_line


    def _sync_to_system_conf(self, nfs_conf):

        if not os.path.exists(NFS_ETC_CONF_DIR):
            os.makedirs(NFS_ETC_CONF_DIR)

        nfs_sys_file = os.path.join(NFS_ETC_CONF_DIR, NFS_ETC_CONF_FILE)
        with open(os.path.join(nfs_sys_file, ), "r") as f:
            lines = f.readlines()

        if "# begin storlever\n" in lines:
            before_storlever = lines[0:lines.index("# begin storlever\n")]
        else:
            before_storlever = lines[0:]
            if not before_storlever[-1].endswith("\n"):
                before_storlever[-1] += "\n"

        if "# end storlever\n" in lines:
            after_storlever = lines[lines.index("# end storlever\n") + 1:]
        else:
            after_storlever = []

        with open(nfs_sys_file, "w") as f:
            f.writelines(before_storlever)
            f.write("# begin storlever\n")
            for export_point in nfs_conf:
                f.write(self._export_point_to_file_line(export_point))
            f.write("# end storlever\n")
            f.writelines(after_storlever)


    def sync_to_system_conf(self):
        """sync the nfs conf to /etc/exports"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        with self.lock:
            nfs_conf = self._load_conf()
            self._sync_to_system_conf(nfs_conf)

    def system_restore_cb(self):
        """sync the smb conf to /etc/samba/"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        os.remove(self.conf_file)

        with self.lock:
            smb_conf = self._load_conf()
            self._sync_to_system_conf(smb_conf)

    def get_export_list(self):
        with self.lock:
            nfs_conf = self._load_conf()
        return nfs_conf

    def get_export_conf(self, index):
        with self.lock:
            nfs_conf = self._load_conf()
        if index >= len(nfs_conf):
            raise StorLeverError("index(%d) not found" % (index), 404)

        return nfs_conf[index]

    def append_export_conf(self, path="/", clients=[], operator="unkown"):

        if path != "" and not os.path.exists(path):
             raise StorLeverError("path(%s) does not exists" % (path), 400)

        new_export_point = {
            "path": path,
            "clients": clients,
        }
        new_export_point = self.export_point_conf_schema.validate(new_export_point)

        with self.lock:
            nfs_conf = self._load_conf()

            for point in nfs_conf:
                if path == point["path"]:
                     raise StorLeverError("export points with path(%s) already in nfs export table" % (path), 400)

            nfs_conf.append(new_export_point)

            # save new conf
            self._save_conf(nfs_conf)
            self._sync_to_system_conf(nfs_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "export point with path(%s) config is added by operator(%s)" %
                   (path, operator))

        return len(nfs_conf) - 1

    def del_export_conf(self, index, operator="unkown"):
        with self.lock:
            nfs_conf = self._load_conf()
            if index >= len(nfs_conf):
                raise StorLeverError("index(%d) not found" % (index), 404)
            export_point = nfs_conf[index]
            del nfs_conf[index]

            # save new conf
            self._save_conf(nfs_conf)
            self._sync_to_system_conf(nfs_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "export point (path:%s) is deleted by operator(%s)" %
                   (export_point["path"], operator))

    def set_export_conf(self, index, path=None, clients=None, operator="unkown"):

        if path is not None and path != "" and not os.path.exists(path):
             raise StorLeverError("path(%s) does not exists" % (path), 400)

        with self.lock:
            nfs_conf = self._load_conf()
            if index >= len(nfs_conf):
                raise StorLeverError("index(%d) not found" % (index), 404)
            export_point = nfs_conf[index]

            if path is not None:
                export_point["path"] = path
            if clients is not None:
                export_point["clients"] = clients

            nfs_conf[index] = self.export_point_conf_schema.validate(export_point)

            # save new conf
            self._save_conf(nfs_conf)
            self._sync_to_system_conf(nfs_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "export point (index:%s) config is updated by operator(%s)" %
                   (index, operator))

    def add_client(self, export_index, host, options="", operator="unkown"):

        new_client = {
            "host":host,
            "options":options
        }
        new_client = self.client_conf_schema.validate(new_client)

        with self.lock:
            nfs_conf = self._load_conf()
            if export_index >= len(nfs_conf):
                raise StorLeverError("export_index (%d) not found" % (export_index), 404)
            export_point = nfs_conf[export_index]

            client_list = export_point["clients"]
            client_list.append(new_client)

            # save new conf
            self._save_conf(nfs_conf)
            self._sync_to_system_conf(nfs_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Client (%s) for export point (%s)is added by operator(%s)" %
                   (host, export_point["path"], operator))

        return len(client_list) - 1

    def del_client(self, export_index, client_index, operator="unkown"):
        with self.lock:
            nfs_conf = self._load_conf()
            if export_index >= len(nfs_conf):
                raise StorLeverError("export_index (%d) not found" % (export_index), 404)
            export_point = nfs_conf[export_index]

            client_list = export_point["clients"]
            if client_index >= len(client_list):
                raise StorLeverError("client_index (%d) not found" % (client_index), 404)
            client = client_list[client_index]
            del client_list[client_index]

            # save new conf
            self._save_conf(nfs_conf)
            self._sync_to_system_conf(nfs_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Client (%s) for export point (%s) is deleted by operator(%s)" %
                   (client["host"], export_point["path"], operator))

    def update_client(self, export_index, client_index, host=None, options=None, operator="unkown"):
        with self.lock:
            nfs_conf = self._load_conf()
            if export_index >= len(nfs_conf):
                raise StorLeverError("export_index (%d) not found" % (export_index), 404)
            export_point = nfs_conf[export_index]

            client_list = export_point["clients"]
            if client_index >= len(client_list):
                raise StorLeverError("client_index (%d) not found" % (client_index), 404)
            client = client_list[client_index]

            if host is not None:
                client["host"] = host
            if options is not None:
                client["options"] = options

            client_list[client_index] = self.client_conf_schema.validate(client)

            # save new conf
            self._save_conf(nfs_conf)
            self._sync_to_system_conf(nfs_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Client (%s) for export point (%s) is updated by operator(%s)" %
                   (client_list[client_index]["host"], export_point["path"], operator))


NfsManager = NfsManager()

# register ftp manager callback functions to basic manager
cfg_mgr().register_restore_from_file_cb(NfsManager.sync_to_system_conf)
cfg_mgr().register_system_restore_cb(NfsManager.system_restore_cb)
service_mgr().register_service("nfs", "nfs", "nfsd", "NFS Server")
service_mgr().register_service("rpcbind", "rpcbind", "rpcbind", "Universal addresses to RPC program number mapper")
service_mgr().register_service("nfslock", "nfslock", "rpc.statd", "NFS file locking service")
ModuleManager.register_module(**MODULE_INFO)

# disable selinux impact
set_selinux_permissive()

def nfs_mgr():
    """return the global user manager instance"""
    return NfsManager








