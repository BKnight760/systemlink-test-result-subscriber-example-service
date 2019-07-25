# -*- coding: utf-8 -*-
"""
Implementation of 'AmqpConnectionManager' class
"""
from __future__ import absolute_import

# Import python libs
import logging
import sys

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.amqp_configuration_manager import AmqpConfigurationManager
from systemlink.messagebus.amqp_consumer_connection import AmqpConsumerConnection
from systemlink.messagebus.amqp_publisher_connection import AmqpPublisherConnection
if sys.version_info[0] < 3:
    from Queue import Queue, Empty, Full
else:
    from queue import Queue, Empty, Full
# pylint: enable=import-error

# Set up logging
LOGGER = logging.getLogger(__name__)


class AmqpConnectionManager(object):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """
    AMQP Connection Manager.

    Factory for :class:`systemlink.messagebus.amqp_connection.AMQPConnection`
    objects.
    """
    _instance = None

    def __init__(self, config=None):
        """
        :param config: The configuration for the connections created by
            :class:`AmqpConnectionManager`, as a
            :class:`systemlink.messagebus.configuration.Configuration` object.
            If this is ``None``, will use the default configuration.
        :type config: systemlink.messagebus.configuration.Configuration or None
        """
        self._closing = False
        self._requested_heartbeat = 270
        self._timeout_seconds = 180
        self._auto_reconnect = True
        self._exception = None
        self._amqp_consumer_connection = None
        self._amqp_publisher_connection = None

        if config is None:
            config = AmqpConfigurationManager.get_configuration()

        self._host_name = config.host
        self._exchange_name = config.exchange_name
        self._user_name = config.user
        self._password = config.password
        self._port = config.port
        self._use_tls = config.use_tls
        self._tls_server_name = config.tls_server_name
        self._cert_path = config.cert_path
        self._status_queue = Queue()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        """
        Close this instance of :class:`AmqpConnectionManager`.
        """
        if self._closing:
            return
        self._closing = True
        LOGGER.debug('AmqpConnectionManager close!')
        cls = self.__class__
        if self._amqp_consumer_connection is not None:
            self._amqp_consumer_connection.close()
        if self._amqp_publisher_connection is not None:
            self._amqp_publisher_connection.close()
        if cls._instance == self:  # pylint: disable=protected-access
            cls._instance = None  # pylint: disable=protected-access

    @classmethod
    def get_instance(cls):
        """
        Returns a singleton instance of :class:`AmqpConnectionManager`.
        This instance is shared within the same Python process.

        :return: An instance of :class:`AmqpConnectionManager`.
        :rtype: AmqpConnectionManager
        """
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    @property
    def connection_timeout(self):
        """
        Get the connection timeout.

        :return: The connection timeout in seconds.
        :rtype: timeout_seconds: int or float
        """
        return self._timeout_seconds

    @connection_timeout.setter
    def connection_timeout(self, timeout_seconds):
        """
        Set the connection timeout.

        :param timeout_seconds: The connection timeout in seconds.
        :type timeout_seconds: int or float
        """
        self._timeout_seconds = timeout_seconds

    def create_consumer_channel(self):
        """
        Create a channel meant for consumption (reading).

        :return: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel`
            object.
        :rtype: systemlink.messagebus.amqp_channel.AmqpChannel
        """
        return self._get_consumer_connection().create_channel()

    def create_publisher_channel(self):
        """
        Create a channel meant for publishing (writing).

        :return: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel`
            object.
        :rtype: systemlink.messagebus.amqp_channel.AmqpChannel
        """
        return self._get_publisher_connection().create_channel()

    def queue_declare(self, amqp_channel, queue_name, durable, exclusive, autodelete):  # pylint: disable=too-many-arguments
        """
        Declare a queue.

        :param amqp_channel: A `systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param queue_name: The queue name.
        :type queue_name: str
        :param durable: ``True`` if the queue is durable (backed up to
            persistent storage).
        :type durable: bool
        :param exclusive: ``True`` if the queue is exclusive.
        :type exclusive: bool
        :param autodelete: ``True`` is the queue should automatically delete
            itself when it is no longer referenced.
        :type autodelete: bool
        """
        self._get_consumer_connection().queue_declare(
            amqp_channel, queue_name, durable, exclusive, autodelete
        )

    def basic_qos(self, amqp_channel, prefetch_size, prefetch_count, global_qos):  # pylint: disable=too-many-arguments
        """
        Specify quality of service.

        :param amqp_channel: A `systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param prefetch_size: The prefetch window size. ``0`` means no
            specific limit.
        :type prefetch_size: int
        :param prefetch_count: Specifies a prefetch window in terms of
            whole messages.
        :type prefetch_count: int
        :param global_qos: ``True`` if the QoS should apply to all
            consumers on the channel. ``False`` if the QoS should
            apply only to this consumer.
        :type global_qos: bool
        """
        self._get_consumer_connection().basic_qos(
            amqp_channel, prefetch_size, prefetch_count, global_qos
        )

    def publish_message(self, amqp_channel, header, body, mandatory=False):
        """
        Publish a message.

        :param amqp_channel: A `systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param header: A :class:`systemlink.messagebus.message_header.MessageHeader`
            object.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The message body.
        :type body: bytes
        :param mandatory: If ``True``, the broker will return an unroutable message
            to the sender as a ``Return`` message.
        :type mandatory: bool
        """
        self._get_publisher_connection().publish_message(amqp_channel, header, body, mandatory)

    def acknowledge_message(self, amqp_channel, delivery_tag):
        """
        Acknowledge a message (meaning that it has been processed by this
        consumer).

        :param amqp_channel: A `systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param delivery_tag: The message delivery tag.
        :type delivery_tag: str
        """
        self._get_consumer_connection().acknowledge_message(amqp_channel, delivery_tag)

    def not_acknowledge_message(self, amqp_channel, delivery_tag):
        """
        Not acknowledge a message (meaning that it will not be processed by
        this consumer).

        :param amqp_channel: A `systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param delivery_tag: The message delivery tag.
        :type delivery_tag: str
        """
        self._get_consumer_connection().not_acknowledge_message(amqp_channel, delivery_tag)

    def start_consuming(self, auto_ack):
        """
        Signal the AMQP connection to start consuming messages.

        :param auto_ack: If ``True``, automatic acknowledgement mode
            will be used (see http://www.rabbitmq.com/confirms.html).
            This corresponds to the ``no_ack`` parameter in the
            basic.consume AMQP 0.9.1 method.
        :type auto_ack: bool
        """
        self._get_consumer_connection().start_consuming(auto_ack)

    def stop_consuming(self):
        """
        Signal the AMQP connection to stop consuming messages.
        """
        self._get_consumer_connection().stop_consuming()

    def register_binding(self, amqp_channel, queue_name, binding_parameters):
        """
        Register a binding.

        :param amqp_channel: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param queue_name: The queue name.
        :type queue_name: str
        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        binding_added = amqp_channel.add_binding(queue_name, binding_parameters)
        if binding_added:
            self._get_consumer_connection().register_binding(
                amqp_channel, queue_name, binding_parameters
            )

    def unregister_binding(self, amqp_channel, queue_name, binding_parameters):
        """
        Unregister a binding.

        :param amqp_channel: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param queue_name: The queue name.
        :type queue_name: str
        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        binding_removed = amqp_channel.remove_binding(queue_name, binding_parameters)
        if binding_removed:
            self._get_consumer_connection().unregister_binding(
                amqp_channel, queue_name, binding_parameters
            )

    def reregister_bindings(self, amqp_channel):
        """
        Re-register previously registered bindings.

        This is to be invoked after a reconnect to restore the bindings.

        :param amqp_channel: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        """
        bindings = amqp_channel.bindings
        for binding in bindings:
            self._get_consumer_connection().register_binding(
                amqp_channel, binding.queue_name, binding.binding_parameters
            )

    @property
    def exchange_name(self):
        """
        Get the exchange name.

        :return: The exchange name.
        :rtype: str
        """
        return self._exchange_name

    def get_status_message(self, block, timeout_seconds=None):
        """
        Get the next status message from the status message queue.

        :param block: ``True`` if we block to wait for the next status
            message. ``False`` if we return immediately.
        :type block: bool
        :param timeout_seconds: The number of seconds to wait if ``block`` is
            ``True``. Use ``None`` to wait indefinitely. Ignored if ``block``
            is ``False``.
        :type timeout_seconds: int or float or None
        :return: The status message or ``None`` if no status message was found
            during the waiting period.
        :rtype: str or None
        """
        try:
            return self._status_queue.get(block, timeout_seconds)
        except Empty:
            return None

    def put_status_message(self, status_message, block, timeout_seconds=None,
                           replace_if_full=False):
        """
        Put a status message onto the status message queue.

        :param status_message: The status message or ``None`` if no status
             message was found during the waiting period.
        :type status_message: str
        :param block: ``True`` if we block to wait when the status message
            queue is full. ``False`` if we return immediately.
        :type block: bool
        :param timeout_seconds: The number of seconds to wait if ``block`` is
            ``True``. Use ``None`` to wait indefinitely. Ignored if ``block``
            is ``False``.
        :type timeout_seconds: int or float or None
        :return: ``True`` if the status message was successfully placed on
            the status message queue. ``False`` otherwise.
        :rtype: bool
        """
        try:
            self._status_queue.put(status_message, block, timeout_seconds)
            return True
        except Full:
            if replace_if_full:
                self._status_queue.get(False)
                self._status_queue.put(status_message, False)
                return True
            return False

    @property
    def exception(self):
        """
        Get the last stored exception.

        :return: An instance of a class that inherits from
            :class:`Exception`.
        :rtype: Exception
        """
        return self._exception

    @exception.setter
    def exception(self, exception):
        """
        Store an exception.

        :param exception: An instance of a class that inherits from
            :class:`Exception`.
        :type exception: Exception
        """
        self._exception = exception

    def _get_consumer_connection(self):
        """
        Get a connection meant for consumption (reading).

        :return: A
            :class:`systemlink.messagebus.amqp_consumer_connection.AmqpConsumerConnection`
            object.
        :rtype: systemlink.messagebus.amqp_consumer_connection.AmqpConsumerConnection
        """
        if (self._amqp_consumer_connection is not None and
                self._amqp_consumer_connection._closing is False):  # pylint: disable=protected-access
            return self._amqp_consumer_connection

        self._amqp_consumer_connection = AmqpConsumerConnection(
            self,
            self._user_name,
            self._password,
            self._host_name,
            self._port,
            self._exchange_name,
            self._use_tls,
            self._tls_server_name,
            self._cert_path,
            self._timeout_seconds)
        return self._amqp_consumer_connection

    def _get_publisher_connection(self):
        """
        Get a connection meant for publishing (writing).

        :return: A
            :class:`systemlink.messagebus.amqp_publisher_connection.AmqpPublisherConnection`
            object.
        :rtype: systemlink.messagebus.amqp_publisher_connection.AmqpPublisherConnection
        """
        if (self._amqp_publisher_connection is not None and
                self._amqp_publisher_connection._closing is False):  # pylint: disable=protected-access
            return self._amqp_publisher_connection

        self._amqp_publisher_connection = AmqpPublisherConnection(
            self,
            self._user_name,
            self._password,
            self._host_name,
            self._port,
            self._exchange_name,
            self._use_tls,
            self._tls_server_name,
            self._cert_path,
            self._timeout_seconds)
        return self._amqp_publisher_connection

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

    def handle_message_returned(self, correlation_id, message_type):
        """
        Handle the case when a mandatory message was returned.

        :param correlation_id: The correlation ID of the returned message.
        :type correlation_id: str
        :param message_type: The message type of the returned message.
        :type message_type: str
        """
        self._get_consumer_connection().handle_message_returned(correlation_id, message_type)
