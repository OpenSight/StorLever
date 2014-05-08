"""
storlever.mngr.fs.nfs
~~~~~~~~~~~~~~~~

nfs filesystem class..

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

from storlever.lib.command import check_output
from storlever.mngr.fs.fs import FileSystem
from storlever.mngr.fs.fsmgr import FileSystemManager
from storlever.lib.exception import StorLeverError, StorLeverCmdError
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "nfs_client",
    "rpms": [
        "nfs-utils",
        "rpcbind"
    ],
    "comment": "Provides the nfs filesystem type support"
}


RPCINFO_CMD = "/usr/sbin/rpcinfo"
NFSSTAT_CMD = "/usr/sbin/nfsstat"

class Nfs(FileSystem):

    @staticmethod
    def _get_nfs_transport_proto(mount_options):
        option_list =mount_options.split(",")
        for option in option_list:
            option = option.strip().lower()
            if option == "udp" or option.startswith("proto=udp"):
                return "udp"
            if option == "tcp" or option.startswith("proto=tcp"):
                return "tcp"
        return ""

    @staticmethod
    def _is_nfs_service_available(ip, mount_options):
        proto = Nfs._get_nfs_transport_proto(mount_options)
        if proto == "":  # detect automatically
            cmd = [RPCINFO_CMD, "-s", ip]
            try:
                result = check_output(cmd)
                if "nfs" in result:
                    return True
            except StorLeverCmdError as e:
                if e.return_code == 1:
                    pass
                else:
                    raise
        else:
            if proto == "udp":
                cmd = [RPCINFO_CMD, "-u", ip, "nfs"]
            elif proto == "tcp":
                cmd = [RPCINFO_CMD, "-t", ip, "nfs"]
            try:
                result = check_output(cmd)
                return True
            except StorLeverCmdError as e:
                if e.return_code == 1:
                    pass
                else:
                    raise
        return False


    @staticmethod
    def _parse_dev_file(dev_file):
        dev_file = str(dev_file)
        if ":" not in dev_file:
            raise StorLeverError("dev_file is not nfs source format (IP:Path)", 400)
        ip, sep, path = dev_file.partition(":")
        ip = ip.strip()
        path = path.strip()
        if len(ip) == 0 or len(path) == 0:
            raise StorLeverError("dev_file is not nfs source format (IP:Path)", 400)
        return ip, path

    @classmethod
    def mkfs(cls, type, dev_file, fs_options=""):
        ip, path = Nfs._parse_dev_file(dev_file)
        if not Nfs._is_nfs_service_available(ip, ""):
            raise StorLeverError("NFS service on %s is not available" % ip, 400)

    def is_available(self):
        result = super(Nfs, self).is_available()
        if result:
            # check nfs service available on the remote host
            ip, path = Nfs._parse_dev_file(self.fs_conf["dev_file"])
            result = Nfs._is_nfs_service_available(ip, self.mount_options)
        return result

    def mount(self):
        # check nfs service available on the remote host
        ip, path = Nfs._parse_dev_file(self.fs_conf["dev_file"])
        if not Nfs._is_nfs_service_available(ip, self.mount_options):
            raise StorLeverError("NFS service on %s is not available" % ip, 400)

        check_output(["/bin/mount", "-t", self.fs_conf["type"],
                     "-o", self.mount_options,
                     self.fs_conf["dev_file"], self.fs_conf["mount_point"]],
                     input_ret=[32])
        # nfs does not support and no needs quota_check and quota_on

    def fs_meta_dump(self):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 500)
        return check_output([NFSSTAT_CMD, "-c", "-l"])

    def quota_check(self):
        # nfs has no quota support
        pass

    def quota_user_report(self):
        # nfs has no quota support
        return []

    def quota_group_report(self):
        # nfs has no quota support
        return []

    def quota_user_set(self, user,
                       block_softlimit=0,
                       block_hardlimit=0,
                       inode_softlimit=0,
                       inode_hardlimit=0,
                       operator="unknown"):
        # nfs has no quota support
        raise StorLeverError("NFS does not support quota", 500)

    def quota_group_set(self, group,
                        block_softlimit=0,
                        block_hardlimit=0,
                        inode_softlimit=0,
                        inode_hardlimit=0,
                        operator="unknown"):
        # nfs has no quota support
        raise StorLeverError("NFS does not support quota", 500)

ModuleManager.register_module(**MODULE_INFO)

# register to fs manager
FileSystemManager.add_fs_type("nfs", Nfs)
