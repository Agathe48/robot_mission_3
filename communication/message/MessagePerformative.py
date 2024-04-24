#!/usr/bin/env python3

from enum import Enum


class MessagePerformative(Enum):
    """MessagePerformative enum class.
    Enumeration containing the possible message performative.
    """
    ### Messages from agent to chief ###

    SEND_PERCEPTS_AND_DATA = 101 # send percepts
    DISABLE_TARGET = 104 # send message to chief that the current target is now None

    ### Messages from chief to agent ###

    SEND_ORDERS = 102 # send orders
    SEND_ORDER_CANCEL_TARGET = 105 # send the order to cancel the target position of an agent
    SEND_ORDER_STOP_ACTING = 106 # send the order to stop acting (at the end of the cleaning)
    
    ### Messages from chief to chief

    SEND_INFORMATION_CHIEF_DROP = 103 # send information from a chief to a chief that a transformed waste has been dropped
    SEND_INFORMATION_CHIEF_PREVIOUS_ZONE_CLEANED = 107 # send information from a chief to a chief that the previous zone is cleaned

    def __str__(self):
        """Returns the name of the enum item.
        """
        return '{0}'.format(self.name)
