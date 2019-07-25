# -*- coding: utf-8 -*-
"""
Implementation of 'AmqpConsumer' class
"""
from __future__ import absolute_import

# Import python libs
from datetime import datetime
import logging
import sys
import time
import threading

# Import third party libs
# pylint: disable=import-error
import pika.spec
# pylint: enable=import-error

# pylint: disable=import-error
if sys.version_info[0] < 3:
    from Queue import Empty
else:
    from queue import Empty
# pylint: enable=import-error

# Import local libs
# pylint: disable=import-error,wrong-import-position
from systemlink.messagebus.exceptions import SystemLinkException
from systemlink.messagebus.amqp_connection_manager import AmqpConnectionManager
from systemlink.messagebus.generic_message import GenericMessage
from systemlink.messagebus.message_header import MessageHeader, CONSUMER_TAG_PROPERTY
# pylint: enable=import-error,wrong-import-position

# Set up logging
LOGGER = logging.getLogger(__name__)


class AmqpConsumer(object):  # pylint: disable=too-many-instance-attributes
    """
    AMQP Consumer.
    """
    def __init__(self, builder):
        """
        :param builder: A :class:`systemlink.messagebus.amqp_consumer_builder.AmqpConsumerBuilder`
            object used in the construction of this object.
        :type builder: systemlink.messagebus.amqp_consumer_builder.AmqpConsumerBuilder
        """
        self._closing = False
        self._trace_logger = None
        self._trace_raw_messages = None
        self._queue_name = builder.queue_name
        self._routing_key_prefix = builder.routing_key_prefix
        self._durable_queue = builder.durable_queue
        self._callback = builder.callback
        self._message_returned_callback = builder.message_returned_callback
        self._event_args_callback = builder.event_args_callback
        self._auto_reconnect = builder.auto_reconnect
        self._message_handling_thread_should_stop = False  # pylint: disable=invalid-name
        self._monitoring_thread_should_stop = False
        self._should_handle_messages = False
        self._is_handling_messages = False
        self._channel = None
        self._monitoring_thread = None
        self._message_handling_thread = None

        self._connection_manager = builder.connection_manager
        if self._connection_manager is None:
            self._connection_manager = AmqpConnectionManager.get_instance()
        self._exchange_name = self._connection_manager.exchange_name
        self.trace_logger = builder.trace_logger
        self._explicit_ack = builder.explicit_ack
        self._channel = self._connection_manager.create_consumer_channel()
        self._connection_manager.queue_declare(
            self._channel,
            self._queue_name,
            self._durable_queue,
            False,
            not self._durable_queue
        )
        self._channel.queue_name = self._queue_name
        self._connection_manager.basic_qos(
            self._channel,
            0,
            builder.prefetch_queue_depth,
            False
        )
        self._consumer_tag = ''
        self._monitoring_thread = None
        if self._auto_reconnect:
            self._monitoring_thread = threading.Thread(target=self._monitoring_thread_func)
            self._monitoring_thread.daemon = True
            self._monitoring_thread.start()
        self._message_handling_thread = threading.Thread(target=self._message_handling_thread_func)
        self._message_handling_thread.daemon = True
        self._message_handling_thread.start()

    def __del__(self):
        self.close()

    def close(self):
        """
        Close this instance of :class:`AmqpConsumer`.
        """
        if self._closing:
            return
        self._closing = True
        self._message_handling_thread_should_stop = True
        self._monitoring_thread_should_stop = True
        if self._channel is not None:
            self._channel._channel_close_event.release()  # pylint: disable=protected-access
        if self._message_handling_thread is not None:
            self._message_handling_thread.join()
            self._message_handling_thread = None
        if self._monitoring_thread is not None:
            self._monitoring_thread.join()
            self._monitoring_thread = None

    @property
    def consumer_tag(self):
        """
        Get the consumer tag.

        :return: The consumer tag.
        :rtype: str
        """
        return self._consumer_tag

    @consumer_tag.setter
    def consumer_tag(self, consumer_tag):
        """
        Set the consumer tag.

        :param consumer_tag: The consumer tag.
        :type consumer_tag: str
        """
        self._consumer_tag = consumer_tag

    @property
    def trace_logger(self):
        """
        Get the trace logger.

        :return: An instance of
            :class:`systemlink.messagebus.trace_logger.TraceLogger` or ``None``.
        :rtype: systemlink.messagebus.trace_logger.TraceLogger or None
        """
        return self._trace_logger

    @trace_logger.setter
    def trace_logger(self, trace_logger):
        """
        Set the trace logger.

        :param trace_logger: An instance of
            :class:`systemlink.messagebus.trace_logger.TraceLogger` or ``None``.
        :type trace_logger: systemlink.messagebus.trace_logger.TraceLogger or None
        """
        self._trace_logger = trace_logger
        if self._trace_logger is not None:
            self._trace_raw_messages = self._trace_logger.make_trace_point('RawMessages')

    def start_handling_messages(self):
        """
        Signal the AMQP Consumer to start handling messages.
        """
        LOGGER.debug('AmqpConsumer start_handling_messages()')
        self._should_handle_messages = True
        self._connection_manager.start_consuming(not self._explicit_ack)
        LOGGER.debug('Set should_handle_messages = %s', self._should_handle_messages)

    def stop_handling_messages(self):
        """
        Signal the AMQP Consumer to stop handling messages.
        """
        LOGGER.debug('AmqpConsumer stop_handling_messages()')
        if not self._is_handling_messages:
            return
        self._should_handle_messages = False
        self._is_handling_messages = False
        self._connection_manager.stop_consuming()
        LOGGER.debug('Set should_handle_messages = %s', self._should_handle_messages)

    @staticmethod
    def _parse(routing_key, basic_properties, consumer_tag):
        """
        Create a message header out of message parameters.

        :param routing_key: The message routing key.
        :type routing_key: str
        :param basic_properties: The message basic properties.
        :type basic_properties: pika.BasicProperties
        :param consumer_tag: The message consumer tag.
        :type consumer_tag: str
        :return: A message header.
        :rtype: systemlink.messagebus.message_header.MessageHeader
        """
        message_name = basic_properties.type
        content_type = basic_properties.content_type
        correlation_id = basic_properties.correlation_id
        header = MessageHeader()
        header.message_name = message_name
        header.content_type = content_type
        header.routing_key = routing_key

        time_ = basic_properties.timestamp / 1000
        timestamp = datetime.utcfromtimestamp(time_)
        header.timestamp = timestamp
        header.correlation_id = correlation_id

        header.persistent = bool(
            basic_properties.delivery_mode == pika.spec.PERSISTENT_DELIVERY_MODE
        )
        header.set_property(CONSUMER_TAG_PROPERTY, consumer_tag)

        for key, value in basic_properties.headers.items():
            LOGGER.debug('setting %s : %s in header...', key, value)
            header.set_property(key, value)
        return header

    def _message_received(self, method, properties, body):
        """
        Handler for when a message is received.

        :param method: A :class:`pika.spec.Basic.Deliver` object.
        :type method: pika.spec.Basic.Deliver
        :param properties: A :class:`pika.spec.BasicProperties` object.
        :type properties: pika.spec.BasicProperties
        :param body: The message body.
        :type body: bytes
        """
        if self._event_args_callback is not None:
            envelope = (method, properties, body)
            self._event_args_callback(envelope)
        elif self._callback is not None:
            routing_key = method.routing_key
            header = self._parse(routing_key, properties, self._consumer_tag)
            header.delivery_tag = method.delivery_tag
            generic_message = GenericMessage(header, body)
            LOGGER.debug('AmqpConsumer _message_received generic_message = %s', generic_message)
            if self._trace_logger is not None and self._trace_raw_messages.IsEnabled():
                self._trace_logger.Log(
                    self._trace_raw_messages,
                    'MsgRx | ' +
                    generic_message.header.log_string
                )
            self._callback(generic_message)
        elif self._trace_logger is not None:
            self._trace_logger.LogError('No callback defined for ' + self._queue_name)
        else:
            LOGGER.debug('No callback defined, and no tracelogger!')

    def acknowledge_message(self, delivery_tag):
        """
        Acknowledge a message (meaning that it has been processed by this
        consumer).

        :param delivery_tag: The message delivery tag.
        :type delivery_tag: str
        """
        self._connection_manager.acknowledge_message(self._channel, delivery_tag)

    def not_acknowledge_message(self, delivery_tag):
        """
        Not acknowledge a message (meaning that it will not be processed by
        this consumer).

        :param delivery_tag: The message delivery tag.
        :type delivery_tag: str
        """
        self._connection_manager.not_acknowledge_message(self._channel, delivery_tag)

    def register_binding(self, binding_parameters):
        """
        Register a binding.

        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        self._connection_manager.register_binding(
            self._channel, self._queue_name, binding_parameters
        )

    def unregister_binding(self, binding_parameters):
        """
        Unregister a binding.

        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        self._connection_manager.unregister_binding(
            self._channel, self._queue_name, binding_parameters
        )

    def _reinitialize(self):
        """
        Re-initialize this :class:`AmqpConsumer` object after
        a disconnect is detected.
        """
        LOGGER.debug('AmqpConsumer initialize!')
        try:
            self._connection_manager.queue_declare(
                self._channel,
                self._queue_name,
                self._durable_queue,
                False,
                not self._durable_queue
            )
            self._connection_manager.reregister_bindings(self._channel)
        except SystemLinkException as exc:
            LOGGER.debug('Caught exception in AmqpConsumer initialize!')
            self._connection_manager.exception = exc

    def _message_handling_thread_func(self):
        """
        The thread function for the message handling thread.

        Dequeues items from the channel queue and processes them.
        """
        try:  # pylint: disable=too-many-nested-blocks
            LOGGER.debug('AmqpConsumer message_handling_thread!')
            while not self._message_handling_thread_should_stop:  # pylint: disable=too-many-nested-blocks
                try:
                    if self._is_handling_messages and not self._should_handle_messages:
                        # We don't attempt to NACK and requeue messages that we
                        # didn't handle.
                        pass
                    if not self._is_handling_messages and self._should_handle_messages:
                        self._is_handling_messages = True
                    if self._is_handling_messages:
                        while True:
                            try:
                                # Block for 1 second waiting for a message to arrive.
                                method, properties, body = self._channel.queue.get(True, 1)
                                if method is not None:
                                    LOGGER.debug('method = %s', method)
                                    LOGGER.debug('properties = %s', properties)
                                    LOGGER.debug('body = %s', body)
                                    self._message_received(method, properties, body)
                            except Empty:
                                pass
                            returned_msg_info = self._channel.get_message_returned()
                            if (returned_msg_info is not None and
                                    self._message_returned_callback is not None):
                                self._message_returned_callback(
                                    returned_msg_info[0], returned_msg_info[1]
                                )
                            if (not self._should_handle_messages or
                                    self._message_handling_thread_should_stop):
                                break
                            time.sleep(0.0001)
                    else:
                        time.sleep(0.0001)
                except Exception as exc:
                    self._connection_manager.put_status_message(
                        'Caught exception in AmqpConsumer message_handling_thread: {0}'.format(exc),
                        False, replace_if_full=True
                    )
                    raise
                    # LOGGER.debug('Releasing semaphore on exception: %s', exc)
                    # self._channel._channel_close_event.release()
                    # time.sleep(0.0001)
                time.sleep(0.0001)
        except (KeyboardInterrupt, SystemExit):
            LOGGER.debug('AmqpConsumer message_handling_thread exiting due to process exit')
        # We don't attempt to NACK and requeue messages that we didn't handle.

    def _monitoring_thread_func(self):
        """
        The thread function for the monitoring thread.

        Re-declares the queue and re-registers the bindings when a disconnect
        is detected.
        """
        try:
            while True:
                self._channel._channel_close_event.acquire()  # pylint: disable=protected-access
                if self._monitoring_thread_should_stop:
                    break
                LOGGER.debug('AmqpConsumer monitoring_thread calling initialize!')
                self._reinitialize()
        except (KeyboardInterrupt, SystemExit):
            LOGGER.debug('AmqpConsumer monitoring_thread exiting due to process exit')
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.debug('Caught exception %s in AmqpConsumer monitoring_thread!', exc)
