#!/usr/bin/env python

import pcapy
from pfsync.packet import Reader

def recv_pkt(pcap_hdr, data):
    print "-- Received packet --"
    (ts, ms) = pcap_hdr.getts()
    print "%s.%d" % (str(datetime.from_timestamp(ts)), ms)
    r = Reader(data)
    r.dump()
    print "-- END --\n\n"

if __name__ == '__main__':
    r = pcapy.open_live('en0', 1600, False, 100)
    r.loop(-1, recv_pkt)
