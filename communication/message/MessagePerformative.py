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

    SEND_PERCEPTS_AND_DATA = 108 # send percepts
    SEND_ORDERS = 109 # send orders
    SEND_INFORMATION_CHIEF_DROP = 110 # send information from a chief to a chief that a transformed waste has been dropped
    SEND_TARGET_ORDERS = 111 # send orders to go to a target
    DISABLE_TARGET = 112 # send message to chief that the current target is now None
    SEND_ORDER_CANCEL_TARGET = 113 # send information from a chief to a chief to cancel target

    def __str__(self):
        """Returns the name of the enum item.
        """
        return '{0}'.format(self.name)
