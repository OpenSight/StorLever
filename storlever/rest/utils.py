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
from storlever.rest.common import get_params_from_request

def includeme(config):

    config.add_route('ntp_server_list', '/utils/ntp/server_list')
    config.add_route('ntp_restrict_list', '/utils/ntp/restrict_list')
    config.add_route('ntp_peer_list', '/utils/ntp/peer_list')

    config.add_route('mail_conf', '/utils/mail/conf')
    config.add_route('send_mail', '/utils/mail/send_mail')

    config.add_route('smartd_monitor_list', '/utils/smartd/monitor_list')

    config.add_route('zabbix_conf', '/utils/zabbix/conf')
    config.add_route('zabbix_active_server_list', '/utils/zabbix/active_server_list')
    config.add_route('zabbix_passive_server_list', '/utils/zabbix/passive_server_list')




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

    DoNotCare(str): object  # for all other key we don't care
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
    Optional("mask"): Default(Use(str), default=""),


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

    DoNotCare(str): object  # for all other key we auto delete

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
    Optional("smtp_server"):  Use(str),

    # password for the account
    Optional("password"):  Use(str),


    DoNotCare(str): object  # for all other key we auto delete
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

    # password for the account
    Optional("content"):  Default(Use(str), default=""),

    Optional("debug"): Default(BoolVal(), default=False),

    DoNotCare(str): object  # for all other key we auto delete
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

    DoNotCare(str): object  # for all other key we don't care

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

    DoNotCare(str): object  # for all other key we don't care
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
