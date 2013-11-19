from .headers import Header, SubHeader

class Reader(object):
    """
    This class parse a PFSYNC packet into header, subheader and actions
    list

    """
    def __init__(self, data=None):
        if data:
            self.parse(data)

    def parse(self, data):
        """
        This method parse the packet

        """
        (self.header, data) = Header.from_data(data)


    def dump(self):
        """
        A simple debug printing method

        """
        print self.header.dump()
