# -*- coding: utf-8 -*-
"""
Implementation of 'MessageServiceBuilder' class
"""
from __future__ import absolute_import

# Import local libs
# pylint: disable=wrong-import-position,import-error
from systemlink.messagebus.exceptions import SystemLinkException
# pylint: enable=wrong-import-position,import-error

DEFAULT_REQUEST_TIMEOUT = 10


class MessageServiceBuilder(object):
    """
    Message Service Builder.

    This is used for the construction of a
    :class:`systemlink.messagebus.message_service.MessageService` object.
    """
    def __init__(self, service_name=None):
        """
        :param service_name: The name of the message service.
        :type service_name: str
        """
        self._instance_name = None
        if service_name is None:
            error_info = 'Service name cannot be none.'
            raise SystemLinkException.from_name('Skyline.Exception', info=error_info)
        self._service_name = service_name
        self._request_timeout = DEFAULT_REQUEST_TIMEOUT
        self._connection_manager = None
        self._subscriber_builder = None
        self._trace_logger = None

    @property
    def service_name(self):
        """
        Get the service name.

        :return: The service name.
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """
        Set the service name.

        :param service_name: The service name.
        :type service_name: str
        """
        self._service_name = service_name

    @property
    def instance_name(self):
        """
        Get the instance name.

        :return: The instance name. May be ``None``.
        :rtype: str or None
        """
        return self._instance_name

    @instance_name.setter
    def instance_name(self, instance_name):
        """
        Set the instance name.

        :param instance_name: The instance name. May be ``None``.
        :type instance_name: str or None
        """
        self._instance_name = instance_name

    @property
    def trace_logger(self):
        """
        Get the Trace Logger.

        :return: The Trace Logger.
        :rtype: systemlink.messagebus.trace_logger.TraceLogger
        """
        return self._trace_logger

    @trace_logger.setter
    def trace_logger(self, trace_logger):
        """
        Set the Trace Logger.

        :param trace_logger: The Trace Logger.
        :type trace_logger: systemlink.messagebus.trace_logger.TraceLogger
        """
        self._trace_logger = trace_logger

    @property
    def request_timeout(self):
        """
        Get the request timeout (in seconds).

        :return: The request timeout (in seconds).
        :rtype: int or float
        """
        return self._request_timeout

    @request_timeout.setter
    def request_timeout(self, timeout_seconds):
        """
        Set the request timeout (in seconds).

        :param timeout_seconds: The request timeout (in seconds).
        :type timeout_seconds: int or float
        """
        self._request_timeout = timeout_seconds

    @property
    def connection_manager(self):
        """
        Get the Connection Manager. If this is ``None``, a new
        Connection Manager will be created during the creation
        of :class:`systemlink.messagebus.message_service.MessageService`.

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
        of :class:`systemlink.messagebus.message_service.MessageService`.

        :param connection_manager: The Connection Manager. May be ``None``.
        :type connection_manager:
            systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager
            or None
        """
        self._connection_manager = connection_manager

    @property
    def subscriber_builder(self):
        """
        Get the Message Subscriber Builder. If this is ``None``, a new
        Message Subscriber Builder will be created during the creation
        of :class:`systemlink.messagebus.message_service.MessageService`.

        :return: The Message Subscriber Builder. May be ``None``.
        :rtype: systemlink.messagebus.message_subscriber_builder.MessageSubscriberBuilder
            or None
        """
        return self._subscriber_builder

    @subscriber_builder.setter
    def subscriber_builder(self, subscriber_builder):
        """
        Set the Message Subscriber Builder. If this is ``None``, a new
        Message Subscriber Builder will be created during the creation
        of :class:`systemlink.messagebus.message_service.MessageService`.

        :param subscriber_builder: The Message Subscriber Builder. May
            be ``None``.
        :type subscriber_builder:
            systemlink.messagebus.message_subscriber_builder.MessageSubscriberBuilder
            or None
        """
        self._subscriber_builder = subscriber_builder
