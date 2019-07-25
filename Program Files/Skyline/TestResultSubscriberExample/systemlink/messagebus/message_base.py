# -*- coding: utf-8 -*-
"""
Implementation of 'MessageBase' class
"""
from __future__ import absolute_import

# Import python libs
import logging
import sys

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.exceptions import SystemLinkException
from systemlink.messagebus.message_header import MessageHeader
# pylint: enable=import-error

# Set up logging
LOGGER = logging.getLogger(__name__)


class MessageBase(object):  # pylint: disable=too-many-public-methods
    """
    Base class for all message types except
    :class:`systemlink.messagebus.generic_message.GenericMessage`.
    This class is meant to be inherited from classes that support
    de-serialization, whereas
    :class:`systemlink.messagebus.generic_message.GenericMessage`
    does not support de-serialization.
    """
    def __init__(self, header, body):
        """
        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The raw message body.
        :type body: bytes
        """
        LOGGER.debug('MessageBase __init__')
        self._header = header
        self._body = body

    @classmethod
    def from_message_name_content_type_routing_param(cls, message_name,  # pylint: disable=invalid-name
                                                     content_type,
                                                     routing_param):
        """
        Create an instance of :class:`MessageBase` based on the message
        name, content type, and routing parameter.

        :param message_name: The name of the message. This is used to generate
            the last part of the routing key. May be ``None``, but in which
            case the routing key will not be generated.
        :type message_name: str or None
        :param content_type: The message content type. Examples are
            ``application/json`` and ``application/octet-stream``. May be
            ``None``.
        :type content_type: str or None
        :param routing_param: The routing parameter. If this is not ``None``,
            it is used to generate the second last part of the routing key,
            just before the message name. May be ``None``.
        :type routing_param: str or None
        :return: A :class:`MessageBase` object with the routing
            information set.
        :rtype: MessageBase
        """
        LOGGER.debug('MessageBase from_message_name_content_type_routing_param')
        header = MessageHeader(message_name, content_type, routing_param)
        return cls(header, None)

    @property
    def body_bytes(self):
        """
        Get the raw message body.

        :return: The raw message body.
        :rtype: bytes
        """
        if self._body is None:
            self._body = self.message_body_as_bytes
        return self._body

    @body_bytes.setter
    def body_bytes(self, body_bytes):
        """
        Set the raw message body.

        :param body_bytes: The raw message body.
        :type body_bytes: bytes
        """
        self._body = body_bytes

    @property
    def message_body_as_bytes(self):  # pylint: disable=no-self-use
        """
        Generate the raw message body from message specific parameters.

        :return: The raw message body.
        :rtype: bytes
        """
        error_info = 'MessageBase.message_body_as_bytes should be overriden by subclass.'
        raise SystemLinkException.from_name('Skyline.UnexpectedException', info=error_info)

    @property
    def header(self):
        """
        Get the message header.

        :return: The message header.
        :rtype: systemlink.messagebus.message_header.MessageHeader
        """
        return self._header

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
    def routing_key(self):
        """
        Get the routing key from the message header.

        :return: The routing key.
        :rtype: str
        """
        return self._header.routing_key

    @routing_key.setter
    def routing_key(self, routing_key):
        """
        Set the routing key in the message header.

        :param routing_key: The routing key.
        :type routing_key: str
        """
        self._header.routing_key = routing_key

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
    def ignore_response(self):
        """
        Get the ``IgnoreResponse`` property from the message header.

        :return: The ``IgnoreResponse`` property.
        :rtype: bool
        """
        return self._header.ignore_response

    @ignore_response.setter
    def ignore_response(self, ignore_response):
        """
        Set the ``IgnoreResponse`` property in the message header.

        :param ignore_response: The ``IgnoreResponse`` property.
        :type ignore_response: bool
        """
        self._header.ignore_response = ignore_response

    @property
    def persistent(self):
        """
        Get the ``Persistent`` property from the message header.

        :return: The ``Persistent`` property.
        :rtype: bool
        """
        return self._header.persistent

    @persistent.setter
    def persistent(self, persistent):
        """
        Set the ``Persistent`` property in the message header.

        :param persistent: The ``Persistent`` property.
        :type persistent: bool
        """
        self._header.persistent = persistent

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

    def get_property(self, key):
        """
        Get a specific property from the message header.

        :param key: The name of the property.
        :type key: str
        :return: The value of the property as a string or ``None`` if
            the property does not exist.
        :rtype: str or None
        """
        return self._header.get_property(key)

    def get_string_property(self, key):
        """
        Get a specific property from the message header and convert
        its value to a :class:`str`.

        :param key: The name of the property.
        :type key: str
        :return: The value of the property as a :class:`str` or empty
            string if the property does not exist.
        :rtype: bool
        """
        value = self._header.get_property(key)
        if value is None:
            return ''
        return str(value)

    def get_bool_property(self, key):
        """
        Get a specific property from the message header and convert
        its value to a :class:`bool`.

        :param key: The name of the property.
        :type key: str
        :return: The value of the property as a :class:`bool` or ``False`` if
            the property does not exist.
        :rtype: bool
        """
        return bool(self._header.get_property(key))

    def get_int_property(self, key):
        """
        Get a specific property from the message header and convert
        its value to a :class:`int`.

        :param key: The name of the property.
        :type key: str
        :return: The value of the property as a :class:`int` or ``0`` if
            the property does not exist.
        :rtype: int
        """
        return int(self._header.get_property(key))

    def get_ulong_property(self, key):
        """
        Get a specific property from the message header and convert
        its value to a :class:`int`. For compatibility with other
        programming languages since :class:`int` may hold values that
        are as big as an unsigned 64-bit integer in other programming
        languages.

        :param key: The name of the property.
        :type key: str
        :return: The value of the property as a :class:`int` or ``0`` if
            the property does not exist.
        :rtype: int
        """
        if sys.version_info[0] < 3:
            return long(self._header.get_property(key))  # pylint: disable=undefined-variable
        return int(self._header.get_property(key))

    def set_property(self, key, value):
        """
        Set a specific property in the message header.

        :param key: The name of the property.
        :type key: str
        :param value: The value of the property. If ``None``, will
            be converted to an empty string. If another type, will
            convert to a :class:`str` via ``str(value)``.
        :type value: str or None
        """
        self._header.set_property(key, value)

    def set_string_property(self, key, value):
        """
        Set a specific :class:`str` property in the message header.

        :param key: The name of the property.
        :type key: str
        :param value: The value of the property. If ``None``, or empty
            string, will remove the property. If another type,
            will convert to a :class:`str` via ``str(value)``.
        :type value: str or None
        """
        if value:
            self._header.set_property(key, value)
        else:
            self._header.clear_property(key)

    def set_bool_property(self, key, value):
        """
        Set a specific :class:`bool` property in the message header.

        :param key: The name of the property.
        :type key: str
        :param value: The value of the property. If ``None``, will
            remove the property.
        :type value: bool or None
        """
        if value is None:
            self._header.clear_property(key)
        elif value:
            self._header.set_property(key, 'True')
        else:
            self._header.set_property(key, 'False')

    def set_int_property(self, key, value):
        """
        Set a specific :class:`int` property in the message header.

        :param key: The name of the property.
        :type key: str
        :param value: The value of the property. If ``None``, will
            remove the property.
        :type value: bool or None
        """
        if value is None:
            self._header.clear_property(key)
        self._header.set_property(key, str(value))
