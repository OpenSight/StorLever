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
    Default, DoNotCare, BoolVal, IntVal, StrRe, AutoDel
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

    AutoDel(str): object  # for all other key we auto delete
})


EXPORT_POINT_CONF_SCHEMA = Schema({
    # export point name
    "name": Use(str),

    # absolute path
    "path": Use(str),

    # client list for this export point
    Optional("clients"): Default([EXPORT_CLIENT_CONF_SCHEMA],default=[]),

    AutoDel(str): object  # for all other key we auto delete

})

NFS_CONF_SCHEMA = Schema({
    Optional("export_point_list"): Default([EXPORT_POINT_CONF_SCHEMA], default=[]),
    AutoDel(str): object  # for all other key we auto delete
})

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
        nfs_conf = {}
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
        if os.path.exists(nfs_sys_file):
            with open(nfs_sys_file, "r") as f:
                lines = f.readlines()
        else:
            lines = []

        if "# begin storlever\n" in lines:
            before_storlever = lines[0:lines.index("# begin storlever\n")]
        else:
            before_storlever = lines[0:]
            if before_storlever and (not before_storlever[-1].endswith("\n")):
                before_storlever[-1] += "\n"

        if "# end storlever\n" in lines:
            after_storlever = lines[lines.index("# end storlever\n") + 1:]
        else:
            after_storlever = []

        with open(nfs_sys_file, "w") as f:
            f.writelines(before_storlever)
            f.write("# begin storlever\n")
            for export_point in nfs_conf["export_point_list"]:
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
            nfs_conf = self._load_conf()
            self._sync_to_system_conf(nfs_conf)

    def get_export_list(self):
        with self.lock:
            nfs_conf = self._load_conf()
        return nfs_conf["export_point_list"]

    def get_export_conf(self, name):
        with self.lock:
            nfs_conf = self._load_conf()
        for export_point in nfs_conf["export_point_list"]:
            if export_point["name"] == name:
                return export_point
        else:
            raise StorLeverError("export(%s) not found" % (name), 404)


    def append_export_conf(self, name, path="/", clients=[], operator="unkown"):

        if path != "" and not os.path.exists(path):
             raise StorLeverError("path(%s) does not exists" % (path), 400)

        new_export_point = {
            "name": name,
            "path": path,
            "clients": clients,
        }
        new_export_point = self.export_point_conf_schema.validate(new_export_point)

        with self.lock:
            nfs_conf = self._load_conf()

            # check duplication
            for point in nfs_conf["export_point_list"]:
                if path == point["path"]:
                    raise StorLeverError("export with path(%s) already in nfs export table" % (path), 400)
                if name == point["name"]:
                    raise StorLeverError("export with name(%s) already in nfs export table" % (name), 400)

            nfs_conf["export_point_list"].append(new_export_point)

            # save new conf
            self._save_conf(nfs_conf)
            self._sync_to_system_conf(nfs_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "NFS export with path(%s) config is added by operator(%s)" %
                   (path, operator))

    def del_export_conf(self, name, operator="unkown"):
        with self.lock:
            nfs_conf = self._load_conf()
            for point in nfs_conf["export_point_list"]:
                if name == point["name"]:
                    break
            else:
                raise StorLeverError("export(%s) not found" % (name), 404)

            nfs_conf["export_point_list"].remove(point)

            # save new conf
            self._save_conf(nfs_conf)
            self._sync_to_system_conf(nfs_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "NFS export (%s) is deleted by operator(%s)" %
                   (point["path"], operator))

    def set_export_conf(self, name, path=None, clients=None, operator="unkown"):

        if path is not None and path != "" and not os.path.exists(path):
             raise StorLeverError("path(%s) does not exists" % (path), 400)

        with self.lock:
            nfs_conf = self._load_conf()
            for index, point in enumerate(nfs_conf["export_point_list"]):
                if name == point["name"]:
                    break
            else:
                raise StorLeverError("export(%s) not found" % (name), 404)

            if path is not None:
                point["path"] = path
            if clients is not None:
                point["clients"] = clients

            nfs_conf["export_point_list"][index] = self.export_point_conf_schema.validate(point)

            # save new conf
            self._save_conf(nfs_conf)
            self._sync_to_system_conf(nfs_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "NFS export (name:%s) config is updated by operator(%s)" %
                   (name, operator))


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








