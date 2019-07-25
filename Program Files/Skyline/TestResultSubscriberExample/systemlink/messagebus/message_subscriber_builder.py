# -*- coding: utf-8 -*-
"""
Implementation of 'MessageSubscriberBuilder' class
"""
from __future__ import absolute_import


class MessageSubscriberBuilder(object):  # pylint: disable=too-many-public-methods, too-many-instance-attributes
    """
    Message Subscriber Builder.

    This is used for the construction of a
    :class:`systemlink.messagebus.message_subscriber.MessageSubscriber` object.
    """
    def __init__(self, queue_name=None):
        self._queue_name = queue_name
        self._number_of_amqp_consumers = 1
        self._max_local_queue_depth = 100
        self._local_queue_task_threads = 1
        self._prefetch_queue_depth = 100
        self._auto_start_consumers = True
        self._register_default_binding = True
        # Default to 6 hours... is this reasonable?
        self._correlation_id_timeout = 6 * 60 * 60
        self._durable_queue = False
        self._explicit_ack = False
        self._trace_logger = None
        self._callback = None
        self._connection_manager = None
        self._is_instance_subscriber = False

    @property
    def connection_manager(self):
        """
        Get the Connection Manager. If this is ``None``, a new
        Connection Manager will be created during the creation
        of :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`.

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
        of :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`.

        :param connection_manager: The Connection Manager. May be ``None``.
        :type connection_manager:
            systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager
            or None
        """
        self._connection_manager = connection_manager

    @property
    def queue_name(self):
        """
        Get the message queue name.

        :return: The message queue name.
        :rtype: str
        """
        return self._queue_name

    @queue_name.setter
    def queue_name(self, queue_name):
        """
        Set the message queue name.

        :param queue_name: The message queue name.
        :type queue_name: str
        """
        self._queue_name = queue_name

    @property
    def callback(self):
        """
        Get the callback that is invoked whenever a message is
        received by the Message Subscriber unless there is a more specific
        callback registered.

        :return: The callback for handling messages. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :rtype: callable
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        """
        Set the callback that is invoked whenever a message is
        received by the Message Subscriber unless there is a more specific
        callback registered.

        :param callback: The callback for handling messages. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        """
        self._callback = callback

    @property
    def number_of_amqp_consumers(self):
        """
        Get the number of
        :class:`systemlink.messagebus.amqp_consumer.AmqpConsumer` objects
        that will be created.

        :return: The number of
            :class:`systemlink.messagebus.amqp_consumer.AmqpConsumer`
            objects that will be created.
        :rtype: int
        """
        return self._number_of_amqp_consumers

    @number_of_amqp_consumers.setter
    def number_of_amqp_consumers(self, number_of_amqp_consumers):
        """
        Set the number of
        :class:`systemlink.messagebus.amqp_consumer.AmqpConsumer` objects
        that will be created.

        :param number_of_amqp_consumers: The number of
            :class:`systemlink.messagebus.amqp_consumer.AmqpConsumer`
            objects that will be created.
        :type number_of_amqp_consumers: int
        """
        self._number_of_amqp_consumers = number_of_amqp_consumers

    @property
    def max_local_queue_depth(self):
        """
        Get the maximum number of items that may be placed in the local
        message queue.

        :return: The maximum number of items that may be placed in the local
            message queue.
        :rtype: int
        """
        return self._max_local_queue_depth

    @max_local_queue_depth.setter
    def max_local_queue_depth(self, max_local_queue_depth):
        """
        Set the maximum number of items that may be placed in the local
        message queue.

        :param max_local_queue_depth: The maximum number of items that
            may be placed in the local message queue.
        :type max_local_queue_depth: int
        """
        self._max_local_queue_depth = max_local_queue_depth

    @property
    def local_queue_task_threads(self):
        """
        Get the number of task threads to use when processing items in
        the local message queue.

        :return: The number of task threads to use when processing items in
            the local message queue.
        :rtype: int
        """
        return self._local_queue_task_threads

    @local_queue_task_threads.setter
    def local_queue_task_threads(self, local_queue_task_threads):
        """
        Set the number of task threads to use when processing items in
        the local message queue.

        :param local_queue_task_threads: The number of task threads to
            use when processing items in the local message queue.
        :type local_queue_task_threads: int
        """
        self._local_queue_task_threads = local_queue_task_threads

    @property
    def durable_queue(self):
        """
        Get whether the queue is ``durable``. A ``durable`` queue can
        survive a broker restart, however, only ``persistent`` messages
        will be recovered.

        :return: ``True`` if the queue is ``durable``. ``False``
            otherwise.
        :rtype: bool
        """
        return self._durable_queue

    @durable_queue.setter
    def durable_queue(self, durable_queue):
        """
        Set whether the queue is ``durable``. A ``durable`` queue can
        survive a broker restart, however, only ``persistent`` messages
        will be recovered.

        :param durable_queue: ``True`` if the queue is ``durable``.
            ``False`` otherwise.
        :type durable_queue: bool
        """
        self._durable_queue = durable_queue

    @property
    def explicit_ack(self):
        """
        Get whether the
        :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`
        object is responsible for acknowledging incoming messages.

        :return: ``True`` if the
            :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`
            object is responsible for acknowledging incoming messages.
            ``False`` otherwise.
        :rtype: bool
        """
        return self._explicit_ack

    @explicit_ack.setter
    def explicit_ack(self, explicit_ack):
        """
        Set whether the
        :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`
        object is responsible for acknowledging incoming messages.

        :param explicit_ack: ``True`` if the
            :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`
            object is responsible for acknowledging incoming messages.
            ``False`` otherwise.
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
    def auto_start_consumers(self):
        """
        Get whether to auto start consumers.

        :return: ``True`` if the consumers will be started during
            creation of
            :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`.
            ``False`` otherwise.
        :rtype: bool
        """
        return self._auto_start_consumers

    @auto_start_consumers.setter
    def auto_start_consumers(self, auto_start_consumers):
        """
        Set whether to auto start consumers.

        :param auto_start_consumers: ``True`` if the consumers will be
            started during creation of
            :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`.
            ``False`` otherwise.
        :type auto_start_consumers: bool
        """
        self._auto_start_consumers = auto_start_consumers

    @property
    def register_default_binding(self):
        """
        Get whether to use the default registration binding. If so, it
        will automatically register the binding during creation of
        :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`.

        :return: ``True`` to use the default registration binding.
            ``False`` otherwise.
        :rtype: bool
        """
        return self._register_default_binding

    @register_default_binding.setter
    def register_default_binding(self, register_default_binding):
        """
        Set whether to use the default registration binding. If so, it
        will automatically register the binding during creation of
        :class:`systemlink.messagebus.message_subscriber.MessageSubscriber`.

        :param register_default_binding: ``True`` to use the default
            registration binding. ``False`` otherwise.
        :type register_default_binding: bool
        """
        self._register_default_binding = register_default_binding

    @property
    def correlation_id_timeout(self):
        """
        Get the correlation ID timeout (in seconds).

        :return: The correlation ID timeout (in seconds).
        :rtype: float or int
        """
        return self._correlation_id_timeout

    @correlation_id_timeout.setter
    def correlation_id_timeout(self, correlation_id_timeout):
        """
        Set the correlation ID timeout (in seconds).

        :param correlation_id_timeout: The correlation ID timeout
            (in seconds).
        :type correlation_id_timeout: float or int
        """
        self._correlation_id_timeout = correlation_id_timeout

    @property
    def is_instance_subscriber(self):
        """
        Get whether this subscriber is for service instance specific
        messages.

        :return: ``True`` if this subscriber is for service instance
            specific messages. ``False`` otherwise.
        :rtype: bool
        """
        return self._is_instance_subscriber

    @is_instance_subscriber.setter
    def is_instance_subscriber(self, is_instance_subscriber):
        """
        Set whether this subscriber is for service instance specific
        messages.

        :param is_instance_subscriber: ``True`` if this subscriber is
            for service instance specific messages. ``False``
            otherwise.
        :type is_instance_subscriber: bool
        """
        self._is_instance_subscriber = is_instance_subscriber
