# -*- coding: utf-8 -*-
"""
Implementation of 'GenericMessage' class
"""
from __future__ import absolute_import


class GenericMessage(object):  # pylint: disable=too-many-public-methods
    """
    A generic message. This message is meant to be a message
    in raw format (without serialization) that is returned
    from the framework when a message is received.

    It is the only message type that does not inherit from
    :class:`systemlink.messagebus.message_base.MessageBase` due to
    this class being meant to not be de-serializable whereas classes
    that inherit from
    :class:`systemlink.messagebus.message_base.MessageBase` are meant to
    be de-serializable.
    """
    def __init__(self, header=None, body=None):
        """
        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The raw message body.
        :type body: bytes
        """
        self._header = header
        self._body = body

    @property
    def header(self):
        """
        Get the message header.

        :return: The message header.
        :rtype: systemlink.messagebus.message_header.MessageHeader
        """
        return self._header

    @header.setter
    def header(self, header):
        """
        Set the message header.

        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        """
        self._header = header

    @property
    def body_bytes(self):
        """
        Get the raw message body.

        :return: The raw message body.
        :rtype: bytes
        """
        return self._body

    @body_bytes.setter
    def body_bytes(self, body_bytes):
        """
        Set the raw message body.

        :param body_bytes: The raw message body.
        :type body_bytes: bytes
        """
        self._body = body_bytes

    def has_error(self):
        """
        Determine whether the error-related properties are set in the
        message header.

        :return: ``True`` if the error-related properties are set.
            ``False`` otherwise.
        :rtype: bool
        """
        return self._header.has_error()

    @property
    def error(self):
        """
        Get the error-related properties from the message header.

        :return: The error-related properties combined
            into an instance of :class:`systemlink.messagebus.error.Error`.
        :rtype: systemlink.messagebus.error.Error or None
        """
        return self._header.error

    @error.setter
    def error(self, error):
        """
        Set the error-related properties in the message header.

        :param error: An instance of :class:`systemlink.messagebus.error.Error`.
        :type error: systemlink.messagebus.error.Error or None
        """
        self._header.error = error

    @property
    def message_name(self):
        """
        Get the message name from the message header.

        :return: The message name.
        :rtype: str
        """
        return self._header.message_name

    @message_name.setter
    def message_name(self, message_name):
        """
        Set the message name in the message header.

        :param message_name: The message name.
        :type message_name: str
        """
        self._header.message_name = message_name

    @property
    def correlation_id(self):
        """
        Get the correlation ID from the message header.

        :return: The correlation ID.
        :rtype: str
        """
        return self._header.correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """
        Set the correlation ID in the message header.

        :param correlation_id: The correlation ID.
        :type correlation_id: str
        """
        self._header.correlation_id = correlation_id

    @property
    def timestamp(self):
        """
        Get the timestamp (in UTC) from the message header.

        :return: The timestamp (in UTC).
        :rtype: datetime.datetime
        """
        return self._header.timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Set the timestamp (in UTC) in the message header.

        :param timestamp: The timestamp (in UTC).
        :type timestamp: datetime.datetime
        """
        self._header.timestamp = timestamp

    @property
    def content_type(self):
        """
        Get the content type from the message header. Examples are
        ``application/json`` and ``application/octet-stream``.

        :return: The content type. May be ``None``.
        :rtype: str or None
        """
        return self._header.content_type

    @content_type.setter
    def content_type(self, content_type):
        """
        Set the content type in the message header. Examples are
        ``application/json`` and ``application/octet-stream``.

        :param content_type: The content type. May be ``None``.
        :type content_type: str or None
        """
        self._header.content_type = content_type

    @property
    def reply_to(self):
        """
        Get the ``ReplyTo`` property from the message header.

        :return: The ``ReplyTo`` property.
        :rtype: str
        """
        return self._header.reply_to

    @reply_to.setter
    def reply_to(self, reply_to):
        """
        Set the ``ReplyTo`` property in the message header.

        :param reply_to: The ``ReplyTo`` property.
        :type reply_to: str
        """
        self._header.reply_to = reply_to

    @property
    def origin(self):
        """
        Get the ``Origin`` property from the message header.

        :return: The ``Origin`` property.
        :rtype: str
        """
        return self._header.origin

    @origin.setter
    def origin(self, origin):
        """
        Set the ``Origin`` property in the message header.

        :param origin: The ``Origin`` property.
        :type origin: str
        """
        self._header.origin = origin

    @property
    def message_id(self):
        """
        Get the ``MessageId`` property from the message header.

        :return: The ``MessageId`` property.
        :rtype: str
        """
        return self._header.message_id

    @property
    def delivery_tag(self):
        """
        Get the ``DeliveryTag`` property from the message header.

        :return: The ``DeliveryTag`` property.
        :rtype: str
        """
        return self._header.delivery_tag

    @property
    def consumer_tag(self):
        """
        Get the ``ConsumerTag`` property from the message header.

        :return: The ``ConsumerTag`` property.
        :rtype: str
        """
        return self._header.consumer_tag
