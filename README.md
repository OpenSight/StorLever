StorLever
===========

The primary goal of this project is ease the management of storage resources on server, 
by exposing a set of well-designed REST-styled web API, which may be consumed by central 
management system or other client who wish to monitor or manipulate those resources
remotely.

StorLever delivers with a intuitive web based user interface based on those web API as well, 
which showcases the potential of those API.

Highlights:

* well-designed REST API to manage disk, raid, NAS 
* based on enterprise class RHEL/CentOS 6
* user-friendly web user interface

Storage Resources
-----------------

By "storage resources" we mean block devices, RAID, LVM, NAS etc.
Following is a non-exhaustive list of what is under the control of this project:

* SCSI block device
* md raid
* LSI raid (LSISAS2108, LSISAS2008 chip)
* iSCSI initiator
* LVM
* XFS
* EXT4
* NFS
* SAMBA
* FTP

For the complete list of software packages involved, check out the dependency document.


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

There are already projects like openfiler and freeNAS which service the similar purpose, but what's
the difference?

Openfiler an freeNAS are both storage systems delivered with the whole operation system
and all the utilities sit on it, on the contrary, StorLever is only a set of API that helps the user
to ease the management of storage resources.

As to the OS part, StorLever is based on RHEL/CentOS 6, which is maintained by a bunch of Linux experts
and has already proven itself the most rock-solid enterprise-class Linux distribution. StorLever also depends
on the packages/RPMs delivered by RHEL/CentOS, but user has the freedom to install only the packages they
actually required.

At what makes StorLever unique is its REST based API, which makes remote and programmatic access so much easier
compare to other solution.



