#!/usr/bin/env python

import sys
import logging
from logging.handlers import SysLogHandler

import pcapy

from pfsync.packet import Reader, StateManager


prog_short_name = "pfstatelog.py"
usage_string = "Usage: %(name)s [-vd] <pfsync interface>" % {'name': prog_short_name}

log_syslog_device = '/dev/log'
log_syslog_facility = SysLogHandler.LOG_DAEMON
# log_handlers is a list of 3 tuples composed of (handler, level, format)
# level or format may be None in which case it will be overwritten by
# the defaults log_level and log_format respectively
log_handlers = [
    (SysLogHandler(address=log_syslog_device, facility=log_syslog_facility), None, None),
    ]
log_level = level=logging.INFO
log_format = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
logger = logging.getLogger(prog_short_name)

manager = StateManager(logger=logger)


def recv_pkt(pcap_hdr, data):
    """
    This function is more or less the entry point
    It get a PCAP header and some data and dispatch it to correct
    extracting and handling classes

    """
    from datetime import datetime

    (ts, ms) = pcap_hdr.getts()
    date = "%s,%6d" % (str(datetime.fromtimestamp(ts)), ms)
    r = Reader(data, logger=logger)
    for a in r.actions:
        manager.handle_action(a, date)


def usage():
    """Print the usage and exits with a erorr code of 1"""
    print >> sys.stderr, usage_string
    sys.exit(1)


def help():
    """Print the help text and exits with error code 0"""
    print usage_string
    print ""
    print "\t-h: Print out this help message"
    print "\t-v: Enable verbose mode, log output will also be printed on console"
    print "\t-d: Enable debug mode, debug messages will be logged"
    sys.exit(0)


def setup_logger():
    """
    This function setup the logger configuration using global variables:
     - log_handlers: a list of handlers to attach
     - log_level: the log level to user
     - log_format: the output format
     - logger: the logger class

    """
    logger.setLevel(log_level)
    for h, l, f in log_handlers:
        if not l:
            l = log_level
        if not f:
            f = log_format
        h.setLevel(l)
        h.setFormatter(f)
        logger.addHandler(h)


def get_args(argv):
    """
    This function parses the command line arguments and set the correct
    options according to these values

    It the returns the remaining arguments

    """
    import getopt

    try:
        opts, args = getopt.getopt(argv, "vhd")
    except getopt.GetoptError as e:
        print >> sys.stderr, str(e)
        usage()
    for o, v in opts:
        if o == '-h':
            help()
        elif o == '-v':
            log_handlers.append((logging.StreamHandler(stream=sys.stdout), None, None))
        elif o == '-d':
            log_level = logging.DEBUG
    return args


if __name__ == '__main__':
    argv = get_args(sys.argv[1:])
    if not len(argv):
        usage()
    setup_logger()
    iface = argv[0]
    r = pcapy.open_live(iface, 1600, False, 100)
    # DLT_PFSYNC == 18
    # See OpenBSD sources sys/net/bpf.h
    if not r.datalink() == 18:
        print >> sys.stderr, "Interface %s is not a pfsync interface" % iface
        sys.exit(1)
    r.loop(-1, recv_pkt)
    sys.exit(0)
