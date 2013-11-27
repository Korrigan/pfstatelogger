from .headers import Header, SubHeader

class Reader(object):
    """
    This class parse a PFSYNC packet into header, subheaders and actions
    list
    It only deals with pfsync version 6

    """
    PFSYNC_VERSION = 6

    def __init__(self, data=None, logger=None):
        import logging

        self.actions = []
        if data:
            self.parse(data)
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)

    def parse(self, data):
        """
        This method parse the packet and create needed action and message classes
        It may fails if packet are a bad version

        """
        from .actions import build_from_header

        (self.header, data) = Header.from_data(data)
        if not self.header.version == self.PFSYNC_VERSION:
            self.logger.warning("dealing with bad pfsync version (%d)" % self.header.version)
        while len(data) >= SubHeader.get_cstruct_size():
            (shdr, data) = SubHeader.from_data(data)
            (action, data) = build_from_header(shdr, data)
            if action:
                self.actions.append(action)
        if len(data) > 0:
            self.logger.warning("there is still data to process")


class StateManager(object):
    """
    This class is used to manage PF states.
    It handle all pfsync actions (when parsed into the correct action
    classes) and log the needed things.

    This is the class that you should extends or replace if you need
    more of pfstatelogger.py

    """

    def __init__(self, logger=None):
        import logging

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
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
        

    def handle_action(self, action, date):
        """
        This method call the right internal method for each message of
        the action class.
        The self.handles array is built according to PFSYNC_ACTIONS
        defines.

        See also .actions.build_from_header

        """
        id = action.header.action_id
        if id >= 0 and id < len(self.handles) and self.handles[id]:
            for m in action.messages:
                return self.handles[id](m, date)

    def _clr_states(self, msg, date):
        """
        Clear all states on a specified interface by a specific creator
        Handles pfsync message clr

        """
        self.logger.info("[%s] CLR STATES: %s" % (date, str(msg)))

    def _add_state(self, state, date):
        """
        Add a state and log it
        Should implements a way to check if not already in list

        direction == 2 corresponds to the #define PF_OUT
        See OpenBSD sources sys/net/pfvar.h

        """
        if state.direction == 2:
            self.logger.info("[%s] INS STATE: %s" % (date, str(state)))

    def _del_state(self, state, date):
        """
        Delete state by id
        Works with pfsync messages del and del_c

        """
        self.logger.info("[%s] DEL STATE: %s" % (date, str(state)))

