"""
storlever.mngr.san.tgt.tgtadmparse
~~~~~~~~~~~~~~~~

This module implements tgtadm show cmd output parser

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""
from storlever.lib.command import check_output, set_selinux_permissive
from storlever.lib.exception import StorLeverError
from tgtmgr import TGTADMIN_CMD

class ParseObject(dict):
    def __init__(self,*args, **kwargs):
        super(ParseObject, self).__init__(*args, **kwargs)
        self.value = ""
def leading_space_num(line):
    no_space_line = line.lstrip()
    return line.index(no_space_line)


def parse_lines(lines=[], value=""):
    obj = ParseObject()
    obj.value = value

    if len(lines) > 0:
        leading = leading_space_num(lines[0])
    else:
        leading = 0
    line_index = 0
    line_num = len(lines)
    while line_index < line_num:
        if leading_space_num(lines[line_index]) < leading:
            break;
        key, sep, value = lines[line_index].partition(":")
        key = key.strip()
        value = value.strip()
        line_index += 1
        if sep == "":
            continue
        if (line_index < line_num) \
            and (leading_space_num(lines[line_index]) > leading):
            parsed_num, tmpObj = parse_lines(lines[line_index:], value)
            line_index += parsed_num
        else:
            tmpObj = ParseObject()
            tmpObj.value = value
        if key in obj:
            if not isinstance(obj[key], list):
                obj[key] = [obj[key]]
            obj[key].append(tmpObj)
        else:
            obj[key] = tmpObj

    return line_index, obj


class TgtStatus(object):
    def __init__(self):
        pass
    def _get_target_info(self, iqn):
        output_lines = check_output([TGTADMIN_CMD, "-s"]).split("\n")
        line_num, root = parse_lines(output_lines)
        for k,v in root.items():
            if v.value == iqn:
                return v
        raise StorLeverError("The target (%s) Not Found" % (iqn), 404)

    def get_target_state(self, iqn):
        try:
            target = self._get_target_info(iqn)
        except StorLeverError:
            return "error"
        return target["System information"]["State"].value

    def get_target_sessions(self, iqn):
        sessions = []
        try:
            target = self._get_target_info(iqn)
        except StorLeverError:
            return sessions

        nexus_info = target["I_T nexus information"]
        if "I_T nexus" not in nexus_info:
            return sessions

        if not isinstance(nexus_info["I_T nexus"], list):
            nexus_info["I_T nexus"] = [nexus_info["I_T nexus"]]

        for nexus in nexus_info["I_T nexus"]:
            if "Connection" in nexus and isinstance(nexus["Connection"], list):
                addr = nexus["Connection"][0]["IP Address"].value
            elif  "Connection" in nexus:
                addr = nexus["Connection"]["IP Address"].value
            else:
                addr = ""

            sessions.append({
                "initiator":nexus["Initiator"].value,
                "addr": addr
            })

        return sessions

TgtStatus = TgtStatus()
def tgt_status():
    return TgtStatus
