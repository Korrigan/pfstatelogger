#!/usr/bin/env python

import sys
import pcapy
from datetime import datetime

from pfsync.packet import Reader

class StateManager(object):
    """
    This class is used to manage states
    It keep a state table in memory and log messages when needed

    """
    def __init__(self):
        self.states = []

    def add_state(self, state):
        """
        Add a state and log it
        Should implements a way to check if not already in list

        direction == 2 corresponds to the #define PF_OUT
        See OpenBSD sources sys/net/pfvar.h

        """
        if state.direction == 2:
            self.states.append(state)
            print "INS STATE: %s" % str(state)

    def del_state(self, state):
        """
        Delete state by id
        Works with pfsync messages del and del_c

        """
        for s in self.states[:]:
            if s.id == state.id:
                print "DEL STATE: %s" % str(s)
                self.states.remove(s)


manager = StateManager()


def recv_pkt(pcap_hdr, data):
    (ts, ms) = pcap_hdr.getts()
    r = Reader(data)
    for a in r.actions:
        f = None
        if a.is_add_action():
            f = manager.add_state
        elif a.is_del_action():
            f = manager.del_state
        if f:
            for m in a.messages:
                f(m)

#    print "-- Received packet --"
#    print "%s.%d" % (str(datetime.fromtimestamp(ts)), ms)
#    r.dump()
#    print "-- END --\n\n"

def usage():
    print "Usage: pfstatelog.py <pfsync interface>"
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    r = pcapy.open_live(sys.argv[1], 1600, False, 100)
    r.loop(-1, recv_pkt)
    sys.exit(0)
