PFStateLogger
=============

Abstract
--------

PFStateLogger is a Python program that logs all packetfilter state
changes. 

The purpose is to provide {sys,net}admin a way to identify connections
in case of an attack from one of his computer. While it can be easy
when NAT is not involved by looking at pflog with tcpump, these logs do
not provide any information about the private IP address used in the
connection if there is one.

Instead of a dirty script doing something like a `pfctl -sa` every
seconds and parsing the output (which was not a reliable nor effective
solution), I came up with this.


Usage
-----

This script relies on the pfsync interface, just create one if there is
none:

```console
ifconfig pfsync0 create
ifconfig pfsync0 up
```

Then lauch the script with that interface:

```console
./pfstatelog.py pfsync0
```

Note that the script will need the pcapy module installed, this can be
achieved easily with `pip install pcapy`. 

You may want to use supervisord to run the script in background, a
configuration sample is in `misc/pfstatelogger.supervisor.conf`. 

When the script is lauched, you should see logs appearing in your
log files (by default the script uses the LOG_DAEMON facility). 

You may also want to see logs on your console too:

```console
./pfstatelog.py -v pfsync0
```


How it works ?
--------------

Since Packetfilter does not provide a easy way to do what I wanted with
logs, I used the pfsync interface to get the info.

PFsync is the protocol used by CARP to share state table with other
PF instances which can be useful in case of loadbalancing. 

I reversed the OpenBSD's kernel source code dealing with pfsync and also
picked some info from tcpdump's code to deal with some of the packets
sent to pfsync interfaces. 

Since I have not that much spare time, my implementation might be
incomplete for your use, feel free to add more features (and open
pull requests if you want) to match your needs.

If you want to understand how it works in details, I recommend the
reading of the following files in OpenBSD sources:

- `sys/net/if_pfsync.h`
- `sys/net/if_pfsync.c`
- `sys/net/pfvar.h`
- `src/usr.sbin/tcpdump/print-pfsync.c`


Compatibility
-------------

This script works with the version 6 of PFsync (I haven't tested any
other). 

This script runs under OpenBSD 5.3 but should work on any other BSD
with Packetfilter and PFsyncV6 (not tested). 

I only tested this script with Python 2.7.


Tools used
----------

The script is wrote in Python. 

I used the [pcapy module](http://corelabs.coresecurity.com/index.php?module=Wiki&action=view&type=tool&name=Pcapy)
to deal with PCAP packets.


Licensing
---------

Since I spent a few hours reversing PF's kernel code and I wish no one
to do the same except if you're some kind of masochist person, I release
this source under the MIT licence (see `LICENSE` file).

