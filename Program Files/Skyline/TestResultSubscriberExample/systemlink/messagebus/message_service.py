# -*- coding: utf-8 -*-
"""
Implementation of 'MessageService' and related classes
"""
from __future__ import absolute_import

# Import python libs
import logging
import sys
import uuid
# pylint: disable=import-error
if sys.version_info[0] < 3:
    from Queue import Queue
else:
    from queue import Queue
# pylint: enable=import-error

# Import local libs
# pylint: disable=wrong-import-position,import-error
from systemlink.messagebus.exceptions import SystemLinkException
from systemlink.messagebus.generic_message import GenericMessage
from systemlink.messagebus.generic_response import GenericResponse
from systemlink.messagebus.message_publisher import MessagePublisher
from systemlink.messagebus.message_publisher_builder import MessagePublisherBuilder
from systemlink.messagebus.message_service_builder import MessageServiceBuilder
from systemlink.messagebus.message_subscriber import MessageSubscriber, SynchCallbackInfo
from systemlink.messagebus.message_subscriber_builder import MessageSubscriberBuilder
from systemlink.messagebus.routed_message import RoutedMessage
# pylint: enable=wrong-import-position,import-error

# Set up logging
LOGGER = logging.getLogger(__name__)


class MessageService(object):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """
    This class oversees the overall usage of the message bus and is
    the top-level class used by Skyline-based clients and services.
    """
    def __init__(self, message_service_builder):
        """
        :param message_service_builder: A
            :class:`systemlink.messagebus.message_service_builder.MessageServiceBuilder`
            object used in the construction of this object.
        :type message_service_builder:
            systemlink.messagebus.message_service_builder.MessageServiceBuilder
        """
        LOGGER.debug('MessageService constructor!')
        self._closing = False
        self._subscriber = None
        self._trace_logger = None
        self._service_name = message_service_builder.service_name
        LOGGER.debug('service_name = %s', self._service_name)
        if not message_service_builder.instance_name:
            self._instance_name = self.get_unique_instance_name()
        else:
            self._instance_name = message_service_builder.instance_name

        LOGGER.debug('_instance_name = %s', self._instance_name)

        self._request_timeout = message_service_builder.request_timeout
        message_publisher_builder = MessagePublisherBuilder(self._service_name)
        message_publisher_builder.connection_manager = message_service_builder.connection_manager
        message_publisher_builder.reply_to = self.implicit_full_name

        LOGGER.debug('fullName = %s', self.implicit_full_name)

        self._publisher = MessagePublisher(message_publisher_builder)

        subscriber_builder = message_service_builder.subscriber_builder
        if subscriber_builder is None:
            subscriber_builder = MessageSubscriberBuilder(self.implicit_full_name)
            subscriber_builder.connection_manager = message_service_builder.connection_manager
            subscriber_builder.register_default_binding = True
            subscriber_builder.is_instance_subscriber = True

        self._subscriber = MessageSubscriber(subscriber_builder)

    @classmethod
    def from_service_name(cls, service_name):
        """
        Create an instance of :class:`MessageService` based on the
        service name.

        :param service_name: The name of the message service.
        :type service_name: str
        :return: An instance of :class:`MessageService`.
        :rtype: MessageService
        """
        message_service_builder = MessageServiceBuilder(service_name)
        return cls(message_service_builder)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        """
        Close this instance of :class:`MessageService`.
        """
        if self._closing:
            return
        self._closing = True
        # `self._subscriber` and `self._publisher` may be used as part
        # of a `AmqpConnectionManager` singleton and hence are shared.
        # Due to this, don't close them explicitly here. Instead, rely
        # on them to close themselves once their reference count
        # reaches zero.
        self._subscriber = None
        self._publisher = None

    @staticmethod
    def get_unique_instance_name():
        """
        Generate a unique instance name.

        :return: A unique instance name.
        :rtype: str
        """
        return str(uuid.uuid4())[:8]

    @property
    def implicit_full_name(self):
        """
        Get the full name of this instance of :class:`MessageService`
        which takes into consideration the service name and the
        instance name if it is set.

        :return: The full name.
        :rtype: str
        """
        return self.get_full_name(self._service_name, self._instance_name)

    @staticmethod
    def get_full_name(service_name, instance_name=None):
        """
        Get the full name based on service name and instance name if
        it exists.

        :param service_name: The name of the message service.
        :type service_name: str
        :param instance_name: The name of the message service instance.
            May be ``None`` if there is only one instance of the
            message service.
        :type instance_name: str or None
        :return: The full name.
        :rtype: str
        """
        if service_name is None:
            error_info = 'Service name cannot be none.'
            raise SystemLinkException.from_name('Skyline.Exception', info=error_info)
        if instance_name is None:
            return service_name
        return service_name + '_' + instance_name

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
        if self._trace_logger is None:
            error_info = 'InvalidOperationException: No TraceLogger set.'
            raise SystemLinkException.from_name('Skyline.Exception', info=error_info)
        return self._trace_logger

    @trace_logger.setter
    def trace_logger(self, trace_logger):
        """
        Set the Trace Logger.

        :param trace_logger: The Trace Logger.
        :type trace_logger: systemlink.messagebus.trace_logger.TraceLogger
        """
        self._trace_logger = trace_logger
        self._subscriber.trace_logger = trace_logger

    @property
    def request_timeout(self):
        """
        Get the request timeout (in seconds).

        :return: The request timeout (in seconds).
        :rtype: int or float
        """
        return self._request_timeout

    @request_timeout.setter
    def request_timeout(self, request_timeout):
        """
        Set the request timeout (in seconds).

        :param request_timeout: The request timeout (in seconds).
        :type request_timeout: int or float
        """
        self._request_timeout = request_timeout

    @property
    def publisher(self):
        """
        Get the message publisher.

        :return: The message publisher.
        :rtype: systemlink.messagebus.message_publisher.MessagePublisher
        """
        return self._publisher

    @property
    def subscriber(self):
        """
        Get the message subscriber.

        :return: The message subscriber.
        :rtype: systemlink.messagebus.message_subscriber.MessageSubscriber
        """
        return self._subscriber

    def publish_request(self, request_message):
        """
        Publish a request message.

        :param request_message: The request message.
        :type request_message:
            systemlink.messagebus.request_message.RequestMessage
        """
        self._publisher.publish_message_base(request_message)

    def publish_response(self, response_message):
        """
        Publish a response message.

        :param response_message: The response message.
        :type response_message:
            systemlink.messagebus.response_message.ResponseMessage
        """
        self._publisher.publish_message_base(response_message)

    def publish_routed_message(self, routed_message, ignore_response=True):
        """
        Publish a routed message.

        :param routed_message: The routed message.
        :type routed_message:
            systemlink.messagebus.routed_message.RoutedMessage
        :param ignore_response: The ``IgnoreResponse`` property in the
            message header.
        :type ignore_response: bool
        """
        routed_message.ignore_response = ignore_response
        self._publisher.publish_message_base(routed_message)

    def publish_broadcast(self, broadcast_message):
        """
        Publish a broadcast message.

        :param broadcast_message: The broadcast message.
        :type broadcast_message:
            systemlink.messagebus.broadcast_message.BroadcastMessage
        """
        self._publisher.publish_message_base(broadcast_message)

    def publish_generic_message(self, generic_message):
        """
        Publish a generic message.

        :param generic_message: The generic message.
        :type generic_message:
            systemlink.messagebus.generic_message.GenericMessage
        """
        self._publisher.publish_generic_message(generic_message)

    def publish_generic_request(self, generic_message):
        """
        Publish a generic message as a request.

        :param generic_message: The generic message.
        :type generic_message:
            systemlink.messagebus.generic_message.GenericMessage
        """
        self._publisher.publish_generic_message(generic_message)

    def publish_synchronous_message(self, message, mandatory=False, timeout_seconds=None):
        """
        Synchronously publish a message.

        :param message: The message object. The class of this object
            inherits from
            :class:`systemlink.messagebus.message_base.MessageBase`.
        :type message: systemlink.messagebus.message_base.MessageBase
        :param mandatory: The mandatory delivery notification flag.
        :type mandatory: bool
        :param timeout_seconds: The timeout in seconds for this query.
            If ``None``, will use the timeout specified by the
            :class:`systemlink.messagebus.message_service_builder.MessageServiceBuilder`
            object used to create this instance of
            :class:`MessageService`.
        :type timeout_seconds: int or float
        :return: The response message.
        :rtype: systemlink.messagebus.generic_message.GenericMessage
        """
        if timeout_seconds is None:
            timeout_seconds = self._request_timeout
        if issubclass(message.__class__, RoutedMessage):
            message.ignore_response = False
        return self._publish_synchronous_request(message, timeout_seconds, mandatory)

    def publish_generic_response(self, request, error=None):
        """
        Publish a generic response.

        :param request: The request message that is being responded to.
        :type request:
            systemlink.messagebus.routed_message.RoutedMessage
        """
        self._publish_generic_response(request, error)

    def register_callback(self, message_class_type, callback, message_name=None):
        """
        Register a callback that will be invoked when a
        specified message class type is used.

        :param message_class_type: The type of the message class to as the
            trigger for the callback.
        :type message_class_type: type
        :param callback: The callback to invoke. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        :param message_name: The message name to use. If ``None``, will
            use the name associated with ``message_class_type``.
        :type message_name: str or None
        """
        self._subscriber.register_callback(
            message_class_type, callback, message_name=message_name
        )

    def unregister_callback(self, message_class_type, message_name=None):
        """
        Unregister a callback that would have been invoked when a
        specified message class type is used.

        :param message_class_type: The name of the message to use as the
            trigger for the callback.
        :type message_class_type: type
        :param message_name: The message name to use. If ``None``, will
            use the name associated with ``message_class_type``.
        :type message_name: str or None
        """
        self._subscriber.unregister_callback(
            message_class_type, message_name=message_name
        )

    def _publish_synchronous_request(self, request, timeout_seconds, mandatory=False):
        """
        Synchronously publish a request.

        :param request: The message object. The class of this object
            inherits from
            :class:`systemlink.messagebus.message_base.MessageBase` or is
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type request: systemlink.messagebus.message_base.MessageBase
            or systemlink.messagebus.generic_message.GenericMessage
        :param timeout_seconds: The timeout in seconds for this query.
        :type timeout_seconds: int or float
        :param mandatory: The mandatory delivery notification flag.
        :type mandatory: bool
        :return: The response message.
        :rtype: systemlink.messagebus.generic_message.GenericMessage
        """
        queue = Queue()
        info = SynchCallbackInfo()
        info.queue = queue

        self._subscriber._sync_callbacks[request.correlation_id] = info  # pylint: disable=protected-access

        try:
            if issubclass(request.__class__, GenericMessage):
                self._publisher.publish_generic_message(request, mandatory)
            else:
                self._publisher.publish_message_base(request, mandatory)

            generic_message = self._subscriber.wait_for_message(queue, True, timeout_seconds)
        finally:
            self._subscriber._sync_callbacks.pop(request.correlation_id, None)  # pylint: disable=protected-access

        if generic_message is None:
            msg = 'Service did not respond | ' + request.routing_key
            LOGGER.error(msg)
            if self._trace_logger is not None:
                self._trace_logger.log_error(msg, skip_if_has_log_handler=True)
        return generic_message

    def _publish_generic_response(self, request, error):
        """
        Publish a generic response.

        :param request: The request message that is being responded to.
        :type request:
            systemlink.messagebus.routed_message.RoutedMessage
        """
        has_error = error is not None and error.has_value()
        if not request.ignore_response:
            if not has_error:
                generic_response = GenericResponse.from_routing_source(request)
                self.publish_generic_response(generic_response)
            else:
                generic_response = GenericResponse.from_routing_source(request, error)
                self.publish_generic_response(generic_response)
        elif has_error:
            msg = (
                'Routed Message had error but response was ignored | ' +
                request.message_name +
                ' from ' +
                request.origin +
                ' | Error: ' +
                str(error)
            )
            LOGGER.error(msg)
            if self._trace_logger is not None:
                self._trace_logger.log_error(msg, skip_if_has_log_handler=True)
