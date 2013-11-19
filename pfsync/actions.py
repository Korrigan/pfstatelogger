from .mixins import UnpackableMixin

class BaseAction(object):
    """
    This class represents a base for a pfsync action

    """

    def __init__(self, hdr, type=None, data=""):
        self.hdr = hdr
        self.type = type
        self.data = data



def build_from_header(hdr, data):
    """
    This method returns an instance of the class corresponding to the
    action type supplied in the header
    hdr is of type pfsync.headers.SubHeader

    """
    actions = [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ]

    if hdr.action_id > 0 and hdr.action_id < len(actions):
        return actions[hdr.action_id].from_data(data, hdr)
    return None
