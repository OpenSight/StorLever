StorLever
===========

The primary goal of this project is ease the management of storage resources on server, 
by exposing a set of well-designed REST-styled web API, which may be consumed by central 
management system or other client who whish to monitor or manipulate those resources 
remotely.

StorLever delivers with a intuitive web based user interface based on those web API as well, 
which showcase the potential of those API.

Web API
-------

By "storage resources" we mean block devices, RAID, LVM, NFS, samba, iSCSI etc. All major 
Linux distributions, by default have a bunch of utilities to manipulate them, but all in 
different style, to master all those the command line and configuration file is not a trivial
task, and to access these utilities remotely and programmatically requires another set of skills,
which make things even worse.

So StorLever comes to the rescue. By providing a set of uniformed, well-designed web API, 
we abstract away all the configuration and command line details, with simplicity and consistency
in mind during API designing, people will find them easy to understand. 

All those API are HTTP based, which makes them totally platform and programming language independent.

Storage Resources
-----------------

