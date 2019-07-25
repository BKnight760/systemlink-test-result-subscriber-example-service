# -*- coding: utf-8 -*-
"""
Implementation of 'MessageHeader' class
"""
from __future__ import absolute_import

# Import python libs
import datetime
import sys
import uuid

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus import error_code_registry
from systemlink.messagebus.error import Error
# pylint: enable=import-error

ROUTING_KEY_PREFIX = 'Skyline'
USER_PROPERTY = 'User'
ORIGIN_PROPERTY = 'Origin'
REPLY_TO_PROPERTY = 'ReplyTo'
IGNORE_RESPONSE_PROPERTY = 'IgnoreResponse'
MESSAGE_ID_PROPERTY = 'MessageId'
DELIVERY_TAG_PROPERTY = 'DeliveryTag'
CONSUMER_TAG_PROPERTY = 'ConsumerTag'
PERSISTENT_PROPERTY = 'Persistent'
CONTENT_ENCODING_PROPERTY = 'ContentEncoding'
ERROR_CODE_PROPERTY = 'ErrorCode'
ERROR_INFO_PROPERTY = 'ErrorInfo'
ERROR_ARGS_PROPERTY = 'ErrorArgs'
JSON_MESSAGE_CONTENT_TYPE = 'application/json'
BINARY_MESSAGE_CONTENT_TYPE = 'application/octet-stream'


class MessageHeader(object):  # pylint: disable=too-many-public-methods,too-many-instance-attributes
    """
    Message Header.

    This contains all the message metadata which is not part of the message
    body.
    """
    def __init__(self,
                 message_name=None,
                 content_type=None,
                 routing_param=None):
        """
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
        """
        self._message_name = message_name
        self._content_type = content_type
        self._routing_key = None
        if message_name:
            self._routing_key = MessageHeader.generate_routing_key(routing_param, message_name)
        self._properties = {}
        self._timestamp = None
        self._correlation_id = None
        self.ensure_properties()

    def ensure_properties(self, reply_to=None):
        """
        This will ensure certain properties in the message header are set.
        In particular, it will ensure that the ``reply to``, the
        ``message ID``, the ``correlation ID``, and the ``timestamp`` are set
        if they haven't been previously set.

        :param reply_to: The ``reply to`` setting. May be ``None``.
        :type reply_to: str or None
        """
        if not self.reply_to:
            self.reply_to = reply_to
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self._correlation_id:
            self._correlation_id = self.message_id
        self._timestamp = datetime.datetime.utcnow()

    @staticmethod
    def generate_routing_key(routing_param, message_name):
        """
        Generate the routing key. If ``routing_param`` is set, the
        routing key would be ``Skyline.<routing_param>.<message_name>``.
        If ``routing_param`` is ``None``, the routing key would be
        ``Skyline.<message_name>``

        :param routing_param: The routing parameter. If this is not ``None``,
            it is used to generate the second last part of the routing key,
            just before the message name. May be ``None``.
        :type routing_param: str or None
        :param message_name: The name of the message. This is used to generate
            the last part of the routing key.
        :type message_name: str
        """
        if not routing_param:
            return ROUTING_KEY_PREFIX + '.' + message_name
        return ROUTING_KEY_PREFIX + '.' + routing_param + '.' + message_name

    @property
    def routing_key(self):
        """
        Get the routing key.

        :return: The routing key.
        :rtype: str
        """
        return self._routing_key

    @routing_key.setter
    def routing_key(self, routing_key):
        """
        Set the routing key.

        :param routing_key: The routing key.
        :type routing_key: str
        """
        self._routing_key = routing_key

    @property
    def message_name(self):
        """
        Get the message name.

        :return: The message name.
        :rtype: str
        """
        return self._message_name

    @message_name.setter
    def message_name(self, message_name):
        """
        Set the message name.

        :param message_name: The message name.
        :type message_name: str
        """
        self._message_name = message_name

    @property
    def content_type(self):
        """
        Get the content type. Examples are ``application/json`` and
        ``application/octet-stream``.

        :return: The content type. May be ``None``.
        :rtype: str or None
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type):
        """
        Set the content type. Examples are ``application/json`` and
        ``application/octet-stream``.

        :param content_type: The content type. May be ``None``.
        :type content_type: str or None
        """
        self._content_type = content_type

    @property
    def correlation_id(self):
        """
        Get the correlation ID.

        :return: The correlation ID.
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """
        Set the correlation ID.

        :param correlation_id: The correlation ID.
        :type correlation_id: str
        """
        self._correlation_id = correlation_id

    @property
    def timestamp(self):
        """
        Get the timestamp (in UTC).

        :return: The timestamp (in UTC).
        :rtype: datetime.datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Set the timestamp (in UTC).

        :param timestamp: The timestamp (in UTC).
        :type timestamp: datetime.datetime
        """
        self._timestamp = timestamp

    @property
    def properties(self):
        """
        Get the properties dictionary.

        :return: The properties dictionary. Both keys and values are
            strings.
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Set the properties dictionary.

        :param properties: The properties dictionary. Both keys and
            values are strings.
        :type properties: dict(str, str)
        """
        self._properties = properties

    @property
    def origin(self):
        """
        Get the ``Origin`` property.

        :return: The ``Origin`` property.
        :rtype: str
        """
        origin = self.get_property(ORIGIN_PROPERTY)
        return '' if origin is None else origin

    @origin.setter
    def origin(self, origin):
        """
        Set the ``Origin`` property.

        :param origin: The ``Origin`` property.
        :type origin: str
        """
        self.set_property(ORIGIN_PROPERTY, origin)

    @property
    def reply_to(self):
        """
        Get the ``ReplyTo`` property.

        :return: The ``ReplyTo`` property.
        :rtype: str
        """
        reply_to = self.get_property(REPLY_TO_PROPERTY)
        if reply_to is None:
            return ''
        return reply_to

    @reply_to.setter
    def reply_to(self, reply_to):
        """
        Set the ``ReplyTo`` property.

        :param reply_to: The ``ReplyTo`` property.
        :type reply_to: str
        """
        self.set_property(REPLY_TO_PROPERTY, reply_to)

    @property
    def ignore_response(self):
        """
        Get the ``IgnoreResponse`` property.

        :return: The ``IgnoreResponse`` property.
        :rtype: bool
        """
        return self.get_bool_property(IGNORE_RESPONSE_PROPERTY)

    @ignore_response.setter
    def ignore_response(self, ignore_response):
        """
        Set the ``IgnoreResponse`` property.

        :param ignore_response: The ``IgnoreResponse`` property.
        :type ignore_response: bool
        """
        if ignore_response is None:
            self.clear_property(IGNORE_RESPONSE_PROPERTY)
        else:
            self.set_property(IGNORE_RESPONSE_PROPERTY, ignore_response)

    @property
    def message_id(self):
        """
        Get the ``MessageId`` property.

        :return: The ``MessageId`` property.
        :rtype: str
        """
        message_id = self.get_property(MESSAGE_ID_PROPERTY)
        if message_id is None:
            return ''
        return message_id

    @message_id.setter
    def message_id(self, message_id):
        """
        Set the ``MessageId`` property.

        :param message_id: The ``MessageId`` property.
        :type message_id: str
        """
        self.set_property(MESSAGE_ID_PROPERTY, message_id)

    @property
    def delivery_tag(self):
        """
        Get the ``DeliveryTag`` property.

        :return: The ``DeliveryTag`` property.
        :rtype: str
        """
        delivery_tag = self.get_property(DELIVERY_TAG_PROPERTY)
        if delivery_tag is None:
            return ''
        return delivery_tag

    @delivery_tag.setter
    def delivery_tag(self, delivery_tag):
        """
        Set the ``DeliveryTag`` property.

        :param delivery_tag: The ``DeliveryTag`` property.
        :type delivery_tag: str
        """
        self.set_property(DELIVERY_TAG_PROPERTY, delivery_tag)

    @property
    def consumer_tag(self):
        """
        Get the ``ConsumerTag`` property.

        :return: The ``ConsumerTag`` property.
        :rtype: str
        """
        consumer_tag = self.get_property(CONSUMER_TAG_PROPERTY)
        if consumer_tag is None:
            return ''
        return consumer_tag

    @consumer_tag.setter
    def consumer_tag(self, consumer_tag):
        """
        Set the ``ConsumerTag`` property.

        :param consumer_tag: The ``ConsumerTag`` property.
        :type consumer_tag: str
        """
        self.set_property(CONSUMER_TAG_PROPERTY, consumer_tag)

    @property
    def persistent(self):
        """
        Get the ``Persistent`` property.

        :return: The ``Persistent`` property.
        :rtype: bool
        """
        return self.get_bool_property(PERSISTENT_PROPERTY)

    @persistent.setter
    def persistent(self, persistent):
        """
        Set the ``Persistent`` property.

        :param persistent: The ``Persistent`` property.
        :type persistent: bool
        """
        self.set_property(PERSISTENT_PROPERTY, persistent)

    @property
    def error(self):
        """
        Get the error-related properties.

        :return: The error-related properties combined
            into an instance of :class:`systemlink.messagebus.error.Error`.
        :rtype: systemlink.messagebus.error.Error or None
        """
        error_code_str = self.get_property(ERROR_CODE_PROPERTY)
        error_info_str = self.get_property(ERROR_INFO_PROPERTY)
        idx = 0
        args = []
        while True:
            arg_prop_name = '{0}{1}'.format(ERROR_ARGS_PROPERTY, idx)
            arg = self.get_property(arg_prop_name)
            if not arg:
                break
            args.append(arg)
            idx += 1

        if error_code_str:
            error_code_obj = error_code_registry.lookup(error_code_str)
        else:
            error_code_obj = error_code_registry.lookup('Unknown')

        if not error_info_str:
            error_info_str = ''

        error_obj = Error(error_code_obj, error_info_str, args)
        return error_obj

    @error.setter
    def error(self, error):
        """
        Set the error-related properties.

        :param error: An instance of :class:`systemlink.messagebus.error.Error`.
        :type error: systemlink.messagebus.error.Error or None
        """
        # Clear any old properties in case some are not set.
        self.clear_property(ERROR_CODE_PROPERTY)
        self.clear_property(ERROR_INFO_PROPERTY)
        idx = 0
        while True:
            arg_prop_name = '{0}{1}'.format(ERROR_ARGS_PROPERTY, idx)
            if arg_prop_name not in self._properties:
                break
            self.clear_property(arg_prop_name)
            idx += 1

        if error is None:
            return

        qualified_name = error.name
        if not qualified_name:
            return

        self.set_property(ERROR_CODE_PROPERTY, qualified_name)
        error_info = error.info
        self.set_property(ERROR_INFO_PROPERTY, error_info)

        error_args = error.args
        for idx, arg in enumerate(error_args):
            arg_prop_name = '{0}{1}'.format(ERROR_ARGS_PROPERTY, idx)
            self.set_property(arg_prop_name, arg)

    def has_error(self):
        """
        Determine whether the error-related properties are set.

        :return: ``True`` if the error-related properties are set.
            ``False`` otherwise.
        :rtype: bool
        """
        error_code = self.get_property(ERROR_CODE_PROPERTY)
        if error_code:
            return True
        return False

    def get_property(self, key):
        """
        Get a specific property.

        :param key: The name of the property.
        :type key: str
        :return: The value of the property as a string or ``None`` if
            the property does not exist.
        :rtype: str or None
        """
        return self._properties.get(key, None)

    def get_bool_property(self, key):
        """
        Get a specific property and convert its value to a
        :class:`bool`.

        :param key: The name of the property.
        :type key: str
        :return: The value of the property as a :class:`bool` or ``False`` if
            the property does not exist.
        :rtype: bool
        """
        value = self.get_property(key)
        if value == 'True':
            return True
        return False

    def get_int_property(self, key):
        """
        Get a specific property and convert its value to a
        :class:`int`.

        :param key: The name of the property.
        :type key: str
        :return: The value of the property as a :class:`int` or ``0`` if
            the property does not exist.
        :rtype: int
        """
        value = self.get_property(key)
        return int(value)

    def get_ulong_property(self, key):
        """
        Get a specific property and convert its value to a
        :class:`int`. For compatibility with other programming
        languages since :class:`int` may hold values that are
        as big as an unsigned 64-bit integer in other programming
        languages.

        :param key: The name of the property.
        :type key: str
        :return: The value of the property as a :class:`int` or ``0`` if
            the property does not exist.
        :rtype: int
        """
        value = self.get_property(key)
        if sys.version_info[0] < 3:
            return long(value)  # pylint: disable=undefined-variable
        return int(value)

    def set_property(self, key, value):
        """
        Set a specific property.

        :param key: The name of the property.
        :type key: str
        :param value: The value of the property. If ``None``, will
            be converted to an empty string. If another type, will
            convert to a :class:`str` via ``str(value)``.
        :type value: str or None
        """
        if value is None:
            value = ''
        self._properties[key] = str(value)

    def clear_property(self, key):
        """
        Remove a specific property. Safe to invoke if the property does
        not currently exist.

        :param key: The name of the property.
        :type key: str
        """
        self._properties.pop(key, None)

    @property
    def log_string(self):
        """
        Return a string meant for logging the key header information.
        Information in this string include the message ID, the message
        name, the routing key, the origin, and the correlation ID.

        :return: A string meant for logging the key header information.
        :rtype: str
        """
        separator = ' | '
        log_string = 'Id='
        log_string += self.message_id
        log_string += separator
        log_string += 'Type='
        log_string += self.message_name
        log_string += separator
        log_string += 'Routing='
        log_string += self._routing_key
        log_string += separator
        log_string += 'Origin='
        log_string += self.origin
        log_string += separator
        log_string += 'Corr='
        log_string += self._correlation_id
        return log_string
