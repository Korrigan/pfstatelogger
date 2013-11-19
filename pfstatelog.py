#!/usr/bin/env python

import pcapy
from psync.headers import Header

def recv_pkt(hdr, data):
    print "> Received packet:"
    dir(hdr)
    print hdr.getts()
    print hdr.getcaplen()
    print hdr.getlen()
    print "-- DATA START --"
    (hdr, ndata) = Header.from_data(data)
    hdr.dump()
    print "--  DATA END  --"

if __name__ == '__main__':
    r = pcapy.open_live('en0', 1024, False, 100)
    r.loop(100, recv_pkt)
