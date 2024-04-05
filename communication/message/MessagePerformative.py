#!/usr/bin/env python3

from enum import Enum


class MessagePerformative(Enum):
    """MessagePerformative enum class.
    Enumeration containing the possible message performative.
    """
    PROPOSE = 101 # init a protocole to propose to do something
    ACCEPT = 102 # confirm that the agent accepts the proposition
    COMMIT = 103 # inform the other agents of our actions
    ASK_WHY = 104 # ask an agent why he's doing something
    ARGUE = 105 # answer to ASK_WHY performative
    QUERY_REF = 106 # ask for value
    INFORM_REF = 107 # give the value

    def __str__(self):
        """Returns the name of the enum item.
        """
        return '{0}'.format(self.name)
