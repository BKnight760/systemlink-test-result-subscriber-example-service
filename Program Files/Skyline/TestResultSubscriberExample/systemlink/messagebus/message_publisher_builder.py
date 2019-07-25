# -*- coding: utf-8 -*-
"""
Implementation of 'MessagePublisherBuilder' class
"""
from __future__ import absolute_import


class MessagePublisherBuilder(object):
    """
    Message Publisher Builder.

    This is used for the construction of a
    :class:`systemlink.messagebus.message_publisher.MessagePublisher` object.
    """
    def __init__(self, origin=None):
        """
        :param origin: The ``Origin`` message property which is an
            identifier specifying where messages are sent from. Used
            for message routing. May be ``None``.
        :type origin: str or None
        """
        self._origin = origin
        self._reply_to = None
        self._connection_manager = None
        self._trace_logger = None

    @property
    def origin(self):
        """
        Get the ``Origin`` message property.

        :return: The ``Origin`` message property. May be ``None``.
        :rtype: str or None
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """
        Set the ``Origin`` message property.

        :param origin: The ``Origin`` message property. May be ``None``.
        :type origin: str or None
        """
        self._origin = origin

    @property
    def reply_to(self):
        """
        Get the ``ReplyTo`` message property.

        :return: The ``ReplyTo`` message property. May be ``None``.
        :rtype: str or None
        """
        return self._reply_to

    @reply_to.setter
    def reply_to(self, reply_to):
        """
        Set the ``ReplyTo`` message property.

        :param reply_to: The ``ReplyTo`` message property. May be ``None``.
        :type reply_to: str or None
        """
        self._reply_to = reply_to

    @property
    def connection_manager(self):
        """
        Get the Connection Manager. If this is ``None``, a new
        Connection Manager will be created during the creation
        of :class:`systemlink.messagebus.message_publisher.MessagePublisher`.

        :return: The Connection Manager. May be ``None``.
        :rtype: systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager
            or None
        """
        return self._connection_manager

    @connection_manager.setter
    def connection_manager(self, connection_manager):
        """
        Set the Connection Manager. If this is ``None``, a new
        Connection Manager will be created during the creation
        of :class:`systemlink.messagebus.message_publisher.MessagePublisher`.

        :param connection_manager: The Connection Manager. May be ``None``.
        :type connection_manager:
            systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager
            or None
        """
        self._connection_manager = connection_manager

    @property
    def trace_logger(self):
        """
        Get the Trace Logger.

        :return: The Trace Logger. May be ``None``.
        :rtype: systemlink.messagebus.trace_logger.TraceLogger or None
        """
        return self._trace_logger

    @trace_logger.setter
    def trace_logger(self, trace_logger):
        """
        Set the Trace Logger.

        :param trace_logger: The Trace Logger. May be ``None``.
        :type trace_logger: systemlink.messagebus.trace_logger.TraceLogger
            or None
        """
        self._trace_logger = trace_logger
