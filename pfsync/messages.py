from .mixins import UnpackableMixin

class PFStateKey(UnpackableMixin):
    """
    A class corresponding to the following C struct:
    struct pfsync_state_key {
    struct pf_addr   addr[2];
    u_int16_t        port[2];
    u_int16_t        rdomain;
    sa_family_t      af;
    u_int8_t         pad;
    };

    See OpenBSD sources sys/net/pfvar.h

    """
    unpack_format = '16s16s 2HHBB'

    def __init__(self,
                 addr1, addr2,
                 port1, port2,
                 rdomain,
                 address_family,
                 pad):
        self.addr = (addr1, addr2)
        self.port = (port1, port2)
        self.address_family = address_family


    def dump(self):
        import socket

        print "ADDR1: %s:%d" % (socket.inet_ntoa(self.addr[0][:4]), self.port[0])
        print "ADDR2: %s:%d" % (socket.inet_ntoa(self.addr[1][:4]), self.port[1])
                                

class MessageState(UnpackableMixin):
    """
    A class corresponding to the following C struct:
    struct pfsync_state {
    u_int64_t        id;
    char             ifname[IFNAMSIZ];
    struct pfsync_state_key key[2];
    struct pfsync_state_peer src;
    struct pfsync_state_peer dst;
    struct pf_addr   rt_addr;
    u_int32_t        rule;
    u_int32_t        anchor;
    u_int32_t        nat_rule;
    u_int32_t        creation;
    u_int32_t        expire;
    u_int32_t        packets[2][2];
    u_int32_t        bytes[2][2];
    u_int32_t        creatorid;
    int32_t          rtableid[2];
    u_int16_t        max_mss;
    sa_family_t      af;
    u_int8_t         proto;
    u_int8_t         direction;
    u_int8_t         log;
    u_int8_t         pad0;
    u_int8_t         timeout;
    u_int8_t         sync_flags;
    u_int8_t         updates;
    u_int8_t         min_ttl;
    u_int8_t         set_tos;
    u_int16_t        state_flags;
    u_int8_t         pad[2];
    } __packed;

    See OpenBSD sources sys/net/if_pfsync.h

    """
    @classmethod
    def get_unpack_format(cls):
        """
        Brace yourselves, long dirty string is coming.

        Unpacking of structs is done as a string with the size of the
        struct and will be unpacked again in __init__

        Tabs are replaced with their size * their type (ex: int a[2] ->
        'ii') and will be repacked in tuples in __init__
        This does not stand for ifname

        The pf_addr struct (which is in fact an union containing the
        128bits ip address) is extracted as 4 32 bits unsigned int which
        will be our preferred form

        """
        from struct import calcsize

        unpack_format = '!Q 16s'
        unpack_format += '%(state_key_size)ds%(state_key_size)ds' % {
            'state_key_size': PFStateKey.get_cstruct_size(),
            }
        unpack_format += '%(state_peer_size)ds%(state_peer_size)ds' % {
            'state_peer_size': calcsize('%dsIIIHHBB6B' % calcsize('HBBI')), # to fix
            }
        unpack_format += '4I IIIII 4I 4I I 2i HBBBBBBBBBBH 2B'
        return unpack_format

    def __init__(self, id, ifname,
                 key1, key2,
                 src, dst,
                 rt_addr1, rt_addr2, rt_addr3, rt_addr4,
                 rule, anchor, nat_rule,
                 creation, expire,
                 packets1, packets2, packets3, packets4,
                 bytes1, bytes2, bytes3, bytes4,
                 creator_id,
                 rtable_id1, rtable_id2,
                 max_mss,
                 addess_family,
                 protocol,
                 direction,
                 log,
                 pad0,
                 timeout,
                 sync_flags,
                 updates,
                 min_ttl,
                 set_tos,
                 state_flags,
                 pad1, pad2):
        self.rt_addr = (rt_addr1, rt_addr2, rt_addr3, rt_addr4)
        self.key = (PFStateKey.from_data(key1)[0],
                    PFStateKey.from_data(key2)[0])
        self.src = src # To unpack
        self.dst = dst # To unpack
        self.packets = ((packets1, packets2), (packets3, packets4))
        self.bytes = ((bytes1, bytes2), (bytes3, bytes4))
        self.protocol = protocol
        self.direction = direction
        self.timeout = timeout

    def dump(self):
        """Simple debug printing method"""
        if self.direction != 2:
            print "OSEF"
            return
        print "PROTOCOL: %d" % self.protocol
        print "DIRECTION: %d" % self.direction
        print "TIMEOUT: %d" % self.timeout
        print "RT_ADDR: %d.%d.%d.%d" % self.rt_addr
        self.key[0].dump()
        self.key[1].dump()
