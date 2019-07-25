# -*- coding: utf-8 -*-
"""
Implementation of 'ManagedServiceBuilder' and related classes
"""
from __future__ import absolute_import

# Import python libs
import logging

# Import local libs
from systemlink.messagebus.utils import is_linux

# Set up logging
LOGGER = logging.getLogger(__name__)


class ManagedServiceBuilder(object):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """
    Managed Service Builder.

    This is used for the construction of an object that inherits from
    :class:`systemlink.messagebus.managed_service_base.ManagedServiceBase`.
    """
    def __init__(self, service_name):
        """
        :param service_name: The name of the message service.
        :type service_name: str
        """
        LOGGER.debug('ManagedServiceBuilder constructor!')
        self._no_configuration_request = False
        self._no_work_subscriber = False
        # For standalone mode, on Windows, default to False. On Linux, default to True.
        self._standalone_property = is_linux()
        self._service_name = service_name
        self._instance_name = ''
        self._trace_logger = None
        self._durable_work_queue = False
        self._work_subscriber_builder = None
        self._instance_subscriber_builder = None
        self._log_to_trace_logger = False

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

    @property
    def no_configuration_request(self):
        # pylint: disable=line-too-long
        """
        Get whether or not a
        :class:`systemlink.messagebus.configuration_messages.ConfigurationGetSectionKeyValuesRequest`
        will be sent during initialization of a non-standalone service.

        :return: ``True`` if such a request will NOT be sent. ``False``
            if such a request will be sent.
        :rtype: bool
        """
        # pylint: enable=line-too-long
        return self._no_configuration_request

    @no_configuration_request.setter
    def no_configuration_request(self, no_configuration_request):
        # pylint: disable=line-too-long
        """
        Set whether or not a
        :class:`systemlink.messagebus.configuration_messages.ConfigurationGetSectionKeyValuesRequest`
        will be sent during initialization of a non-standalone service.

        :param no_configuration_request: ``True`` if such a request
             will NOT be sent. ``False`` if such a request will be
             sent.
        :type no_configuration_request: bool
        """
        # pylint: enable=line-too-long
        self._no_configuration_request = no_configuration_request

    @property
    def durable_work_queue(self):
        """
        Get whether the work queue is ``durable``. A ``durable`` queue
        can survive a broker restart, however, only ``persistent``
        messages will be recovered.

        :return: ``True`` if the work queue is ``durable``. ``False``
            otherwise.
        :rtype: bool
        """
        return self._durable_work_queue

    @durable_work_queue.setter
    def durable_work_queue(self, durable_work_queue):
        """
        Set whether the work queue is ``durable``. A ``durable`` queue
        can survive a broker restart, however, only ``persistent``
        messages will be recovered.

        :param durable_work_queue: ``True`` if the work queue is
            ``durable``. ``False`` otherwise.
        :type durable_work_queue: bool
        """
        self._durable_work_queue = durable_work_queue

    @property
    def work_subscriber_builder(self):
        """
        Get the builder for the work message subscriber.

        :return: A
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used in the construction of the work message
            subscriber. May be ``None`` if default behavior is desired.
        :rtype:
            systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder
        """
        return self._work_subscriber_builder

    @work_subscriber_builder.setter
    def work_subscriber_builder(self, work_subscriber_builder):
        """
        Set the builder for the work message subscriber.

        :param builder: A
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used in the construction of the work message
            subscriber. May be ``None`` if default behavior is desired.
        :type builder:
            systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder
        """
        self._work_subscriber_builder = work_subscriber_builder

    @property
    def instance_subscriber_builder(self):
        """
        Get the builder for the instance message subscriber.

        :return: A
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used in the construction of the instance message
            subscriber. May be ``None`` if default behavior is desired.
        :rtype:
            systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder
        """
        return self._instance_subscriber_builder

    @instance_subscriber_builder.setter
    def instance_subscriber_builder(self, instance_subscriber_builder):
        """
        Set the builder for the instance message subscriber.

        :param builder: A
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used in the construction of the instance message
            subscriber. May be ``None`` if default behavior is desired.
        :type builder:
            systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder
        """
        self._instance_subscriber_builder = instance_subscriber_builder

    @property
    def no_work_subscriber(self):
        """
        Get whether or not a message subscriber is used for work
        messages.

        :return: ``True`` if a message subscriber is NOT used for work
            messages. ``False`` if a message subscriber is used for work
            messages.
        :rtype: bool
        """
        return self._no_work_subscriber

    @no_work_subscriber.setter
    def no_work_subscriber(self, no_work_subscriber):
        """
        Set whether or not a message subscriber is used for work
        messages.

        :param no_work_subscriber: ``True`` if a message subscriber is
            NOT used for work messages. ``False`` if a message
            subscriber is used for work messages.
        :type no_work_subscriber: bool
        """
        self._no_work_subscriber = no_work_subscriber

    @property
    def standalone_property(self):
        """
        Get whether or not the service is ``standalone``. A
        ``standalone`` service does not integrate with the Service
        Manager, and hence does not register with the Service Manager
        nor can it be started or stopped from the Service Manager.

        :return: ``True`` if the service is ``standalone``. ``False``
            otherwise.
        :rtype: bool
        """
        return self._standalone_property

    @standalone_property.setter
    def standalone_property(self, standalone_property):
        """
        Set whether or not the service is ``standalone``. A
        ``standalone`` service does not integrate with the Service
        Manager, and hence does not register with the Service Manager
        nor can it be started or stopped from the Service Manager.

        :param standalone_property: ``True`` if the service is
            ``standalone``. ``False`` otherwise.
        :type standalone_property: bool
        """
        self._standalone_property = standalone_property

    @property
    def log_to_trace_logger(self):
        """
        Get whether the top-most
        :class:`systemlink.messagebus.trace_logger.TraceLogger` instance
        should automatically send Python logging to the Trace Logger
        service.

        :return: ``True`` if Python logging is automatically sent to
            the Trace Logger service. ``False`` otherwise.
        :rtype: bool
        """
        return self._log_to_trace_logger

    @log_to_trace_logger.setter
    def log_to_trace_logger(self, log_to_trace_logger):
        """
        Set whether the top-most
        :class:`systemlink.messagebus.trace_logger.TraceLogger` instance
        should automatically send Python logging to the Trace Logger
        service.

        :param log_to_trace_logger: ``True`` if Python logging is
            automatically sent to the Trace Logger service.
            ``False`` otherwise.
        :type log_to_trace_logger: bool
        """
        self._log_to_trace_logger = log_to_trace_logger
