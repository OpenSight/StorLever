storlever_megaraid
===========

This project is an extension of storlever, which provide supports for Megaraid RAID controller from
LSI Corp. (www.lsi.com). Megaraid controller is the mainstream HW raid controller for X86 Server
market, which highlights low cost RAID solution.

storlever_megaraid makes use of the MegaCli tools, which is from LSI, to manage the low-level
megaraid driver in kernel so that it can Create/Remove/Update/Browse the logical disk ( raid disk)
which is output by megaraid driver.

The other purpose of storlever_megaraid is to provide a example to show how to write a extension (plugin)
for storlever. Storlever makes use of setuptools entry-points mechanism to implement extensibility so
that the third part can add new features to storlever by writing their own extension. The extension developer can take
storlever_megaraid as skeleton, and begins from it.

Highlights:

* Provide support for the popular low-cost Megaraid controller for HW RAID
* Example for writing a extension for storlever

Quickly Usage
-----------------

Add storlever_megaraid to storlever is very simple, following the steps below:

1.  Install storlever following the storlever's readme
2.  Install storlever_megaraid. storlever_megaraid is a pure python project which is very easy to installed.
    Just type the following CMD in the storlever_megaraid's project's directory:


        python setup.py install



3.  Enjoy the new feature in storlever!!




