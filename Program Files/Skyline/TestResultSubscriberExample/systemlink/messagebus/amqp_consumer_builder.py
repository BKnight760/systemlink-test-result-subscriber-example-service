# -*- coding: utf-8 -*-
"""
Implementation of 'AmqpConsumerBuilder' class
"""
from __future__ import absolute_import

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.message_header import ROUTING_KEY_PREFIX
# pylint: enable=import-error


class AmqpConsumerBuilder(object):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """
    AMQP Consumer Builder.

    This is required for the construction of a
    :class:`systemlink.messagebus.amqp_consumer.AmqpConsumer` object.
    """
    def __init__(self, queue_name, callback):
        """
        :param queue_name: The queue name.
        :type queue_name: str
        :param callback: The callback for when handling messages. This
            is an instance of
            :class:`systemlink.messagebus.message_subscriber.MessageSubscriberReceiveCallback`.
        :type callback: systemlink.messagebus.message_subscriber.MessageSubscriberReceiveCallback
        """
        self._queue_name = queue_name
        self._callback = callback
        self._message_returned_callback = None
        self._routing_key_prefix = ROUTING_KEY_PREFIX
        self._event_args_callback = None
        self._prefetch_queue_depth = 100
        self._connection_manager = None
        self._trace_logger = None
        self._durable_queue = None
        self._explicit_ack = None
        self._auto_reconnect = True

    @property
    def queue_name(self):
        """
        Get the queue name.

        :return: The queue name.
        :rtype: str
        """
        return self._queue_name

    @queue_name.setter
    def queue_name(self, queue_name):
        """
        Set the queue name.

        :param queue_name: The queue name.
        :type queue_name: str
        """
        self._queue_name = queue_name

    @property
    def routing_key_prefix(self):
        """
        Get the routing key prefix.

        :return: The routing key prefix.
        :rtype: str
        """
        return self._routing_key_prefix

    @routing_key_prefix.setter
    def routing_key_prefix(self, routing_key_prefix):
        """
        Set the routing key prefix.

        :param routing_key_prefix: The routing key prefix.
        :type routing_key_prefix: str
        """
        self._routing_key_prefix = routing_key_prefix

    @property
    def callback(self):
        """
        Get the callback for handling messages.

        :return: The callback for handling messages. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :rtype: callable
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        """
        Set the callback for handling messages.

        :param callback: The callback for handling messages. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        """
        self._callback = callback

    @property
    def message_returned_callback(self):
        """
        Get the callback for handling the case when a mandatory message
        was returned.

        :return: The callback for this case. This
            is a callable object or function that takes two arguments:
                correlation_id: str
                message_type: str
        :rtype: callable
        """
        return self._message_returned_callback

    @message_returned_callback.setter
    def message_returned_callback(self, message_returned_callback):
        """
        Set the callback for handling the case when a mandatory message
        was returned.

        :param message_returned_callback: The callback for this case. This
            is a callable object or function that takes two arguments:
                correlation_id: str
                message_type: str
        :type message_returned_callback: callable
        """
        self._message_returned_callback = message_returned_callback

    @property
    def event_args_callback(self):
        """
        Get the callback for handling messages at a low level. If this is
        set, it will take precedence over the callback from ``callback``
        and that callback will not be used.

        :return: The callback for handling messages at a low level. This
            is a callable object or function that takes one argument
            that is a 3-tuple with types:
                :class:`pika.spec.Basic.Deliver`,
                :class:`pika.spec.BasicProperties`, and
                :class:`bytes` (for the message body).
        :rtype: callable
        """
        return self._event_args_callback

    @event_args_callback.setter
    def event_args_callback(self, event_args_callback):
        """
        Get the callback for handling messages at a low level. If this is
        set, it will take precedence over the callback from ``callback``
        and that callback will not be used.

        :param event_args_callback: The callback for handling messages at
            a low level. This is a callable object or function that takes
            one argument that is a 3-tuple with types:
                :class:`pika.spec.Basic.Deliver`,
                :class:`pika.spec.BasicProperties`, and
                :class:`bytes` (for the message body).
        :type event_args_callback: callable
        """
        self._event_args_callback = event_args_callback

    @property
    def connection_manager(self):
        """
        Get the connection manager.

        :return: A
            :class:`systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager`
            object.
        :rtype: systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager
        """
        return self._connection_manager

    @connection_manager.setter
    def connection_manager(self, connection_manager):
        """
        Set the connection manager.

        :param connection_manager: A
            :class:`systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager`
            object.
        :type connection_manager:
            systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager
        """
        self._connection_manager = connection_manager

    @property
    def trace_logger(self):
        """
        Get the Trace Logger.

        :return: A :class:`systemlink.messagebus.trace_logger.TraceLogger`
            object.
        :rtype: systemlink.messagebus.trace_logger.TraceLogger
        """
        return self._trace_logger

    @trace_logger.setter
    def trace_logger(self, trace_logger):
        """
        Get the Trace Logger.

        :param trace_logger: A :class:`systemlink.messagebus.trace_logger.TraceLogger`
            object.
        :type trace_logger: systemlink.messagebus.trace_logger.TraceLogger
        """
        self._trace_logger = trace_logger

    @property
    def durable_queue(self):
        """
        Get whether the queue is durable (backed by persistent storage).

        :return: ``True`` if the queue is durable. ``False`` otherwise.
        :rtype: bool
        """
        return self._durable_queue

    @durable_queue.setter
    def durable_queue(self, durable_queue):
        """
        Set whether the queue is durable (backed by persistent storage).

        :param durable_queue: ``True`` if the queue is durable. ``False`` otherwise.
        :type durable_queue: bool
        """
        self._durable_queue = durable_queue

    @property
    def explicit_ack(self):
        """
        Get explicit acknowledge (not using auto-acknowledge).

        :return: ``True if explicit acknowledge is enabled. ``False`` otherwise.
        :rtype: bool
        """
        return self._explicit_ack

    @explicit_ack.setter
    def explicit_ack(self, explicit_ack):
        """
        Set explicit acknowledge (not using auto-acknowledge).

        :param explicit_ack: ``True if explicit acknowledge is enabled. ``False`` otherwise.
        :type explicit_ack: bool
        """
        self._explicit_ack = explicit_ack

    @property
    def prefetch_queue_depth(self):
        """
        Get the prefetch queue depth.

        :return: The prefetch queue depth.
        :rtype: int
        """
        return self._prefetch_queue_depth

    @prefetch_queue_depth.setter
    def prefetch_queue_depth(self, prefetch_queue_depth):
        """
        Set the prefetch queue depth.

        :param prefetch_queue_depth: The prefetch queue depth.
        :type prefetch_queue_depth: int
        """
        self._prefetch_queue_depth = prefetch_queue_depth

    @property
    def auto_reconnect(self):
        """
        Get auto-reconnect.

        :return: Returns ``True`` when it will attempt to reconnect the AMQP
            connection when a disconnect is detected. Returns ``False``
            otherwise.
        :rtype: bool
        """
        return self._auto_reconnect

    @auto_reconnect.setter
    def auto_reconnect(self, auto_reconnect):
        """
        Set auto-reconnect.

        :param auto_reconnect: If ``True``, will attempt to reconnect the AMQP
            connection when a disconnect is detected.
        :type auto_reconnect: bool
        """
        self._auto_reconnect = auto_reconnect
