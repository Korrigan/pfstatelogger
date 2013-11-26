#!/usr/bin/env python

import sys
import pcapy
from datetime import datetime

from pfsync.packet import Reader, StateManager

manager = StateManager()


def recv_pkt(pcap_hdr, data):
    (ts, ms) = pcap_hdr.getts()
    r = Reader(data)
    for a in r.actions:
        manager.handle_action(a)


def usage():
    print "Usage: pfstatelog.py <pfsync interface>"
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    r = pcapy.open_live(sys.argv[1], 1600, False, 100)
    r.loop(-1, recv_pkt)
    sys.exit(0)
