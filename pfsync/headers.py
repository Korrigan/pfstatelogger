from .mixins import UnpackableMixin

class Header(UnpackableMixin):
    """
    This class represents a pfsync header corresponding to the following
    C struct:

    struct pfsync_header {
    u_int8_t                        version;
    u_int8_t                        _pad;
    u_int16_t                       len; /* in bytes */
    u_int8_t                        pfcksum[PF_MD5_DIGEST_LENGTH];
    } __packed;

    See OpenBSD source sys/net/if_pfsync.h
    
    """
    unpack_format = '!bbh16s'

    def __init__(self, version, pad, len, checksum):
        self.version = version
        self.len = len
        self.checksum = checksum


    def dump(self):
        print "PFSYNC version: %d" % version
        print "PFSYNC packet length: %d" % len
        print "CHECKSUM: %s" % checksum


class SubHeader(UnpackableMixin):
    """
    This class represents a pfsync subheader corresponding to the
    following C struct:

    struct pfsync_subheader {
    u_int8_t                        action;
    u_int8_t                        len; /* in dwords */
    u_int16_t                       count;
    } __packed;

    See OpenBSD source sys/net/if_pfsync.h

    """
    unpack_format = '!bbh'

    def __init__(self, action_id, len, count):
        self.action_id = action_id
        self.len = len
        self.count = count
