#!/usr/bin/env python3
from communication.message.MessagePerformative import MessagePerformative

class MessageService:
    """MessageService class.
    Class implementing the message service used to dispatch messages between communicating agents.

    Not intended to be created more than once: it's a singleton.

    attr:
        scheduler: the scheduler of the sma (Scheduler)
        messages_to_proceed: the list of message to proceed mailbox of the agent (list)
    """

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method.
        """
        return MessageService.__instance

    def __init__(self, scheduler, instant_delivery=True):
        """ Create a new MessageService object.
        """
        MessageService.__instance = self
        self.__scheduler = scheduler
        self.__instant_delivery = instant_delivery
        self.__messages_to_proceed = []
        self.nb_messages_chief_to_agent = 0
        self.nb_messages_agent_to_chief = 0
        self.nb_messages_chief_to_chief = 0

    def set_instant_delivery(self, instant_delivery):
        """ Set the instant delivery parameter.
        """
        self.__instant_delivery = instant_delivery

    def send_message(self, message):
        """ Dispatch message if instant delivery active, otherwise add the message to proceed list.
        """
        if message.get_performative() in [
            MessagePerformative.SEND_ORDERS,
            MessagePerformative.SEND_ORDER_STOP_ACTING,
            MessagePerformative.SEND_ORDER_CANCEL_TARGET]:
            self.nb_messages_chief_to_agent += 1
        elif message.get_performative() in [
            MessagePerformative.SEND_PERCEPTS_AND_DATA,
            MessagePerformative.DISABLE_TARGET]:
            self.nb_messages_agent_to_chief += 1
        elif message.get_performative() in [
            MessagePerformative.SEND_INFORMATION_CHIEF_DROP,
            MessagePerformative.SEND_INFORMATION_CHIEF_PREVIOUS_ZONE_CLEANED
        ]:
            self.nb_messages_chief_to_chief += 1
        
        if self.__instant_delivery:
            self.dispatch_message(message)
        else:
            self.__messages_to_proceed.append(message)

    def dispatch_message(self, message):
        """ Dispatch the message to the right agent.
        """
        self.find_agent_from_name(message.get_dest()).receive_message(message)

    def dispatch_messages(self):
        """ Proceed each message received by the message service.
        """
        if len(self.__messages_to_proceed) > 0:
            for message in self.__messages_to_proceed:
                self.dispatch_message(message)

        self.__messages_to_proceed.clear()

    def find_agent_from_name(self, agent_name):
        """ Return the agent according to the agent name given.
        """
        for agent in self.__scheduler.get_communicating_agents():
            if agent.get_name() == agent_name:
                return agent
