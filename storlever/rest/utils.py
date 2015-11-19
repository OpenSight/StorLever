"""
storlever.rest.utils
~~~~~~~~~~~~~~~~

This module implements the rest API for utils.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""



from storlever.rest.common import get_view, post_view, put_view, delete_view
from pyramid.response import Response

from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError, BoolVal, StrRe, ListVal
from storlever.lib.exception import StorLeverError
from storlever.mngr.utils import ntpmgr
from storlever.mngr.utils import mailmgr
from storlever.mngr.utils import smartdmgr
from storlever.mngr.utils import zabbixagent
from storlever.mngr.utils import snmpagent
from storlever.rest.common import get_params_from_request

def includeme(config):

    config.add_route('ntp_server_list', '/utils/ntp/server_list')
    config.add_route('ntp_restrict_list', '/utils/ntp/restrict_list')
    config.add_route('ntp_peer_list', '/utils/ntp/peer_list')

    config.add_route('mail_conf', '/utils/mail/conf')
    config.add_route('send_mail', '/utils/mail/send_mail')

    config.add_route('smartd_monitor_list', '/utils/smartd/monitor_list')

    config.add_route('zabbix_conf', '/utils/zabbix_agent/conf')
    config.add_route('zabbix_active_server_list', '/utils/zabbix_agent/active_server_list')
    config.add_route('zabbix_passive_server_list', '/utils/zabbix_agent/passive_server_list')


    config.add_route('snmp_agent_conf', '/utils/snmp_agent/conf')
    config.add_route('snmp_agent_community_list', '/utils/snmp_agent/community_list')
    config.add_route('snmp_agent_community_info', '/utils/snmp_agent/community_list/{community_name}')
    config.add_route('snmp_agent_monitor_list', '/utils/snmp_agent/monitor_list')
    config.add_route('snmp_agent_monitor_info', '/utils/snmp_agent/monitor_list/{monitor_name}')
    config.add_route('snmp_agent_trap_sink_list', '/utils/snmp_agent/trap_sink_list')

@get_view(route_name='ntp_server_list')
def get_ntp_server_list(request):
    ntp_mgr = ntpmgr.NtpManager
    return ntp_mgr.get_server_conf_list()


ntp_server_list_schema = Schema([{
    # it can be a ipv4 address, ipv6 address, or host dns name
    "server_addr":StrRe(r"^\S+$"),
    # if set to True, it would be forced to resolve the host name to
    # ipv6 address in DNS resolution
    Optional("ipv6"):  Default(BoolVal(), default=False),

    # Marks the server as preferred.  All other things being equal,
    # this host will be chosen for synchronization among set of correctly operating hosts
    Optional("prefer"): Default(BoolVal(), default=False),

    # Specifies a mode number which is interpreted in a device
    # specific fashion.	For instance, it selects a dialing,
    # protocol in the ACTS driver and a device subtype in the
    # parse drivers.
    # Only valid for reference clock server, i.e. server_addr is 127.127.t.n
    Optional("mode"): Default(IntVal(min=0, max=65535), default=0),


    # Specifies the stratum number assigned to the driver, an
    # integer between 0 and 15.	This number overrides the
    # default stratum number ordinarily assigned	by the driver
    # itself, usually zero.
    # Only valid for reference clock server, i.e. server_addr is 127.127.t.n
    Optional("stratum"): Default(IntVal(min=0, max=15), default=0),

    # These four flags are used for customizing the clock
    # driver.  The interpretation of these values, and whether
    # they are used at all, is a function of the	particular
    # clock driver. However, by convention flag4 is used to
    # enable recording monitoring data to the clockstats file
    # configured with the filegen command.  Further information
    # on the filegen command can be found in Monitoring
    # Options.
    # Only valid for reference clock server, i.e. server_addr is 127.127.t.n
    Optional("flag1"): Default(IntVal(min=0, max=1), default=0),
    Optional("flag2"): Default(IntVal(min=0, max=1), default=0),
    Optional("flag3"): Default(IntVal(min=0, max=1), default=0),
    Optional("flag4"): Default(IntVal(min=0, max=1), default=0),

    DoNotCare(Use(str)): object  # for all other key we don't care
}])

@put_view(route_name='ntp_server_list')
def put_ntp_server_list(request):
    ntp_mgr = ntpmgr.NtpManager
    new_server_list = get_params_from_request(request, ntp_server_list_schema)
    ntp_mgr.set_server_conf_list(new_server_list, operator=request.client_addr)
    return Response(status=200)


@get_view(route_name='ntp_restrict_list')
def get_ntp_restrict_list(request):
    ntp_mgr = ntpmgr.NtpManager
    return ntp_mgr.get_restrict_list()


ntp_restrict_list_schema = Schema([{

    # it can be a ipv4 address, ipv6 address, or "default"
    "restrict_addr": StrRe(r"^\S+$"),

    # if set to True, it would be forced to restrict to ipv6 addr
    Optional("ipv6"):  Default(BoolVal(), default=False),

    # mask the restrict_addr to indicate the network address.
    # for ipv4, is xxx.xxx.xxx.xxx. for ipv6 is xxxx:xxxx:xxxx::
    # default is empty, which is equal to 255.255.255.255
    Optional("mask"): Default(StrRe(r"^\S*$"), default=""),


    # Deny packets of all kinds,	including ntpq(8) and ntpdc(8) queries
    Optional("ignore"): Default(BoolVal(), default=False),

    # Deny ntpq(8) and ntpdc(8) queries which attempt to	modify
    # the state of the server (i.e., run	time reconfiguration).
    # Queries which return information are permitted
    Optional("nomodify"): Default(BoolVal(), default=False),

    # Deny ntpq(8) and ntpdc(8) queries. Time service is not affected
    Optional("noquery"): Default(BoolVal(), default=False),

    # Deny all packets except ntpq(8) and ntpdc(8) queries.
    Optional("noserve"): Default(BoolVal(), default=False),

    # Decline to	provide	mode 6 control message trap service to
    # matching hosts.  The trap service is a subsystem of the
    # ntpdq control message protocol which is intended for use
    # by	remote event logging programs
    Optional("notrap"): Default(BoolVal(), default=False),

    DoNotCare(Use(str)): object  # for all other key we auto delete

}])

@put_view(route_name='ntp_restrict_list')
def put_ntp_restrict_list(request):
    ntp_mgr = ntpmgr.NtpManager
    new_restrict_list = get_params_from_request(request, ntp_restrict_list_schema)
    ntp_mgr.set_restrict_list(new_restrict_list, operator=request.client_addr)
    return Response(status=200)


@get_view(route_name='ntp_peer_list')
def get_ntp_peer_list(request):
    ntp_mgr = ntpmgr.NtpManager
    return ntp_mgr.get_peer_list()




@get_view(route_name='mail_conf')
def get_mail_conf(request):
    mail_mgr = mailmgr.MailManager
    return mail_mgr.get_mail_conf()

mail_conf_schema=Schema({

    # the email address of user's account, it would also be place in the FROM header of the email
    Optional("email_addr"):  StrRe(r"^(|\w+([-+.]\w+)*@\w+([-.]\w+)*)$"),

    # smtp server address or domain name to send the mail
    Optional("smtp_server"):  StrRe(r"^\S*$"),

    # password for the account
    Optional("password"):  StrRe(r"^\S*$"),


    DoNotCare(Use(str)): object  # for all other key we auto delete
})

@put_view(route_name='mail_conf')
def put_mail_conf(request):
    mail_mgr = mailmgr.MailManager
    mail_conf = get_params_from_request(request, mail_conf_schema)
    mail_mgr.set_mail_conf(mail_conf, operator=request.client_addr)
    return Response(status=200)


send_mail_schema=Schema({

    # to email addr
    Optional("to"):  StrRe(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*$"),

    # subject
    Optional("subject"):  StrRe(r"^\S+$"),

    Optional("content"):  Default(Use(str), default=""),

    Optional("debug"): Default(BoolVal(), default=False),

    DoNotCare(Use(str)): object  # for all other key we don't care
})


@post_view(route_name='send_mail')
def post_send_mail(request):
    mail_mgr = mailmgr.MailManager
    send_mail_conf = get_params_from_request(request, send_mail_schema)
    info = mail_mgr.send_email(send_mail_conf["to"], send_mail_conf["subject"],
                               send_mail_conf["content"], send_mail_conf["debug"])
    return {"debug_info":info}


@get_view(route_name='smartd_monitor_list')
def get_smartd_monitor_list(request):
    smartd_mgr = smartdmgr.SmartdManager
    return smartd_mgr.get_monitor_list()


smartd_monitor_list_schema = Schema([{

    # the dev's file to monitor
    "dev":  StrRe(r"^\S+$"),

    # the (e)mail address to which smartd would send when a error is detected.
    #  To  send email to more than one user, please use the following "comma separated"
    # form for the address: user1@add1,user2@add2,...,userN@addN (with no spaces).
    Optional("mail_to"): Default(StrRe(r"^(|\w+([-+.]\w+)*@\w+([-.]\w+)*(,\w+([-+.]\w+)*@\w+([-.]\w+)*)*)$"), default=""),

    # test the mail. if true, send a single test email immediately upon smartd  startup.
    # This  allows one to verify that email is delivered correctly
    Optional("mail_test"): Default(BoolVal(), default=False),

    # run the executable PATH instead of the default mail command.
    # if this list is empty, smartd would run the default "/bin/mail" utility
    # to send warning email to user in "mail_to" option. Otherwise, smartd would run
    # the scripts in this option. See man smartd.conf
    # for more detail
    Optional("mail_exec"): Default(StrRe(r"^\S*$"), default=""),

    # Run Self-Tests or Offline Immediate Tests,  at  scheduled  times.   A  Self-  or
    # Offline Immediate Test will be run at the end of periodic device polling, if all
    # 12 characters of the string T/MM/DD/d/HH match the extended  regular  expression
    # REGEXP. See man smartd.conf for detail.
    # if this option is empty, no schedule test at all
    Optional("schedule_regexp"): Default(StrRe(r"^\S*$"), default=""),

    DoNotCare(Use(str)): object  # for all other key we don't care

}])

@put_view(route_name='smartd_monitor_list')
def put_smartd_monitor_list(request):
    smartd_mgr = smartdmgr.SmartdManager
    new_monitor_list = get_params_from_request(request, smartd_monitor_list_schema)
    smartd_mgr.set_monitor_list(new_monitor_list, operator=request.client_addr)
    return Response(status=200)




@get_view(route_name='zabbix_conf')
def get_zabbix_conf(request):
    zabbix_agent = zabbixagent.ZabbixAgentManager
    return zabbix_agent.get_agent_conf()

zabbix_conf_schema=Schema({

    # used for active check, this name must match the hostname set in the active server
    Optional("hostname"):  StrRe(r"^\S+$"),

    # How often list of active checks is refreshed, in seconds.
    # Note that after failing to refresh active checks the next refresh
    # will be attempted after 60 seconds.
    Optional("refresh_active_check"): IntVal(min=60, max=3600),

    DoNotCare(Use(str)): object  # for all other key we don't care
})

@put_view(route_name='zabbix_conf')
def put_zabbix_conf(request):
    zabbix_agent = zabbixagent.ZabbixAgentManager
    zabbix_conf = get_params_from_request(request, zabbix_conf_schema)
    zabbix_agent.set_agent_conf(zabbix_conf, operator=request.client_addr)
    return Response(status=200)


@get_view(route_name='zabbix_active_server_list')
def get_zabbix_active_server_list(request):
    zabbix_agent = zabbixagent.ZabbixAgentManager
    return zabbix_agent.get_active_check_server_list()

# only support ipv4 server address now
zabbix_active_server_list_schema=Schema(ListVal(StrRe(r"\w+([-+.]\w+)*(:\d+)?$")))

@put_view(route_name='zabbix_active_server_list')
def put_zabbix_active_server_list(request):
    zabbix_agent = zabbixagent.ZabbixAgentManager
    server_list_conf = get_params_from_request(request, zabbix_active_server_list_schema)
    zabbix_agent.set_active_check_server_list(server_list_conf, operator=request.client_addr)
    return Response(status=200)



@get_view(route_name='zabbix_passive_server_list')
def get_zabbix_passive_server_list(request):
    zabbix_agent = zabbixagent.ZabbixAgentManager
    return zabbix_agent.get_passive_check_server_list()


# only support ipv4 server address now
zabbix_passive_server_list_schema=Schema(ListVal(StrRe(r"\w+([-+.]\w+)*$")))

@put_view(route_name='zabbix_passive_server_list')
def put_zabbix_passive_server_list(request):
    zabbix_agent = zabbixagent.ZabbixAgentManager
    server_list_conf = get_params_from_request(request, zabbix_passive_server_list_schema)
    zabbix_agent.set_passive_check_server_list(server_list_conf, operator=request.client_addr)
    return Response(status=200)



snmp_conf_schema = Schema({

    # set the system location,  system  contact  or  system  name  (sysLocation.0,
    # sysContact.0  and  sysName.0)  for the agent respectively.  Ordinarily these
    # objects are writeable via suitably authorized SNMP SET  requests if these object
    # are empty,  However, specifying one of these directives makes the corresponding object read-only,
    # and attempts to SET it will result in a notWritable error response.
    Optional("sys_location"): StrRe(r"^\S*$"),
    Optional("sys_contact"):  StrRe(r"^\S*$"),
    Optional("sys_name"):  StrRe(r"^\S*$"),

    # defines  a  list  of  listening addresses(separated by commas), on which to receive incoming SNMP
    # requests.  See the section LISTENING ADDRESSES in the snmpd(8)  manual  page
    # for more information about the format of listening addresses.
    # if it's empty, it would be the default address and port
    Optional("agent_address"):  StrRe(r"^\S*$"),

    # specifies  the  default  SNMPv3  username,  to  be used when making internal
    # queries to retrieve any necessary information  (either  for  evaluating  the
    # monitored  expression,  or building a notification payload).  These internal
    # queries always use SNMPv3, even if normal querying  of  the  agent  is  done
    # using SNMPv1 or SNMPv2c.
    Optional("iquery_sec_name"): StrRe(r"^\S+$"),

    # monitor the interface link up and down
    Optional("link_up_down_notifications"): BoolVal(),

    # enable the default monitors for system
    Optional("default_monitors"):BoolVal(),

    # system 1 minutes load max threshold for default load monitor,
    # if it's 0, this monitor never report error
    Optional("load_max"): Use(float),

    # swap space min threshold for default memory monitor, in kB
    Optional("swap_min"): Use(int),

    # disk space min percent for the default disk usage monitor, 0 means never report error
    Optional("disk_min_percent"): IntVal(0, 99),

    DoNotCare(Use(str)): object  # for all other key we don't care
})



@get_view(route_name='snmp_agent_conf')
def get_snmp_agent_conf(request):
    snmp_agent = snmpagent.SnmpAgentManager
    return snmp_agent.get_basic_conf()

@put_view(route_name='snmp_agent_conf')
def put_snmp_agent_conf(request):
    snmp_agent = snmpagent.SnmpAgentManager
    snmp_conf = get_params_from_request(request, snmp_conf_schema)
    snmp_agent.set_basic_conf(snmp_conf, operator=request.client_addr)
    return Response(status=200)





@get_view(route_name='snmp_agent_community_list')
def get_snmp_agent_community_list(request):
    snmp_agent = snmpagent.SnmpAgentManager
    return snmp_agent.get_community_list()



snmp_community_schema = Schema({


    "community_name": StrRe(r"^\S+$"),

    # if set to True, it would be forced to resolve the host name to
    # ipv6 address in DNS resolution
    Optional("ipv6"):  BoolVal(),

    # restrict  access from the specified source.
    #  A restricted source  can either be a specific hostname (or address), or a subnet - repre-
    # sented  as  IP/MASK  (e.g.  10.10.10.0/255.255.255.0),  or   IP/BITS   (e.g.
    # 10.10.10.0/24), or the IPv6 equivalents.
    # if it's empty, it would give access to any system, that means "global" range
    Optional("source"): StrRe(r"^\S*$"),

    #  this field restricts access for that community to  the
    # subtree rooted at the given OID.
    # if it's empty, the whole tree would be access
    Optional("oid"): StrRe(r"^\S*$"),

    # if set to True, this commnunity can only read the oid tree.
    # Or, it can set the the oid tree
    Optional("read_only"):  BoolVal(),

    DoNotCare(Use(str)): object  # for all other key we don't care
})


@post_view(route_name='snmp_agent_community_list')
def post_snmp_agent_community_list(request):
    snmp_agent = snmpagent.SnmpAgentManager
    new_community_conf = get_params_from_request(request, snmp_community_schema)
    snmp_agent.add_community_conf(new_community_conf["community_name"],
                                  new_community_conf.get("ipv6", False),
                                  new_community_conf.get("source", ""),
                                  new_community_conf.get("oid", ""),
                                  new_community_conf.get("read_only", False),
                                  operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('snmp_agent_community_info',
                                      community_name=new_community_conf["community_name"])
    return resp




@get_view(route_name='snmp_agent_community_info')
def get_snmp_agent_community_info(request):
    community_name = request.matchdict['community_name']
    snmp_agent = snmpagent.SnmpAgentManager
    return snmp_agent.get_community_conf(community_name)




@put_view(route_name='snmp_agent_community_info')
def put_snmp_agent_community_info(request):
    community_name = request.matchdict['community_name']
    snmp_agent = snmpagent.SnmpAgentManager
    community_info = get_params_from_request(request)
    community_info["community_name"] = community_name
    community_info = snmp_community_schema.validate(community_info)

    snmp_agent.update_community_conf(community_name,
                                     community_info.get("ipv6"),
                                     community_info.get("source"),
                                     community_info.get("oid"),
                                     community_info.get("read_only"),
                                     operator=request.client_addr)
    return Response(status=200)

@delete_view(route_name='snmp_agent_community_info')
def delete_snmp_agent_community_info(request):
    community_name = request.matchdict['community_name']
    snmp_agent = snmpagent.SnmpAgentManager
    snmp_agent.del_community_conf(community_name, operator=request.client_addr)
    return Response(status=200)


@get_view(route_name='snmp_agent_monitor_list')
def get_snmp_agent_monitor_list(request):
    snmp_agent = snmpagent.SnmpAgentManager
    return snmp_agent.get_monitor_list()


snmp_monitor_new_schema = Schema({

    # monitor name
    "monitor_name": StrRe(r"^\w+$"),

    # options to control the monitor's behavior,
    # see monitor options section of man snmpd.conf for more detail
    Optional("option"): Default(Use(str), default=""),

    # expression to check of this monitor,
    #  see monitor expression of man snmpd.conf for more detail
    "expression":  Use(str),

    DoNotCare(Use(str)): object  # for all other key we don't care
})

@post_view(route_name='snmp_agent_monitor_list')
def post_snmp_agent_monitor_list(request):
    snmp_agent = snmpagent.SnmpAgentManager
    new_monitor_conf = get_params_from_request(request, snmp_monitor_new_schema)
    snmp_agent.add_monitor_conf(new_monitor_conf["monitor_name"],
                                new_monitor_conf["expression"],
                                new_monitor_conf["option"],
                                operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('snmp_agent_monitor_info',
                                      monitor_name=new_monitor_conf["monitor_name"])
    return resp



@get_view(route_name='snmp_agent_monitor_info')
def get_snmp_agent_monitor_info(request):
    monitor_name = request.matchdict['monitor_name']
    snmp_agent = snmpagent.SnmpAgentManager
    return snmp_agent.get_monitor_conf(monitor_name)


snmp_monitor_mod_schema = Schema({


    # options to control the monitor's behavior,
    # see monitor options section of man snmpd.conf for more detail
    Optional("option"): Use(str),

    # expression to check of this monitor,
    #  see monitor expression of man snmpd.conf for more detail
    Optional("expression"):  Use(str),

    DoNotCare(Use(str)): object  # for all other key we don't care
})

@put_view(route_name='snmp_agent_monitor_info')
def put_snmp_agent_monitor_info(request):
    monitor_name = request.matchdict['monitor_name']
    snmp_agent = snmpagent.SnmpAgentManager
    monitor_info = get_params_from_request(request, snmp_monitor_mod_schema)

    snmp_agent.update_monitor_conf(monitor_name,
                                   monitor_info.get("expression"),
                                   monitor_info.get("option"),
                                   operator=request.client_addr)

    return Response(status=200)

@delete_view(route_name='snmp_agent_monitor_info')
def delete_snmp_agent_monitor_info(request):
    monitor_name = request.matchdict['monitor_name']
    snmp_agent = snmpagent.SnmpAgentManager
    snmp_agent.del_monitor_conf(monitor_name, operator=request.client_addr)
    return Response(status=200)


snmp_trap_sink_list_schema = Schema([{


    # address of the host to which send the trap
    "host": StrRe(r"^\S+$"),

    # trap type, can only be set to trap/trap2/inform,
    # which would send SNMPv1 TRAPs, SNMPv2c TRAP2s,
    # or SNMPv2 INFORM notifications respectively
    Optional("type"): Default(StrRe(r"^trap|trap2|inform$"), default="trap"),

    # community name used by this sink
    Optional("community"):  Default(StrRe(r"^\S+$"), default="public"),


    DoNotCare(Use(str)): object  # for all other key we don't care


}])


@get_view(route_name='snmp_agent_trap_sink_list')
def get_snmp_agent_trap_sink_list(request):
    snmp_agent = snmpagent.SnmpAgentManager
    return snmp_agent.get_trap_sink_list()


@put_view(route_name='snmp_agent_trap_sink_list')
def put_snmp_agent_trap_sink_list(request):
    snmp_agent = snmpagent.SnmpAgentManager
    new_sink_list = get_params_from_request(request, snmp_trap_sink_list_schema)
    snmp_agent.set_trap_sink_list(new_sink_list, operator=request.client_addr)
    return Response(status=200)