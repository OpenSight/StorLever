Introduction
===========

StorLever is a management, configuration, monitor system for storage & network resource in Linux, 
which provides a set of well-designed REST-styled web API as well as a web panel. 

The primary goal of StorLever is to ease the management of storage resources on Linux server. 
Built on top of existing Linux management tools, StorLever provides a user-friendly web panel 
for Linux system administrators, which can reduce the learning curve and enhance the user experience for them. 

Besides web panel, StorLever offers a set of RESTful-style(HTTP+JSON) APIs to manage the Linux system remotely, 
which is another powerful feature. Based on it, the third-party management software on another host
(such as central manage system) can easily take over the remote Linux system no matter what language and platform 
it is built on. Human can pleasently understand the REST API's output as well as the computer program can interpret it easily.
Any program language has its mature library to handle HTTP protocol and interpret JSON string. SDK for StorLever 
can easily develop on any language and platform.

StorLever focus on the management of storage resource of Linux system, which is the most diverse and difficult part 
of Linux, including block device, LVM, MD, FileSystem, NAS, IP-SAN  and etc. They are usually the nightmare for system 
administrators, and often take a week or more time of them to configure these functions but not sure they are working in
the best state. StorLever is the Saviour of them. 
Through accumulating many storage management experience and export a clear, simple interface, StorLever can solve these 
problem in minutes. 

StorLever is not just a frozen software, but also a extensible framework. Anyone who want to manage another object by StorLever, 
can easily develop an extension(plug-in) for it in a separate project without changing even one line code of it.

StorLever is built on the pure python so that it's simple, understandable, stable and reliable, easy to develop and deploy, 
The principle of StorLever's design is Simple, Extensible, Easy to use.
 

Highlights:
----------------

* Integrates various storage technologies of Linux, LVM, Raid, NAS/SAN, etc.
* Provides various form of interface for remote control, RESTful API, Web Page, CLI(in sub-project), SDK(in sub-project)
* Extensible, easy to add a extension for it
* Simple, pure python


Storage Resources
-----------------

By "storage resources" we mean block devices, RAID, LVM, NAS etc.
Following is a non-exhaustive list of what is under the control of the newest StorLever:

* Block device
* SCSI device
* MD Raid
* LSI Raid (LSISAS2108, LSISAS2008 chip)
* LVM
* XFS
* EXT4
* NFS(Client & Server)
* SAMBA
* FTP
* iSCSI(Initiator & Target)

For the complete list of software packages involved, check out the dependency document.

Why StorLever
-------------------
Traditionally, Linux distribution would provides two kinds of local operation interface for 
system administrator, typical CLI and GUI. They used to be the most popular approach to manage
Linux system. As the network, especially Internet becomes universal,  Linux system usually locates
on the remote machine(especially VPS, Virtual Private Sever). Local interface does not make sense 
any more, administrator like to use SSH to login the remote system to manage them. Management with 
SSH is flexible, but difficult, not friendly. Some Web Control Panel project is developed to assist 
the administrators to manage the remote system. 
With the popularity of cloud computing, many VPS must be managed by the administrators, so that they 
need the assist of a central management platform to perform the management task, which need the APIs
of the remote system. 
StorLever is the answer of these problem.

Why Web API
-----------

All those "resources" mentioned above, come with their own utilities like command line
and configuration files for the management purpose, but unfortunately all in different style.
To master all those the command lines and configuration files requires non-trivial effort, 
and to access these utilities remotely and programmatically requires another set of skills,
which make things even worse.

So StorLever comes to the rescue. By providing a set of uniformed, well-designed web API, 
we abstract away all the configuration and command line details, with simplicity and consistency
in mind during API designing, people will find them easy to understand. 

All those API are HTTP based, which makes them totally platform and programming language independent.

Differences with other similar projects
---------------------------------------

There are already projects like openfiler which service the similar purpose, but what's
the difference?

Openfiler or freeNAS are both storage systems delivered with the whole operation system
and all the utilities sit on it, on the contrary, StorLever is only a set of API that helps the user
to ease the management of storage resources. It is based on top of existing management tools in Linux 
distribution, e.g. RHEL/CentOS. RHEL/CentOS 6/7, which is maintained by a bunch of Linux experts
and has already proven itself the most rock-solid enterprise-class Linux distribution. StorLever also depends
on the packages/RPMs delivered by RHEL/CentOS, but user has the freedom to install only the packages they
actually required. 

Ajenti is another excellent project which is also developed in Python, and its purpose to provide a web control
panel for Linux on VPS and it's also extensible. It is a general control panel including some general utilities of 
Linux, but not focus on the storage management, and also does not provides software development API to other system

OpenLMI is a very similar project to StorLever, and it has been included in the RHEL 7, which also provides APIs for 
administrators to remotely manage, configure, monitor Linux system. But we don't think it's on the right way, 
OpenLMI is based on the technology so called "WBEM" to implement its scalability (extensibility). 
WBEM is a very complex technology architecture initiated by some big company like Microsoft、Compaq, Cisco at 1990s 
to support enterprise distributed computing environment. 
It is consist of many components and many protocol, flexible and considerate, but difficult to understand, 
difficult to deploy, difficult to develop. The network datagram is also difficult to read by human. 
We don't think we need such a complex architecture to implement remote management of Linux system. 
StorLever is simple framework to implement scalability, provides simple API, friendly web page. As to OpenLMI, 
StorLever is an alternative lightweight solution to implement the same function. 



Usage
====================

