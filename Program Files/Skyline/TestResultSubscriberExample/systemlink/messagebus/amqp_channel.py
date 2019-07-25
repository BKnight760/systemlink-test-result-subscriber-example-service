# -*- coding: utf-8 -*-
"""
Implementation of 'Binding' and 'AmqpChannel' classes
"""
from __future__ import absolute_import

# Import python libs
import logging
import sys
import threading

# pylint: disable=import-error
if sys.version_info[0] < 3:
    from Queue import Queue, Empty
else:
    from queue import Queue, Empty
# pylint: enable=import-error

# Import third party libs
# pylint: disable=import-error,wrong-import-position
import pika
# pylint: enable=import-error,wrong-import-position

# Import local libs
# pylint: disable=import-error,wrong-import-position
from systemlink.messagebus.exceptions import SystemLinkException
# pylint: enable=import-error,wrong-import-position

# Set up logging
LOGGER = logging.getLogger(__name__)


def raise_connection_closed():
    """
    Raise a SystemLinkException to indicate that the connection is closed.
    """
    raise SystemLinkException.from_name('Skyline.AMQPErrorOpeningTCPConnection')


class Binding(object):  # pylint: disable=too-few-public-methods
    """
    The binding class maintains the bindings for a queue.
    """
    def __init__(self, queue_name, binding_parameters):
        """
        :param queue_name: The name of the queue that the binding belongs to.
        :type queue_name: str
        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        self.queue_name = queue_name
        self.binding_parameters = binding_parameters


class AmqpChannel(object):  # pylint: disable=too-many-instance-attributes
    """
    AMQP Channel.
    """
    def __init__(self, amqp_connection, channel, channel_id, queue):
        """
        :param amqp_connection: The instance of the
            :class:`systemlink.messagebus.amqp_connection.AmqpConnection`
            object that owns this channel.
        :type amqp_connection: systemlink.messagebus.amqp_connection.AmqpConnection
        :param channel: The channel used by the pika AMQP client.
        :type channel: pika.channel.Channel
        :param channel_id: The channel id number.
        :type channel_id: int
        :param queue: A shared queue to store messages until the
            :class:`systemlink.messagebus.AmqpConsumer` can process them.
        :type queue: Queue.queue
        """
        self._closing = False
        self._queue_name = None
        self._consumer_tag = None
        self._amqp_connection = amqp_connection
        self.channel = channel
        self.channel_id = channel_id
        self.queue = queue
        self.message_returned_queue = Queue()
        self._channel_close_event = threading.Semaphore(0)
        self._bindings = []
        self.channel.add_on_return_callback(self._on_message_returned)

    def __del__(self):
        self.close()

    def close(self):
        """
        Close this instance of :class:`AmqpChannel`.
        """
        if self._closing:
            return
        self._closing = True
        if self.channel:
            self.cancel_consume()
            try:
                self.channel.close()
            except Exception:  # pylint: disable=broad-except
                pass
            self.channel = None

    def add_binding(self, queue_name, binding_parameters):
        """
        Adds a binding to the :class:`AmqpChannel`.

        :param queue_name: The name of the queue that the binding belongs to.
        :type queue_name: str
        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        for binding in self._bindings:
            if (binding.queue_name == queue_name and
                    binding.binding_parameters == binding_parameters):
                return False
        self._bindings.append(Binding(queue_name, binding_parameters))
        return True

    def remove_binding(self, queue_name, binding_parameters):
        """
        Removes a binding to the :class:`AmqpChannel`.

        :param queue_name: The name of the queue that the binding belongs to.
        :type queue_name: str
        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        for binding in self._bindings:
            if (binding.queue_name == queue_name and
                    binding.binding_parameters == binding_parameters):
                self._bindings.remove(binding)
                return True
        return False

    @property
    def bindings(self):
        """
        Returns the list of bindings associated with the :class:`AmqpChannel`.

        :return: A list of bindings.
        :rtype: list(Binding)
        """
        return self._bindings

    def get_message_returned(self):
        """
        Gets information on a mandatory message that was returned on
        this channel.

        :return: A two-tuple with strings for the correlation ID
            and message type, or ``None`` if the queue is empty.
        :rtype: tuple or None
        """
        try:
            return self.message_returned_queue.get_nowait()
        except Empty:
            return None

    @property
    def queue_name(self):
        """
        Get the queue name associated with the :class:`AmqpChannel`.

        :return: The name of the queue associated with the
            :class:`AmqpChannel`.
        :rtype: str
        """
        return self._queue_name

    @queue_name.setter
    def queue_name(self, queue_name):
        """
        Set the queue name associated with the :class:`AmqpChannel`.

        :param queue_name: The name of the queue associated with the
            :class:`AmqpChannel`.
        :type queue_name: str
        """
        self._queue_name = queue_name

    def consume(self, auto_ack):
        """
        Tells the server that this channel wants to start consuming.
        At this point, the server will send messages to the channel
        and they will be received by the '_on_message' callback.

        :param auto_ack: If ``True``, automatic acknowledgement mode
            will be used (see http://www.rabbitmq.com/confirms.html).
            This corresponds to the ``no_ack`` parameter in the
            basic.consume AMQP 0.9.1 method.
        :type auto_ack: bool
        """
        if self._consumer_tag is None and self._queue_name and not self._closing:
            if not self.channel:
                raise_connection_closed()

            if pika.__version__[0] == '0':
                # Backwards compatibility for pika < 1.0.0.
                self._consumer_tag = self.channel.basic_consume(
                    self._on_message,
                    self._queue_name,
                    no_ack=auto_ack
                )
                return

            self._consumer_tag = self.channel.basic_consume(
                self._queue_name,
                self._on_message,
                auto_ack=auto_ack
            )

    def cancel_consume(self):
        """
        Tells the server that this channel wants to stop consuming.
        Safe to call if the channel is not consuming.
        """
        if self._consumer_tag is not None and self.channel:
            try:
                self.channel.basic_cancel(
                    consumer_tag=self._consumer_tag
                )
            except Exception as exc:  # pylint: disable=broad-except
                # Absorb exceptions because the channel may already be closed.
                # There are many potential exceptions for this type of condition,
                # so just absorb the generic Exception.
                LOGGER.debug('Cancel consume returned exception: %s', exc)
            self._consumer_tag = None

    def _on_message(self, channel, method_frame, header_frame, body):  # pylint: disable=unused-argument
        """
        Callback that is invoked by pika when this channel receives
        a message.

        :param channel: A :class:`pika.channel.Channel` object.
        :type channel: pika.channel.Channel
        :param method_frame: A :class:`pika.spec.Basic.Deliver` object.
        :type method_frame: pika.spec.Basic.Deliver
        :param header_frame: A :class:`pika.spec.BasicProperties` object.
        :type header_frame: pika.spec.BasicProperties
        :param body: The message body.
        :type body: bytes
        """
        self.queue.put_nowait((method_frame, header_frame, body))

    def _on_message_returned(self, channel, method_frame, header_frame, body):  # pylint: disable=unused-argument
        """
        Callback that is invoked by pika when this connection receives
        a message that was returned.

        :param channel: A :class:`pika.channel.Channel` object.
        :type channel: pika.channel.Channel
        :param method_frame: A :class:`pika.spec.Basic.Deliver` object.
        :type method_frame: pika.spec.Basic.Deliver
        :param header_frame: A :class:`pika.spec.BasicProperties` object.
        :type header_frame: pika.spec.BasicProperties
        :param body: The message body.
        :type body: bytes
        """
        self._amqp_connection._amqp_connection_manager.handle_message_returned(  # pylint: disable=protected-access
            header_frame.correlation_id,
            header_frame.type
        )

    def perform_publish(self, exchange_name, routing_key, body, properties, mandatory):  # pylint: disable=too-many-arguments
        """
        Publishes a message on the AMQP bus.

        :param exchange_name: The name of the AMQP exchange to publish on.
        :type exchange_name: str
        :param routing_key: The destination routing key for the message.
        :type routing_key: str
        :param body: The message body contents.
        :type body: bytes
        :param properties: A :class:`pika.spec.BasicProperties` object.
        :type properties: pika.spec.BasicProperties
        :param mandatory: The mandatory delivery notification flag.
        :type mandatory: bool
        """
        if not self.channel:
            raise_connection_closed()

        if sys.version_info[0] < 3 and not isinstance(body, str):
            # 'body' does not work as a 'bytearray' in Python 2.
            # For Python 2, ensure that 'body' is a 'str'.
            body = str(body)

        if pika.__version__[0] == '0':
            # Backwards compatibility for pika < 1.0.0.
            self.channel.publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=body,
                properties=properties,
                mandatory=mandatory
            )
            return

        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=body,
            properties=properties,
            mandatory=mandatory
        )
