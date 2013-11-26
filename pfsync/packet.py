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
        while len(data) >= SubHeader.get_cstruct_size():
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


class StateManager(object):
    """
    This class is used to manage states
    It keep a state table in memory and log messages when needed

    """

    def __init__(self):
        self.states = []
        self.handles = [
            self._clr_states,
            None,
            None,
            None,
            None,
            None,
            self._del_state,
            self._del_state,
            None,
            None,
            None,
            None,
            None,
            self._add_state,
            None,
            None,
            ]

    def handle_action(self, action):
        """
        Handle an action class and update the state table in this way
        This method call the right internal method for each message of
        the action class.

        """
        id = action.header.action_id
        if id >= 0 and id < len(self.handles) and self.handles[id]:
            for m in action.messages:
                return self.handles[id](m)

    def _clr_states(self, msg):
        """
        Clear all states on a specified interface by a specific creator
        Handles pfsync message clr

        """
        print "CLR STATES: %s" % str(msg)

    def _add_state(self, state):
        """
        Add a state and log it
        Should implements a way to check if not already in list

        direction == 2 corresponds to the #define PF_OUT
        See OpenBSD sources sys/net/pfvar.h

        """
        if state.direction == 2:
            print "INS STATE: %s" % str(state)

    def _del_state(self, state):
        """
        Delete state by id
        Works with pfsync messages del and del_c

        """
        print "DEL STATE: %s" % str(state)

