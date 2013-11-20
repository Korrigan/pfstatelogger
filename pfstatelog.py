#!/usr/bin/env python

import sys
import pcapy
from datetime import datetime

from pfsync.packet import Reader

def recv_pkt(pcap_hdr, data):
    print "-- Received packet --"
    (ts, ms) = pcap_hdr.getts()
    print "%s.%d" % (str(datetime.fromtimestamp(ts)), ms)
    r = Reader(data)
    r.dump()
    print "-- END --\n\n"

def usage():
    print "Usage: pfstatelog.py <pfsync interface>"
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    r = pcapy.open_live(sys.argv[1], 1600, False, 100)
    r.loop(-1, recv_pkt)
    sys.exit(0)
