from .headers import Header, SubHeader

class Reader(object):
    """
    This class parse a PFSYNC packet into header, subheaders and actions
    list

    """
    def __init__(self, data=None):
        self.actions = []
        if data:
            self.parse(data)

    def parse(self, data):
        """
        This method parse the packet

        """
        from .actions import build_from_header

        (self.header, data) = Header.from_data(data)
        while len(data) > SubHeader.get_cstruct_size():
            (shdr, data) = SubHeader.from_data(data)
            (action, data) = build_from_header(shdr, data)
            if action:
                self.actions.append(action)


    def dump(self):
        """Simple debug printing method"""
        self.header.dump()
        for a in self.actions:
            print "--"
            a.dump()
            print "--"
