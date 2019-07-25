# -*- coding: utf-8 -*-
"""
Implementation of 'PublishMessageCallback' and 'MessagePublisher' classes
"""
from __future__ import absolute_import

# Import python libs
import logging

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.amqp_connection_manager import AmqpConnectionManager
from systemlink.messagebus.message_publisher_builder import MessagePublisherBuilder
# pylint: enable=import-error

# Set up logging
LOGGER = logging.getLogger(__name__)


class MessagePublisher(object):  # pylint: disable=too-many-instance-attributes
    """
    The Message Publisher.

    This class is used to publish messages.
    """
    def __init__(self, builder=None):
        """
        :param builder: A
            :class:`systemlink.messagebus.message_publisher_builder.MessagePublisherBuilder`
            object used in the construction of this object. May be ``None`` if default
            behavior is desired.
        :type builder:
            systemlink.messagebus.message_publisher_builder.MessagePublisherBuilder
        """
        if builder is None:
            builder = MessagePublisherBuilder()
        self._connection_manager = builder.connection_manager
        if self._connection_manager is None:
            self._connection_manager = AmqpConnectionManager.get_instance()
        LOGGER.debug('MessagePublisher\'s connection_manager: %s', self._connection_manager)
        self._origin_name = builder.origin
        self._reply_to = builder.reply_to
        self._exchange_name = self._connection_manager.exchange_name
        self._channel = self._connection_manager.create_publisher_channel()
        self._trace_logger = builder.trace_logger
        self._trace_raw_messages = None
        if self._trace_logger:
            self._trace_raw_messages = self._trace_logger.make_trace_point('RawMessages')

    @classmethod
    def from_origin(cls, origin=None):
        """
        Create an instance of :class:`MessagePublisher` based on the
        ``Origin`` message property.

        :param origin: The ``Origin`` message property which is an
            identifier specifying where messages are sent from. Used
            for message routing. May be ``None``.
        :type origin: str or None
        :return: An instance of :class:`MessagePublisher`.
        :rtype: MessageService
        """
        builder = MessagePublisherBuilder(origin)
        return cls(builder)

    def publish_message_base(self, message_base, mandatory=False):
        """
        Publish a message. The class of the message inherits from
        :class:`systemlink.messagebus.message_base.MessageBase`.

        :param message_base: The message to publish. The class of the
            message inherits from
            :class:`systemlink.messagebus.message_base.MessageBase`.
        :type message_base: systemlink.messagebus.message_base.MessageBase
        :param mandatory: The mandatory delivery notification flag.
        :type mandatory: bool
        """
        self.publish_message_callback(message_base, mandatory)

    def publish_generic_message(self, message, mandatory=False):
        """
        Publish a message. The class of the message is
        :class:`systemlink.messagebus.generic_message.GenericMessage`.

        :param message: The message to publish. The class of the
            message is
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type message: systemlink.messagebus.generic_message.GenericMessage
        :param mandatory: The mandatory delivery notification flag.
        :type mandatory: bool
        """
        self._publish_message(message.header, message.body_bytes, mandatory)

    def _publish_message(self, header, body, mandatory=False):
        """
        Publish a message based on the header and body.

        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The raw message body.
        :type body: bytes
        :param mandatory: The mandatory delivery notification flag.
        :type mandatory: bool
        """
        self._update_header(header)
        self._connection_manager.publish_message(self._channel, header, body, mandatory)
        if (self._trace_logger and self._trace_raw_messages and
                self._trace_raw_messages.is_enabled):
            self._trace_logger.log(
                'MsgTx | ' + header.log_string,
                self._trace_raw_messages
            )

    def _update_header(self, header):
        """
        This makes sure the required header properties are set.

        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        """
        header.ensure_properties(self._reply_to)
        if header.origin is None:
            header.origin = self._origin_name

    @property
    def trace_logger(self):
        """
        Get an instance of the Trace Logger.

        :return: An instance of the Trace Logger or ``None`` if there
            is no Trace Logger associated with this object.
        :rtype: systemlink.messagebus.trace_logger.TraceLogger or None
        """
        return self._trace_logger

    def publish_message_callback(self, message_base, mandatory=False):
        """
        The callback function invoked by the framework.

        :param message_base: The message. The class of this object
            inherits from
            :class:`systemlink.messagebus.message_base.MessageBase`.
        :type message_base:
            systemlink.messagebus.message_base.MessageBase
        :param mandatory: The mandatory delivery notification flag.
        :type mandatory: bool
        """
        self._publish_message(
            message_base.header,
            message_base.body_bytes,
            mandatory
        )
