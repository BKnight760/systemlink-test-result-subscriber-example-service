# -*- coding: utf-8 -*-
# DO NOT EDIT! This file is auto-generated.
"""
Classes for SystemLink Message Bus usage.
"""
from __future__ import absolute_import

# Import python libs
import json
import sys
from datetime import datetime  # pylint: disable=unused-import

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.broadcast_message import BroadcastMessage  # pylint: disable=unused-import
from systemlink.messagebus.datetime import from_datetime, to_datetime  # pylint: disable=unused-import
from systemlink.messagebus.message_header import (  # pylint: disable=unused-import
    MessageHeader, JSON_MESSAGE_CONTENT_TYPE, BINARY_MESSAGE_CONTENT_TYPE)
from systemlink.messagebus.message_base import MessageBase
from systemlink.messagebus.request_message import RequestMessage  # pylint: disable=unused-import
from systemlink.messagebus.response_message import ResponseMessage  # pylint: disable=unused-import
from systemlink.messagebus.routed_message import RoutedMessage  # pylint: disable=unused-import
# pylint: enable=import-error

if sys.version_info[0] >= 3:
    long = int  # pylint: disable=redefined-builtin,invalid-name


_PASS_THROUGH_TYPES = {
    'bool',
    'bytearray',
    'float',
    'int',
    'long',
    'object',
    'str'
}

_PRIMITIVE_TYPES = {
    'bool': bool,
    'bytearray': bytearray,
    'datetime': datetime,
    'dict': dict,
    'float': float,
    'int': int,
    'list': list,
    'long': long,
    'object': object,
    'str': str
}


def _str_to_type(type_name):
    """
    Convert a type name to a type.

    :param type_name: The name of the type.
    :type type_name: str
    :return: The corresponding type.
    :rtype: type
    """
    type_ = _PRIMITIVE_TYPES.get(type_name)
    if type_ is not None:
        return type_
    return getattr(sys.modules[__name__], type_name)


def _deserialize(value, type_name):  # pylint: disable=too-many-return-statements,too-many-branches
    """
    Deserialize a value from a Python native type.

    :param value: The value to deserialize.
    :type value: object
    :param type_name: The name of the type of `value``.
    :type type_name: str
    :return: The deserialized object.
    :rtype: object
    """
    if value is None:
        return None
    if not type_name:
        return value
    if type_name.endswith(')'):
        sep_index = type_name.find('(')
        sub_type_name = type_name[sep_index+1:-1]
        type_name = type_name[:sep_index]
        if type_name == 'list':
            if sub_type_name in _PASS_THROUGH_TYPES:
                return value
            return [_deserialize(item, sub_type_name) for item in value]
        assert type_name == 'dict'
        sep_index = sub_type_name.find(',')
        key_type_name = sub_type_name[:sep_index]
        value_type_name = sub_type_name[sep_index+1:].strip()
        if key_type_name in _PASS_THROUGH_TYPES and value_type_name in _PASS_THROUGH_TYPES:
            return value
        new_dict = {}
        for dict_key, dict_value in value.items():
            new_dict[_deserialize(dict_key, key_type_name)] = _deserialize(
                dict_value, value_type_name
            )
        return new_dict
    if type_name in _PASS_THROUGH_TYPES:
        return value
    type_ = _str_to_type(type_name)
    if type_ == datetime:
        if not isinstance(value, datetime):
            return to_datetime(value)
        return value
    if hasattr(type_, 'from_dict'):
        return type_.from_dict(value)
    if hasattr(type_, 'from_string'):
        if isinstance(value, int):
            return type_(value)
        return type_.from_string(value)
    if hasattr(type_, 'from_list'):
        if isinstance(value, int):
            return type_(value)
        return type_.from_list(value)
    return value


def _serialize(value):  # pylint: disable=too-many-return-statements
    """
    Serialize a value to a Python native type.

    :param value: The value to serialize.
    :type value: object
    :return: The serialized object.
    :rtype: object
    """
    if value is None:
        return None
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        new_dict = {}
        for dict_key, dict_value in value.items():
            new_dict[_serialize(dict_key)] = _serialize(dict_value)
        return new_dict
    if isinstance(value, datetime):
        return from_datetime(value)
    if hasattr(value, 'to_dict'):
        return value.to_dict()
    if hasattr(value, 'to_string'):
        return value.to_string()
    if hasattr(value, 'to_list'):
        return value.to_list()
    return value


# pylint: disable=line-too-long,too-many-lines,too-many-instance-attributes,too-many-arguments,too-many-locals,useless-object-inheritance


#
# MessageObjects namespace
#


class ServiceState(object):  # pylint: disable=too-few-public-methods
    """
    ServiceState normal enum.
    """
    UNKNOWN = 0
    DISABLED = 1
    MANUAL = 2
    AWAITING_DEPS = 3
    STARTING = 4
    REGISTERED = 5
    IDLE = 6
    LIVE = 7
    ERROR = 8
    UNRESPONSIVE = 9
    DEAD = 10
    SHUTTING_DOWN = 11
    STOPPED = 12
    _INT_TO_STRING = {
        0: 'UNKNOWN',
        1: 'DISABLED',
        2: 'MANUAL',
        3: 'AWAITING_DEPS',
        4: 'STARTING',
        5: 'REGISTERED',
        6: 'IDLE',
        7: 'LIVE',
        8: 'ERROR',
        9: 'UNRESPONSIVE',
        10: 'DEAD',
        11: 'SHUTTING_DOWN',
        12: 'STOPPED'
    }
    _STRING_TO_INT = {
        'UNKNOWN': 0,
        'DISABLED': 1,
        'MANUAL': 2,
        'AWAITING_DEPS': 3,
        'STARTING': 4,
        'REGISTERED': 5,
        'IDLE': 6,
        'LIVE': 7,
        'ERROR': 8,
        'UNRESPONSIVE': 9,
        'DEAD': 10,
        'SHUTTING_DOWN': 11,
        'STOPPED': 12
    }

    def __init__(self, value):
        """
        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @property
    def value(self):
        """
        Get integer value of the enum.

        :return: The integer value of the enum.
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Set integer value of the enum.

        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @classmethod
    def from_string(cls, value_string):
        """
        Create a new instance of :class:`ServiceState` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`ServiceState`.
        :rtype: ServiceState
        """
        if value_string is None:
            return None
        value = cls._STRING_TO_INT[value_string]
        return cls(value)

    def to_string(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self._INT_TO_STRING[self._value]

    def __str__(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self.to_string()


class ServiceStartType(object):  # pylint: disable=too-few-public-methods
    """
    ServiceStartType normal enum.
    """
    SKYLINE_SERVICE = 0
    EXECUTABLE = 1
    _INT_TO_STRING = {
        0: 'SKYLINE_SERVICE',
        1: 'EXECUTABLE'
    }
    _STRING_TO_INT = {
        'SKYLINE_SERVICE': 0,
        'EXECUTABLE': 1
    }

    def __init__(self, value):
        """
        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @property
    def value(self):
        """
        Get integer value of the enum.

        :return: The integer value of the enum.
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Set integer value of the enum.

        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @classmethod
    def from_string(cls, value_string):
        """
        Create a new instance of :class:`ServiceStartType` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`ServiceStartType`.
        :rtype: ServiceStartType
        """
        if value_string is None:
            return None
        value = cls._STRING_TO_INT[value_string]
        return cls(value)

    def to_string(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self._INT_TO_STRING[self._value]

    def __str__(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self.to_string()


class ServiceStartMode(object):  # pylint: disable=too-few-public-methods
    """
    ServiceStartMode normal enum.
    """
    UNKNOWN = 0
    DISABLED = 1
    AUTO = 2
    MANUAL = 3
    _INT_TO_STRING = {
        0: 'UNKNOWN',
        1: 'DISABLED',
        2: 'AUTO',
        3: 'MANUAL'
    }
    _STRING_TO_INT = {
        'UNKNOWN': 0,
        'DISABLED': 1,
        'AUTO': 2,
        'MANUAL': 3
    }

    def __init__(self, value):
        """
        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @property
    def value(self):
        """
        Get integer value of the enum.

        :return: The integer value of the enum.
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Set integer value of the enum.

        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @classmethod
    def from_string(cls, value_string):
        """
        Create a new instance of :class:`ServiceStartMode` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`ServiceStartMode`.
        :rtype: ServiceStartMode
        """
        if value_string is None:
            return None
        value = cls._STRING_TO_INT[value_string]
        return cls(value)

    def to_string(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self._INT_TO_STRING[self._value]

    def __str__(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self.to_string()


class SkylineExeProperties(object):  # pylint: disable=too-few-public-methods
    """
    SkylineExeProperties normal enum.
    """
    PATH = 0
    ARGUMENTS = 1
    USER_ACCOUNT_NAME = 2
    USER_ACCOUNT_PASSWORD_ENCRYPTED = 3
    _INT_TO_STRING = {
        0: 'PATH',
        1: 'ARGUMENTS',
        2: 'USER_ACCOUNT_NAME',
        3: 'USER_ACCOUNT_PASSWORD_ENCRYPTED'
    }
    _STRING_TO_INT = {
        'PATH': 0,
        'ARGUMENTS': 1,
        'USER_ACCOUNT_NAME': 2,
        'USER_ACCOUNT_PASSWORD_ENCRYPTED': 3
    }

    def __init__(self, value):
        """
        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @property
    def value(self):
        """
        Get integer value of the enum.

        :return: The integer value of the enum.
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Set integer value of the enum.

        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @classmethod
    def from_string(cls, value_string):
        """
        Create a new instance of :class:`SkylineExeProperties` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`SkylineExeProperties`.
        :rtype: SkylineExeProperties
        """
        if value_string is None:
            return None
        value = cls._STRING_TO_INT[value_string]
        return cls(value)

    def to_string(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self._INT_TO_STRING[self._value]

    def __str__(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self.to_string()


class LaunchState(object):  # pylint: disable=too-few-public-methods
    """
    LaunchState normal enum.
    """
    DISABLED = 0
    AWAIT_REGISTRATION = 1
    AWAITING_DEPENDENCIES = 2
    READY_TO_LAUNCH = 3
    REGISTERED = 4
    LAUNCHING = 5
    ATTACHING = 6
    RUNNING = 7
    FAILED = 8
    _INT_TO_STRING = {
        0: 'DISABLED',
        1: 'AWAIT_REGISTRATION',
        2: 'AWAITING_DEPENDENCIES',
        3: 'READY_TO_LAUNCH',
        4: 'REGISTERED',
        5: 'LAUNCHING',
        6: 'ATTACHING',
        7: 'RUNNING',
        8: 'FAILED'
    }
    _STRING_TO_INT = {
        'DISABLED': 0,
        'AWAIT_REGISTRATION': 1,
        'AWAITING_DEPENDENCIES': 2,
        'READY_TO_LAUNCH': 3,
        'REGISTERED': 4,
        'LAUNCHING': 5,
        'ATTACHING': 6,
        'RUNNING': 7,
        'FAILED': 8
    }

    def __init__(self, value):
        """
        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @property
    def value(self):
        """
        Get integer value of the enum.

        :return: The integer value of the enum.
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Set integer value of the enum.

        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @classmethod
    def from_string(cls, value_string):
        """
        Create a new instance of :class:`LaunchState` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`LaunchState`.
        :rtype: LaunchState
        """
        if value_string is None:
            return None
        value = cls._STRING_TO_INT[value_string]
        return cls(value)

    def to_string(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self._INT_TO_STRING[self._value]

    def __str__(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self.to_string()


#
# Service service
#


class ServiceGoLiveRoutedMessage(RoutedMessage):
    """
    ServiceGoLiveRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'ServiceGoLiveRoutedMessage'

    def __init__(self,
                 send_to,
                 service_guid_=None):
        """
        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param service_guid_: service_guid
        :type service_guid_: str
        """
        self.service_guid = service_guid_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(ServiceGoLiveRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, send_to, body_dict):
        """
        Create a new instance of :class:`ServiceGoLiveRoutedMessage` using a dictionary.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`ServiceGoLiveRoutedMessage`.
        :rtype: ServiceGoLiveRoutedMessage
        """
        service_guid_ = _deserialize(body_dict.get('serviceGuid'), 'str')
        return cls(
            send_to,
            service_guid_=service_guid_
        )

    @classmethod
    def from_json(cls, send_to, body_json):
        """
        Create a new instance of :class:`ServiceGoLiveRoutedMessage` using a JSON string.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ServiceGoLiveRoutedMessage`.
        :rtype: ServiceGoLiveRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(send_to, body_dict)

    @classmethod
    def from_body_bytes(cls, send_to, body_bytes):
        """
        Create a new instance of :class:`ServiceGoLiveRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ServiceGoLiveRoutedMessage`.
        :rtype: ServiceGoLiveRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(send_to, body_json)

    @classmethod
    def from_message(cls, send_to, message):
        """
        Create a new instance of :class`ServiceGoLiveRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`ServiceGoLiveRoutedMessage`.
        :rtype: ServiceGoLiveRoutedMessage
        """
        instance = cls.from_body_bytes(send_to, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        service_guid_ = _serialize(self.service_guid)
        return {
            'serviceGuid': service_guid_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, send_to, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class ServiceMakeIdleRoutedMessage(RoutedMessage):
    """
    ServiceMakeIdleRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'ServiceMakeIdleRoutedMessage'

    def __init__(self,
                 send_to):
        """
        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        """
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(ServiceMakeIdleRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, send_to, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`ServiceMakeIdleRoutedMessage` using a dictionary.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`ServiceMakeIdleRoutedMessage`.
        :rtype: ServiceMakeIdleRoutedMessage
        """
        return cls(
            send_to
        )

    @classmethod
    def from_json(cls, send_to, body_json):
        """
        Create a new instance of :class:`ServiceMakeIdleRoutedMessage` using a JSON string.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ServiceMakeIdleRoutedMessage`.
        :rtype: ServiceMakeIdleRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(send_to, body_dict)

    @classmethod
    def from_body_bytes(cls, send_to, body_bytes):
        """
        Create a new instance of :class:`ServiceMakeIdleRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ServiceMakeIdleRoutedMessage`.
        :rtype: ServiceMakeIdleRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(send_to, body_json)

    @classmethod
    def from_message(cls, send_to, message):
        """
        Create a new instance of :class`ServiceMakeIdleRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`ServiceMakeIdleRoutedMessage`.
        :rtype: ServiceMakeIdleRoutedMessage
        """
        instance = cls.from_body_bytes(send_to, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):  # pylint: disable=no-self-use
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        return {
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, send_to, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class ServiceShutdownRoutedMessage(RoutedMessage):
    """
    ServiceShutdownRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'ServiceShutdownRoutedMessage'

    def __init__(self,
                 send_to):
        """
        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        """
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(ServiceShutdownRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, send_to, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`ServiceShutdownRoutedMessage` using a dictionary.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`ServiceShutdownRoutedMessage`.
        :rtype: ServiceShutdownRoutedMessage
        """
        return cls(
            send_to
        )

    @classmethod
    def from_json(cls, send_to, body_json):
        """
        Create a new instance of :class:`ServiceShutdownRoutedMessage` using a JSON string.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ServiceShutdownRoutedMessage`.
        :rtype: ServiceShutdownRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(send_to, body_dict)

    @classmethod
    def from_body_bytes(cls, send_to, body_bytes):
        """
        Create a new instance of :class:`ServiceShutdownRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ServiceShutdownRoutedMessage`.
        :rtype: ServiceShutdownRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(send_to, body_json)

    @classmethod
    def from_message(cls, send_to, message):
        """
        Create a new instance of :class`ServiceShutdownRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`ServiceShutdownRoutedMessage`.
        :rtype: ServiceShutdownRoutedMessage
        """
        instance = cls.from_body_bytes(send_to, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):  # pylint: disable=no-self-use
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        return {
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, send_to, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class ServiceStartedBroadcast(BroadcastMessage):
    """
    ServiceStartedBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'ServiceStartedBroadcast'

    def __init__(self,
                 service_=None,
                 service_reply_to_=None):
        """
        :param service_: service
        :type service_: str
        :param service_reply_to_: service_reply_to
        :type service_reply_to_: str
        """
        self.service = service_
        self.service_reply_to = service_reply_to_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(ServiceStartedBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ServiceStartedBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`ServiceStartedBroadcast`.
        :rtype: ServiceStartedBroadcast
        """
        service_ = _deserialize(body_dict.get('service'), 'str')
        service_reply_to_ = _deserialize(body_dict.get('serviceReplyTo'), 'str')
        return cls(
            service_=service_,
            service_reply_to_=service_reply_to_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ServiceStartedBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ServiceStartedBroadcast`.
        :rtype: ServiceStartedBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ServiceStartedBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ServiceStartedBroadcast`.
        :rtype: ServiceStartedBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`ServiceStartedBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`ServiceStartedBroadcast`.
        :rtype: ServiceStartedBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        service_ = _serialize(self.service)
        service_reply_to_ = _serialize(self.service_reply_to)
        return {
            'service': service_,
            'serviceReplyTo': service_reply_to_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class ServiceStatusBroadcast(BroadcastMessage):
    """
    ServiceStatusBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'ServiceStatusBroadcast'

    def __init__(self,
                 node_name_=None,
                 service_guid_=None,
                 service_name_=None,
                 service_group_name_=None,
                 service_reply_to_=None,
                 service_state_=None):
        """
        :param node_name_: node_name
        :type node_name_: str
        :param service_guid_: service_guid
        :type service_guid_: str
        :param service_name_: service_name
        :type service_name_: str
        :param service_group_name_: service_group_name
        :type service_group_name_: str
        :param service_reply_to_: service_reply_to
        :type service_reply_to_: str
        :param service_state_: service_state
        :type service_state_: ServiceState
        """
        self.node_name = node_name_
        self.service_guid = service_guid_
        self.service_name = service_name_
        self.service_group_name = service_group_name_
        self.service_reply_to = service_reply_to_
        self.service_state = service_state_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(ServiceStatusBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ServiceStatusBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`ServiceStatusBroadcast`.
        :rtype: ServiceStatusBroadcast
        """
        node_name_ = _deserialize(body_dict.get('nodeName'), 'str')
        service_guid_ = _deserialize(body_dict.get('serviceGuid'), 'str')
        service_name_ = _deserialize(body_dict.get('serviceName'), 'str')
        service_group_name_ = _deserialize(body_dict.get('serviceGroupName'), 'str')
        service_reply_to_ = _deserialize(body_dict.get('serviceReplyTo'), 'str')
        service_state_ = _deserialize(body_dict.get('serviceState'), 'ServiceState')
        return cls(
            node_name_=node_name_,
            service_guid_=service_guid_,
            service_name_=service_name_,
            service_group_name_=service_group_name_,
            service_reply_to_=service_reply_to_,
            service_state_=service_state_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ServiceStatusBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ServiceStatusBroadcast`.
        :rtype: ServiceStatusBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ServiceStatusBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ServiceStatusBroadcast`.
        :rtype: ServiceStatusBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`ServiceStatusBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`ServiceStatusBroadcast`.
        :rtype: ServiceStatusBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        node_name_ = _serialize(self.node_name)
        service_guid_ = _serialize(self.service_guid)
        service_name_ = _serialize(self.service_name)
        service_group_name_ = _serialize(self.service_group_name)
        service_reply_to_ = _serialize(self.service_reply_to)
        service_state_ = _serialize(self.service_state)
        return {
            'nodeName': node_name_,
            'serviceGuid': service_guid_,
            'serviceName': service_name_,
            'serviceGroupName': service_group_name_,
            'serviceReplyTo': service_reply_to_,
            'serviceState': service_state_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


#
# ServiceManager service
#


class NodeStatus(object):  # pylint: disable=too-few-public-methods
    """
    NodeStatus normal enum.
    """
    UP_NORMAL = 0
    MISSED_HEARTBEAT = 1
    DEAD = 2
    _INT_TO_STRING = {
        0: 'UP_NORMAL',
        1: 'MISSED_HEARTBEAT',
        2: 'DEAD'
    }
    _STRING_TO_INT = {
        'UP_NORMAL': 0,
        'MISSED_HEARTBEAT': 1,
        'DEAD': 2
    }

    def __init__(self, value):
        """
        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @property
    def value(self):
        """
        Get integer value of the enum.

        :return: The integer value of the enum.
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Set integer value of the enum.

        :param value: The integer value of the enum.
        :type value: int
        """
        self._value = value

    @classmethod
    def from_string(cls, value_string):
        """
        Create a new instance of :class:`NodeStatus` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`NodeStatus`.
        :rtype: NodeStatus
        """
        if value_string is None:
            return None
        value = cls._STRING_TO_INT[value_string]
        return cls(value)

    def to_string(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self._INT_TO_STRING[self._value]

    def __str__(self):
        """
        Returns a string representing the enum.

        :return: A string representing the enum.
        :rtype: str
        """
        return self.to_string()


class DependencyBase(object):
    """
    DependencyBase custom data type.
    """
    def __init__(self,
                 name_=None,
                 version_=None,
                 on_same_node_=None):
        """
        :param name_: name
        :type name_: str
        :param version_: version
        :type version_: str
        :param on_same_node_: on_same_node
        :type on_same_node_: bool
        """
        self.name = name_
        self.version = version_
        self.on_same_node = on_same_node_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`DependencyBase` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`DependencyBase`.
        :rtype: DependencyBase
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        version_ = _deserialize(body_dict.get('version'), 'str')
        on_same_node_ = _deserialize(body_dict.get('onSameNode'), 'bool')
        return cls(
            name_=name_,
            version_=version_,
            on_same_node_=on_same_node_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`DependencyBase` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`DependencyBase`.
        :rtype: DependencyBase
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`DependencyBase` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`DependencyBase`.
        :rtype: DependencyBase
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        name_ = _serialize(self.name)
        version_ = _serialize(self.version)
        on_same_node_ = _serialize(self.on_same_node)
        return {
            'name': name_,
            'version': version_,
            'onSameNode': on_same_node_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')


class ServiceGroup(object):
    """
    ServiceGroup custom data type.
    """
    def __init__(self,
                 name_=None,
                 singleton_=None,
                 default_instance_count_=None,
                 start_mode_=None,
                 environment_variables_=None,
                 properties_=None):
        """
        :param name_: name
        :type name_: str
        :param singleton_: singleton
        :type singleton_: bool
        :param default_instance_count_: default_instance_count
        :type default_instance_count_: int
        :param start_mode_: start_mode
        :type start_mode_: ServiceStartMode
        :param environment_variables_: environment_variables
        :type environment_variables_: dict(str,str)
        :param properties_: properties
        :type properties_: dict(str,str)
        """
        self.name = name_
        self.singleton = singleton_
        self.default_instance_count = default_instance_count_
        self.start_mode = start_mode_
        self.environment_variables = environment_variables_
        self.properties = properties_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ServiceGroup` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ServiceGroup`.
        :rtype: ServiceGroup
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        singleton_ = _deserialize(body_dict.get('singleton'), 'bool')
        default_instance_count_ = _deserialize(body_dict.get('defaultInstanceCount'), 'int')
        start_mode_ = _deserialize(body_dict.get('startMode'), 'ServiceStartMode')
        environment_variables_ = _deserialize(body_dict.get('environmentVariables'), 'dict(str,str)')
        properties_ = _deserialize(body_dict.get('properties'), 'dict(str,str)')
        return cls(
            name_=name_,
            singleton_=singleton_,
            default_instance_count_=default_instance_count_,
            start_mode_=start_mode_,
            environment_variables_=environment_variables_,
            properties_=properties_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ServiceGroup` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ServiceGroup`.
        :rtype: ServiceGroup
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ServiceGroup` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ServiceGroup`.
        :rtype: ServiceGroup
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        name_ = _serialize(self.name)
        singleton_ = _serialize(self.singleton)
        default_instance_count_ = _serialize(self.default_instance_count)
        start_mode_ = _serialize(self.start_mode)
        environment_variables_ = _serialize(self.environment_variables)
        properties_ = _serialize(self.properties)
        return {
            'name': name_,
            'singleton': singleton_,
            'defaultInstanceCount': default_instance_count_,
            'startMode': start_mode_,
            'environmentVariables': environment_variables_,
            'properties': properties_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')


class ServiceDescriptor(object):
    """
    ServiceDescriptor custom data type.
    """
    def __init__(self,
                 name_=None,
                 version_=None,
                 start_type_=None,
                 depends_on_=None,
                 service_groups_=None):
        """
        :param name_: name
        :type name_: str
        :param version_: version
        :type version_: str
        :param start_type_: start_type
        :type start_type_: ServiceStartType
        :param depends_on_: depends_on
        :type depends_on_: list(DependencyBase)
        :param service_groups_: service_groups
        :type service_groups_: list(ServiceGroup)
        """
        self.name = name_
        self.version = version_
        self.start_type = start_type_
        self.depends_on = depends_on_
        self.service_groups = service_groups_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ServiceDescriptor` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ServiceDescriptor`.
        :rtype: ServiceDescriptor
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        version_ = _deserialize(body_dict.get('version'), 'str')
        start_type_ = _deserialize(body_dict.get('startType'), 'ServiceStartType')
        depends_on_ = _deserialize(body_dict.get('dependsOn'), 'list(DependencyBase)')
        service_groups_ = _deserialize(body_dict.get('serviceGroups'), 'list(ServiceGroup)')
        return cls(
            name_=name_,
            version_=version_,
            start_type_=start_type_,
            depends_on_=depends_on_,
            service_groups_=service_groups_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ServiceDescriptor` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ServiceDescriptor`.
        :rtype: ServiceDescriptor
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ServiceDescriptor` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ServiceDescriptor`.
        :rtype: ServiceDescriptor
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        name_ = _serialize(self.name)
        version_ = _serialize(self.version)
        start_type_ = _serialize(self.start_type)
        depends_on_ = _serialize(self.depends_on)
        service_groups_ = _serialize(self.service_groups)
        return {
            'name': name_,
            'version': version_,
            'startType': start_type_,
            'dependsOn': depends_on_,
            'serviceGroups': service_groups_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')


class ServiceInstanceBase(object):
    """
    ServiceInstanceBase custom data type.
    """
    def __init__(self,
                 service_guid_=None,
                 name_=None,
                 version_=None,
                 node_name_=None,
                 service_group_name_=None,
                 service_state_=None,
                 reply_to_queue_=None,
                 service_descriptor_=None,
                 launch_time_=None,
                 stop_time_=None,
                 process_id_=None):
        """
        :param service_guid_: service_guid
        :type service_guid_: str
        :param name_: name
        :type name_: str
        :param version_: version
        :type version_: str
        :param node_name_: node_name
        :type node_name_: str
        :param service_group_name_: service_group_name
        :type service_group_name_: str
        :param service_state_: service_state
        :type service_state_: ServiceState
        :param reply_to_queue_: reply_to_queue
        :type reply_to_queue_: str
        :param service_descriptor_: service_descriptor
        :type service_descriptor_: ServiceDescriptor
        :param launch_time_: launch_time
        :type launch_time_: datetime
        :param stop_time_: stop_time
        :type stop_time_: datetime
        :param process_id_: process_id
        :type process_id_: int
        """
        self.service_guid = service_guid_
        self.name = name_
        self.version = version_
        self.node_name = node_name_
        self.service_group_name = service_group_name_
        self.service_state = service_state_
        self.reply_to_queue = reply_to_queue_
        self.service_descriptor = service_descriptor_
        self.launch_time = launch_time_
        self.stop_time = stop_time_
        self.process_id = process_id_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ServiceInstanceBase` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ServiceInstanceBase`.
        :rtype: ServiceInstanceBase
        """
        service_guid_ = _deserialize(body_dict.get('serviceGuid'), 'str')
        name_ = _deserialize(body_dict.get('name'), 'str')
        version_ = _deserialize(body_dict.get('version'), 'str')
        node_name_ = _deserialize(body_dict.get('nodeName'), 'str')
        service_group_name_ = _deserialize(body_dict.get('serviceGroupName'), 'str')
        service_state_ = _deserialize(body_dict.get('serviceState'), 'ServiceState')
        reply_to_queue_ = _deserialize(body_dict.get('replyToQueue'), 'str')
        service_descriptor_ = _deserialize(body_dict.get('serviceDescriptor'), 'ServiceDescriptor')
        launch_time_ = _deserialize(body_dict.get('launchTime'), 'datetime')
        stop_time_ = _deserialize(body_dict.get('stopTime'), 'datetime')
        process_id_ = _deserialize(body_dict.get('processId'), 'int')
        return cls(
            service_guid_=service_guid_,
            name_=name_,
            version_=version_,
            node_name_=node_name_,
            service_group_name_=service_group_name_,
            service_state_=service_state_,
            reply_to_queue_=reply_to_queue_,
            service_descriptor_=service_descriptor_,
            launch_time_=launch_time_,
            stop_time_=stop_time_,
            process_id_=process_id_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ServiceInstanceBase` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ServiceInstanceBase`.
        :rtype: ServiceInstanceBase
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ServiceInstanceBase` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ServiceInstanceBase`.
        :rtype: ServiceInstanceBase
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        service_guid_ = _serialize(self.service_guid)
        name_ = _serialize(self.name)
        version_ = _serialize(self.version)
        node_name_ = _serialize(self.node_name)
        service_group_name_ = _serialize(self.service_group_name)
        service_state_ = _serialize(self.service_state)
        reply_to_queue_ = _serialize(self.reply_to_queue)
        service_descriptor_ = _serialize(self.service_descriptor)
        launch_time_ = _serialize(self.launch_time)
        stop_time_ = _serialize(self.stop_time)
        process_id_ = _serialize(self.process_id)
        return {
            'serviceGuid': service_guid_,
            'name': name_,
            'version': version_,
            'nodeName': node_name_,
            'serviceGroupName': service_group_name_,
            'serviceState': service_state_,
            'replyToQueue': reply_to_queue_,
            'serviceDescriptor': service_descriptor_,
            'launchTime': launch_time_,
            'stopTime': stop_time_,
            'processId': process_id_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')


class NodeStatusRecord(object):
    """
    NodeStatusRecord custom data type.
    """
    def __init__(self,
                 node_name_=None,
                 status_=None,
                 last_heartbeat_time_=None):
        """
        :param node_name_: node_name
        :type node_name_: str
        :param status_: status
        :type status_: NodeStatus
        :param last_heartbeat_time_: last_heartbeat_time
        :type last_heartbeat_time_: datetime
        """
        self.node_name = node_name_
        self.status = status_
        self.last_heartbeat_time = last_heartbeat_time_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`NodeStatusRecord` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`NodeStatusRecord`.
        :rtype: NodeStatusRecord
        """
        node_name_ = _deserialize(body_dict.get('nodeName'), 'str')
        status_ = _deserialize(body_dict.get('status'), 'NodeStatus')
        last_heartbeat_time_ = _deserialize(body_dict.get('lastHeartbeatTime'), 'datetime')
        return cls(
            node_name_=node_name_,
            status_=status_,
            last_heartbeat_time_=last_heartbeat_time_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`NodeStatusRecord` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`NodeStatusRecord`.
        :rtype: NodeStatusRecord
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`NodeStatusRecord` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`NodeStatusRecord`.
        :rtype: NodeStatusRecord
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        node_name_ = _serialize(self.node_name)
        status_ = _serialize(self.status)
        last_heartbeat_time_ = _serialize(self.last_heartbeat_time)
        return {
            'nodeName': node_name_,
            'status': status_,
            'lastHeartbeatTime': last_heartbeat_time_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')


class SvcMgrHeartbeatBroadcast(BroadcastMessage):
    """
    SvcMgrHeartbeatBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'SvcMgrHeartbeatBroadcast'

    def __init__(self,
                 node_name_=None):
        """
        :param node_name_: node_name
        :type node_name_: str
        """
        self.node_name = node_name_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrHeartbeatBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrHeartbeatBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrHeartbeatBroadcast`.
        :rtype: SvcMgrHeartbeatBroadcast
        """
        node_name_ = _deserialize(body_dict.get('nodeName'), 'str')
        return cls(
            node_name_=node_name_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrHeartbeatBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrHeartbeatBroadcast`.
        :rtype: SvcMgrHeartbeatBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrHeartbeatBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrHeartbeatBroadcast`.
        :rtype: SvcMgrHeartbeatBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrHeartbeatBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrHeartbeatBroadcast`.
        :rtype: SvcMgrHeartbeatBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        node_name_ = _serialize(self.node_name)
        return {
            'nodeName': node_name_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrRunningServiceManagersRequest(RequestMessage):
    """
    SvcMgrRunningServiceManagersRequest JSON request message.
    """
    MESSAGE_NAME = 'SvcMgrRunningServiceManagersRequest'

    def __init__(self):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('ServiceManager', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrRunningServiceManagersRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`SvcMgrRunningServiceManagersRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrRunningServiceManagersRequest`.
        :rtype: SvcMgrRunningServiceManagersRequest
        """
        return cls(
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrRunningServiceManagersRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrRunningServiceManagersRequest`.
        :rtype: SvcMgrRunningServiceManagersRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrRunningServiceManagersRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrRunningServiceManagersRequest`.
        :rtype: SvcMgrRunningServiceManagersRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrRunningServiceManagersRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrRunningServiceManagersRequest`.
        :rtype: SvcMgrRunningServiceManagersRequest
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):  # pylint: disable=no-self-use
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        return {
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrRunningServiceManagersResponse(ResponseMessage):
    """
    SvcMgrRunningServiceManagersResponse JSON response message.
    """
    MESSAGE_NAME = 'SvcMgrRunningServiceManagersResponse'

    def __init__(self,
                 request_message,
                 nodes_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param nodes_: nodes
        :type nodes_: list(NodeStatusRecord)
        """
        self.nodes = nodes_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(SvcMgrRunningServiceManagersResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`SvcMgrRunningServiceManagersResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrRunningServiceManagersResponse`.
        :rtype: SvcMgrRunningServiceManagersResponse
        """
        nodes_ = _deserialize(body_dict.get('nodes'), 'list(NodeStatusRecord)')
        return cls(
            request_message,
            nodes_=nodes_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`SvcMgrRunningServiceManagersResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrRunningServiceManagersResponse`.
        :rtype: SvcMgrRunningServiceManagersResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`SvcMgrRunningServiceManagersResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrRunningServiceManagersResponse`.
        :rtype: SvcMgrRunningServiceManagersResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrRunningServiceManagersResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrRunningServiceManagersResponse`.
        :rtype: SvcMgrRunningServiceManagersResponse
        """
        instance = cls.from_body_bytes(message, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        routing_key = MessageHeader.generate_routing_key(message.reply_to, cls.MESSAGE_NAME)
        instance.routing_key = routing_key
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        nodes_ = _serialize(self.nodes)
        return {
            'nodes': nodes_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_header.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrRegisterLocalServiceRoutedMessage(RoutedMessage):
    """
    SvcMgrRegisterLocalServiceRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'SvcMgrRegisterLocalServiceRoutedMessage'

    def __init__(self,
                 send_to,
                 service_guid_=None,
                 node_name_=None,
                 service_name_=None,
                 service_group_name_=None,
                 reply_to_queue_=None,
                 process_id_=None):
        """
        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param service_guid_: service_guid
        :type service_guid_: str
        :param node_name_: node_name
        :type node_name_: str
        :param service_name_: service_name
        :type service_name_: str
        :param service_group_name_: service_group_name
        :type service_group_name_: str
        :param reply_to_queue_: reply_to_queue
        :type reply_to_queue_: str
        :param process_id_: process_id
        :type process_id_: int
        """
        self.service_guid = service_guid_
        self.node_name = node_name_
        self.service_name = service_name_
        self.service_group_name = service_group_name_
        self.reply_to_queue = reply_to_queue_
        self.process_id = process_id_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrRegisterLocalServiceRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, send_to, body_dict):
        """
        Create a new instance of :class:`SvcMgrRegisterLocalServiceRoutedMessage` using a dictionary.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrRegisterLocalServiceRoutedMessage`.
        :rtype: SvcMgrRegisterLocalServiceRoutedMessage
        """
        service_guid_ = _deserialize(body_dict.get('serviceGuid'), 'str')
        node_name_ = _deserialize(body_dict.get('nodeName'), 'str')
        service_name_ = _deserialize(body_dict.get('serviceName'), 'str')
        service_group_name_ = _deserialize(body_dict.get('serviceGroupName'), 'str')
        reply_to_queue_ = _deserialize(body_dict.get('replyToQueue'), 'str')
        process_id_ = _deserialize(body_dict.get('processId'), 'int')
        return cls(
            send_to,
            service_guid_=service_guid_,
            node_name_=node_name_,
            service_name_=service_name_,
            service_group_name_=service_group_name_,
            reply_to_queue_=reply_to_queue_,
            process_id_=process_id_
        )

    @classmethod
    def from_json(cls, send_to, body_json):
        """
        Create a new instance of :class:`SvcMgrRegisterLocalServiceRoutedMessage` using a JSON string.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrRegisterLocalServiceRoutedMessage`.
        :rtype: SvcMgrRegisterLocalServiceRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(send_to, body_dict)

    @classmethod
    def from_body_bytes(cls, send_to, body_bytes):
        """
        Create a new instance of :class:`SvcMgrRegisterLocalServiceRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrRegisterLocalServiceRoutedMessage`.
        :rtype: SvcMgrRegisterLocalServiceRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(send_to, body_json)

    @classmethod
    def from_message(cls, send_to, message):
        """
        Create a new instance of :class`SvcMgrRegisterLocalServiceRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrRegisterLocalServiceRoutedMessage`.
        :rtype: SvcMgrRegisterLocalServiceRoutedMessage
        """
        instance = cls.from_body_bytes(send_to, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        service_guid_ = _serialize(self.service_guid)
        node_name_ = _serialize(self.node_name)
        service_name_ = _serialize(self.service_name)
        service_group_name_ = _serialize(self.service_group_name)
        reply_to_queue_ = _serialize(self.reply_to_queue)
        process_id_ = _serialize(self.process_id)
        return {
            'serviceGuid': service_guid_,
            'nodeName': node_name_,
            'serviceName': service_name_,
            'serviceGroupName': service_group_name_,
            'replyToQueue': reply_to_queue_,
            'processId': process_id_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, send_to, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrUnavailableLocalServiceRequest(RequestMessage):
    """
    SvcMgrUnavailableLocalServiceRequest JSON request message.
    """
    MESSAGE_NAME = 'SvcMgrUnavailableLocalServiceRequest'

    def __init__(self,
                 service_guid_=None,
                 node_name_=None,
                 service_name_=None,
                 service_group_name_=None,
                 process_id_=None):
        """
        :param service_guid_: service_guid
        :type service_guid_: str
        :param node_name_: node_name
        :type node_name_: str
        :param service_name_: service_name
        :type service_name_: str
        :param service_group_name_: service_group_name
        :type service_group_name_: str
        :param process_id_: process_id
        :type process_id_: int
        """
        self.service_guid = service_guid_
        self.node_name = node_name_
        self.service_name = service_name_
        self.service_group_name = service_group_name_
        self.process_id = process_id_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('ServiceManager', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrUnavailableLocalServiceRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrUnavailableLocalServiceRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrUnavailableLocalServiceRequest`.
        :rtype: SvcMgrUnavailableLocalServiceRequest
        """
        service_guid_ = _deserialize(body_dict.get('serviceGuid'), 'str')
        node_name_ = _deserialize(body_dict.get('nodeName'), 'str')
        service_name_ = _deserialize(body_dict.get('serviceName'), 'str')
        service_group_name_ = _deserialize(body_dict.get('serviceGroupName'), 'str')
        process_id_ = _deserialize(body_dict.get('processId'), 'int')
        return cls(
            service_guid_=service_guid_,
            node_name_=node_name_,
            service_name_=service_name_,
            service_group_name_=service_group_name_,
            process_id_=process_id_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrUnavailableLocalServiceRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrUnavailableLocalServiceRequest`.
        :rtype: SvcMgrUnavailableLocalServiceRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrUnavailableLocalServiceRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrUnavailableLocalServiceRequest`.
        :rtype: SvcMgrUnavailableLocalServiceRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrUnavailableLocalServiceRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrUnavailableLocalServiceRequest`.
        :rtype: SvcMgrUnavailableLocalServiceRequest
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        service_guid_ = _serialize(self.service_guid)
        node_name_ = _serialize(self.node_name)
        service_name_ = _serialize(self.service_name)
        service_group_name_ = _serialize(self.service_group_name)
        process_id_ = _serialize(self.process_id)
        return {
            'serviceGuid': service_guid_,
            'nodeName': node_name_,
            'serviceName': service_name_,
            'serviceGroupName': service_group_name_,
            'processId': process_id_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrUnavailableLocalServiceResponse(ResponseMessage):
    """
    SvcMgrUnavailableLocalServiceResponse JSON response message.
    """
    MESSAGE_NAME = 'SvcMgrUnavailableLocalServiceResponse'

    def __init__(self,
                 request_message):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(SvcMgrUnavailableLocalServiceResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`SvcMgrUnavailableLocalServiceResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrUnavailableLocalServiceResponse`.
        :rtype: SvcMgrUnavailableLocalServiceResponse
        """
        return cls(
            request_message
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`SvcMgrUnavailableLocalServiceResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrUnavailableLocalServiceResponse`.
        :rtype: SvcMgrUnavailableLocalServiceResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`SvcMgrUnavailableLocalServiceResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrUnavailableLocalServiceResponse`.
        :rtype: SvcMgrUnavailableLocalServiceResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrUnavailableLocalServiceResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrUnavailableLocalServiceResponse`.
        :rtype: SvcMgrUnavailableLocalServiceResponse
        """
        instance = cls.from_body_bytes(message, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        routing_key = MessageHeader.generate_routing_key(message.reply_to, cls.MESSAGE_NAME)
        instance.routing_key = routing_key
        return instance

    def to_dict(self):  # pylint: disable=no-self-use
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        return {
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_header.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrSendServiceStatusRequestBroadcast(BroadcastMessage):
    """
    SvcMgrSendServiceStatusRequestBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'SvcMgrSendServiceStatusRequestBroadcast'

    def __init__(self):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrSendServiceStatusRequestBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`SvcMgrSendServiceStatusRequestBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrSendServiceStatusRequestBroadcast`.
        :rtype: SvcMgrSendServiceStatusRequestBroadcast
        """
        return cls(
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrSendServiceStatusRequestBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrSendServiceStatusRequestBroadcast`.
        :rtype: SvcMgrSendServiceStatusRequestBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrSendServiceStatusRequestBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrSendServiceStatusRequestBroadcast`.
        :rtype: SvcMgrSendServiceStatusRequestBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrSendServiceStatusRequestBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrSendServiceStatusRequestBroadcast`.
        :rtype: SvcMgrSendServiceStatusRequestBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):  # pylint: disable=no-self-use
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        return {
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrGetServiceInfoSnapshotRequest(RequestMessage):
    """
    SvcMgrGetServiceInfoSnapshotRequest JSON request message.
    """
    MESSAGE_NAME = 'SvcMgrGetServiceInfoSnapshotRequest'

    def __init__(self):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('ServiceManager', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrGetServiceInfoSnapshotRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`SvcMgrGetServiceInfoSnapshotRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrGetServiceInfoSnapshotRequest`.
        :rtype: SvcMgrGetServiceInfoSnapshotRequest
        """
        return cls(
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrGetServiceInfoSnapshotRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrGetServiceInfoSnapshotRequest`.
        :rtype: SvcMgrGetServiceInfoSnapshotRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrGetServiceInfoSnapshotRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrGetServiceInfoSnapshotRequest`.
        :rtype: SvcMgrGetServiceInfoSnapshotRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrGetServiceInfoSnapshotRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrGetServiceInfoSnapshotRequest`.
        :rtype: SvcMgrGetServiceInfoSnapshotRequest
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):  # pylint: disable=no-self-use
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        return {
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrGetServiceInfoSnapshotResponse(ResponseMessage):
    """
    SvcMgrGetServiceInfoSnapshotResponse JSON response message.
    """
    MESSAGE_NAME = 'SvcMgrGetServiceInfoSnapshotResponse'

    def __init__(self,
                 request_message,
                 services_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param services_: services
        :type services_: list(ServiceInstanceBase)
        """
        self.services = services_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(SvcMgrGetServiceInfoSnapshotResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`SvcMgrGetServiceInfoSnapshotResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrGetServiceInfoSnapshotResponse`.
        :rtype: SvcMgrGetServiceInfoSnapshotResponse
        """
        services_ = _deserialize(body_dict.get('services'), 'list(ServiceInstanceBase)')
        return cls(
            request_message,
            services_=services_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`SvcMgrGetServiceInfoSnapshotResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrGetServiceInfoSnapshotResponse`.
        :rtype: SvcMgrGetServiceInfoSnapshotResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`SvcMgrGetServiceInfoSnapshotResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrGetServiceInfoSnapshotResponse`.
        :rtype: SvcMgrGetServiceInfoSnapshotResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrGetServiceInfoSnapshotResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrGetServiceInfoSnapshotResponse`.
        :rtype: SvcMgrGetServiceInfoSnapshotResponse
        """
        instance = cls.from_body_bytes(message, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        routing_key = MessageHeader.generate_routing_key(message.reply_to, cls.MESSAGE_NAME)
        instance.routing_key = routing_key
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        services_ = _serialize(self.services)
        return {
            'services': services_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_header.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrPurgeStoppedServicesRequestBroadcast(BroadcastMessage):
    """
    SvcMgrPurgeStoppedServicesRequestBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'SvcMgrPurgeStoppedServicesRequestBroadcast'

    def __init__(self):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrPurgeStoppedServicesRequestBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`SvcMgrPurgeStoppedServicesRequestBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrPurgeStoppedServicesRequestBroadcast`.
        :rtype: SvcMgrPurgeStoppedServicesRequestBroadcast
        """
        return cls(
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrPurgeStoppedServicesRequestBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrPurgeStoppedServicesRequestBroadcast`.
        :rtype: SvcMgrPurgeStoppedServicesRequestBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrPurgeStoppedServicesRequestBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrPurgeStoppedServicesRequestBroadcast`.
        :rtype: SvcMgrPurgeStoppedServicesRequestBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrPurgeStoppedServicesRequestBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrPurgeStoppedServicesRequestBroadcast`.
        :rtype: SvcMgrPurgeStoppedServicesRequestBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):  # pylint: disable=no-self-use
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        return {
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrGetActorTreeRequest(RequestMessage):
    """
    SvcMgrGetActorTreeRequest JSON request message.
    """
    MESSAGE_NAME = 'SvcMgrGetActorTreeRequest'

    def __init__(self):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('ServiceManager', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrGetActorTreeRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`SvcMgrGetActorTreeRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrGetActorTreeRequest`.
        :rtype: SvcMgrGetActorTreeRequest
        """
        return cls(
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrGetActorTreeRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrGetActorTreeRequest`.
        :rtype: SvcMgrGetActorTreeRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrGetActorTreeRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrGetActorTreeRequest`.
        :rtype: SvcMgrGetActorTreeRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrGetActorTreeRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrGetActorTreeRequest`.
        :rtype: SvcMgrGetActorTreeRequest
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):  # pylint: disable=no-self-use
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        return {
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrGetActorTreeResponse(ResponseMessage):
    """
    SvcMgrGetActorTreeResponse JSON response message.
    """
    MESSAGE_NAME = 'SvcMgrGetActorTreeResponse'

    def __init__(self,
                 request_message,
                 node_name_=None,
                 actor_list_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param node_name_: node_name
        :type node_name_: str
        :param actor_list_: actor_list
        :type actor_list_: list(str)
        """
        self.node_name = node_name_
        self.actor_list = actor_list_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(SvcMgrGetActorTreeResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`SvcMgrGetActorTreeResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrGetActorTreeResponse`.
        :rtype: SvcMgrGetActorTreeResponse
        """
        node_name_ = _deserialize(body_dict.get('nodeName'), 'str')
        actor_list_ = _deserialize(body_dict.get('actorList'), 'list(str)')
        return cls(
            request_message,
            node_name_=node_name_,
            actor_list_=actor_list_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`SvcMgrGetActorTreeResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrGetActorTreeResponse`.
        :rtype: SvcMgrGetActorTreeResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`SvcMgrGetActorTreeResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrGetActorTreeResponse`.
        :rtype: SvcMgrGetActorTreeResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrGetActorTreeResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrGetActorTreeResponse`.
        :rtype: SvcMgrGetActorTreeResponse
        """
        instance = cls.from_body_bytes(message, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        routing_key = MessageHeader.generate_routing_key(message.reply_to, cls.MESSAGE_NAME)
        instance.routing_key = routing_key
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        node_name_ = _serialize(self.node_name)
        actor_list_ = _serialize(self.actor_list)
        return {
            'nodeName': node_name_,
            'actorList': actor_list_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_header.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrStopOneServiceRoutedMessage(RoutedMessage):
    """
    SvcMgrStopOneServiceRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'SvcMgrStopOneServiceRoutedMessage'

    def __init__(self,
                 send_to,
                 process_id_=None,
                 service_guid_=None,
                 kill_=None):
        """
        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param process_id_: process_id
        :type process_id_: int
        :param service_guid_: service_guid
        :type service_guid_: str
        :param kill_: kill
        :type kill_: bool
        """
        self.process_id = process_id_
        self.service_guid = service_guid_
        self.kill = kill_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrStopOneServiceRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, send_to, body_dict):
        """
        Create a new instance of :class:`SvcMgrStopOneServiceRoutedMessage` using a dictionary.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrStopOneServiceRoutedMessage`.
        :rtype: SvcMgrStopOneServiceRoutedMessage
        """
        process_id_ = _deserialize(body_dict.get('processId'), 'int')
        service_guid_ = _deserialize(body_dict.get('serviceGuid'), 'str')
        kill_ = _deserialize(body_dict.get('kill'), 'bool')
        return cls(
            send_to,
            process_id_=process_id_,
            service_guid_=service_guid_,
            kill_=kill_
        )

    @classmethod
    def from_json(cls, send_to, body_json):
        """
        Create a new instance of :class:`SvcMgrStopOneServiceRoutedMessage` using a JSON string.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrStopOneServiceRoutedMessage`.
        :rtype: SvcMgrStopOneServiceRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(send_to, body_dict)

    @classmethod
    def from_body_bytes(cls, send_to, body_bytes):
        """
        Create a new instance of :class:`SvcMgrStopOneServiceRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrStopOneServiceRoutedMessage`.
        :rtype: SvcMgrStopOneServiceRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(send_to, body_json)

    @classmethod
    def from_message(cls, send_to, message):
        """
        Create a new instance of :class`SvcMgrStopOneServiceRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrStopOneServiceRoutedMessage`.
        :rtype: SvcMgrStopOneServiceRoutedMessage
        """
        instance = cls.from_body_bytes(send_to, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        process_id_ = _serialize(self.process_id)
        service_guid_ = _serialize(self.service_guid)
        kill_ = _serialize(self.kill)
        return {
            'processId': process_id_,
            'serviceGuid': service_guid_,
            'kill': kill_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, send_to, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param send_to: The value to use as a routing parameter.
        :type send_to: str
        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(send_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrStopMultipleServicesBroadcast(BroadcastMessage):
    """
    SvcMgrStopMultipleServicesBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'SvcMgrStopMultipleServicesBroadcast'

    def __init__(self,
                 service_name_=None,
                 node_name_=None,
                 kill_=None):
        """
        :param service_name_: service_name
        :type service_name_: str
        :param node_name_: node_name
        :type node_name_: str
        :param kill_: kill
        :type kill_: bool
        """
        self.service_name = service_name_
        self.node_name = node_name_
        self.kill = kill_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrStopMultipleServicesBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrStopMultipleServicesBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrStopMultipleServicesBroadcast`.
        :rtype: SvcMgrStopMultipleServicesBroadcast
        """
        service_name_ = _deserialize(body_dict.get('serviceName'), 'str')
        node_name_ = _deserialize(body_dict.get('nodeName'), 'str')
        kill_ = _deserialize(body_dict.get('kill'), 'bool')
        return cls(
            service_name_=service_name_,
            node_name_=node_name_,
            kill_=kill_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrStopMultipleServicesBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrStopMultipleServicesBroadcast`.
        :rtype: SvcMgrStopMultipleServicesBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrStopMultipleServicesBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrStopMultipleServicesBroadcast`.
        :rtype: SvcMgrStopMultipleServicesBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrStopMultipleServicesBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrStopMultipleServicesBroadcast`.
        :rtype: SvcMgrStopMultipleServicesBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        service_name_ = _serialize(self.service_name)
        node_name_ = _serialize(self.node_name)
        kill_ = _serialize(self.kill)
        return {
            'serviceName': service_name_,
            'nodeName': node_name_,
            'kill': kill_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrServiceHasShutdownBroadcast(BroadcastMessage):
    """
    SvcMgrServiceHasShutdownBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'SvcMgrServiceHasShutdownBroadcast'

    def __init__(self,
                 service_=None,
                 service_reply_to_=None):
        """
        :param service_: service
        :type service_: str
        :param service_reply_to_: service_reply_to
        :type service_reply_to_: str
        """
        self.service = service_
        self.service_reply_to = service_reply_to_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrServiceHasShutdownBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrServiceHasShutdownBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrServiceHasShutdownBroadcast`.
        :rtype: SvcMgrServiceHasShutdownBroadcast
        """
        service_ = _deserialize(body_dict.get('service'), 'str')
        service_reply_to_ = _deserialize(body_dict.get('serviceReplyTo'), 'str')
        return cls(
            service_=service_,
            service_reply_to_=service_reply_to_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrServiceHasShutdownBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrServiceHasShutdownBroadcast`.
        :rtype: SvcMgrServiceHasShutdownBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrServiceHasShutdownBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrServiceHasShutdownBroadcast`.
        :rtype: SvcMgrServiceHasShutdownBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrServiceHasShutdownBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrServiceHasShutdownBroadcast`.
        :rtype: SvcMgrServiceHasShutdownBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        service_ = _serialize(self.service)
        service_reply_to_ = _serialize(self.service_reply_to)
        return {
            'service': service_,
            'serviceReplyTo': service_reply_to_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrConsoleWriteLineBroadcast(BroadcastMessage):
    """
    SvcMgrConsoleWriteLineBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'SvcMgrConsoleWriteLineBroadcast'

    def __init__(self,
                 console_write_=None):
        """
        :param console_write_: console_write
        :type console_write_: str
        """
        self.console_write = console_write_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrConsoleWriteLineBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrConsoleWriteLineBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrConsoleWriteLineBroadcast`.
        :rtype: SvcMgrConsoleWriteLineBroadcast
        """
        console_write_ = _deserialize(body_dict.get('consoleWrite'), 'str')
        return cls(
            console_write_=console_write_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrConsoleWriteLineBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrConsoleWriteLineBroadcast`.
        :rtype: SvcMgrConsoleWriteLineBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrConsoleWriteLineBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrConsoleWriteLineBroadcast`.
        :rtype: SvcMgrConsoleWriteLineBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrConsoleWriteLineBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrConsoleWriteLineBroadcast`.
        :rtype: SvcMgrConsoleWriteLineBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        console_write_ = _serialize(self.console_write)
        return {
            'consoleWrite': console_write_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrReportServicesRequestBroadcast(BroadcastMessage):
    """
    SvcMgrReportServicesRequestBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'SvcMgrReportServicesRequestBroadcast'

    def __init__(self,
                 requesting_node_name_=None):
        """
        :param requesting_node_name_: requesting_node_name
        :type requesting_node_name_: str
        """
        self.requesting_node_name = requesting_node_name_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrReportServicesRequestBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrReportServicesRequestBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrReportServicesRequestBroadcast`.
        :rtype: SvcMgrReportServicesRequestBroadcast
        """
        requesting_node_name_ = _deserialize(body_dict.get('requestingNodeName'), 'str')
        return cls(
            requesting_node_name_=requesting_node_name_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrReportServicesRequestBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrReportServicesRequestBroadcast`.
        :rtype: SvcMgrReportServicesRequestBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrReportServicesRequestBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrReportServicesRequestBroadcast`.
        :rtype: SvcMgrReportServicesRequestBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrReportServicesRequestBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrReportServicesRequestBroadcast`.
        :rtype: SvcMgrReportServicesRequestBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        requesting_node_name_ = _serialize(self.requesting_node_name)
        return {
            'requestingNodeName': requesting_node_name_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrReportServicesResponseBroadcast(BroadcastMessage):
    """
    SvcMgrReportServicesResponseBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'SvcMgrReportServicesResponseBroadcast'

    def __init__(self,
                 node_name_=None,
                 services_=None):
        """
        :param node_name_: node_name
        :type node_name_: str
        :param services_: services
        :type services_: list(ServiceInstanceBase)
        """
        self.node_name = node_name_
        self.services = services_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrReportServicesResponseBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrReportServicesResponseBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrReportServicesResponseBroadcast`.
        :rtype: SvcMgrReportServicesResponseBroadcast
        """
        node_name_ = _deserialize(body_dict.get('nodeName'), 'str')
        services_ = _deserialize(body_dict.get('services'), 'list(ServiceInstanceBase)')
        return cls(
            node_name_=node_name_,
            services_=services_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrReportServicesResponseBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrReportServicesResponseBroadcast`.
        :rtype: SvcMgrReportServicesResponseBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrReportServicesResponseBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrReportServicesResponseBroadcast`.
        :rtype: SvcMgrReportServicesResponseBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrReportServicesResponseBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrReportServicesResponseBroadcast`.
        :rtype: SvcMgrReportServicesResponseBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        node_name_ = _serialize(self.node_name)
        services_ = _serialize(self.services)
        return {
            'nodeName': node_name_,
            'services': services_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrStartServicesBroadcast(BroadcastMessage):
    """
    SvcMgrStartServicesBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'SvcMgrStartServicesBroadcast'

    def __init__(self,
                 all_nodes_=None,
                 node_names_=None,
                 all_services_=None,
                 service_names_=None,
                 instance_count_=None):
        """
        :param all_nodes_: all_nodes
        :type all_nodes_: bool
        :param node_names_: node_names
        :type node_names_: list(str)
        :param all_services_: all_services
        :type all_services_: bool
        :param service_names_: service_names
        :type service_names_: list(str)
        :param instance_count_: instance_count
        :type instance_count_: int
        """
        self.all_nodes = all_nodes_
        self.node_names = node_names_
        self.all_services = all_services_
        self.service_names = service_names_
        self.instance_count = instance_count_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrStartServicesBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrStartServicesBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrStartServicesBroadcast`.
        :rtype: SvcMgrStartServicesBroadcast
        """
        all_nodes_ = _deserialize(body_dict.get('allNodes'), 'bool')
        node_names_ = _deserialize(body_dict.get('nodeNames'), 'list(str)')
        all_services_ = _deserialize(body_dict.get('allServices'), 'bool')
        service_names_ = _deserialize(body_dict.get('serviceNames'), 'list(str)')
        instance_count_ = _deserialize(body_dict.get('instanceCount'), 'int')
        return cls(
            all_nodes_=all_nodes_,
            node_names_=node_names_,
            all_services_=all_services_,
            service_names_=service_names_,
            instance_count_=instance_count_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrStartServicesBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrStartServicesBroadcast`.
        :rtype: SvcMgrStartServicesBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrStartServicesBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrStartServicesBroadcast`.
        :rtype: SvcMgrStartServicesBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrStartServicesBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrStartServicesBroadcast`.
        :rtype: SvcMgrStartServicesBroadcast
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        all_nodes_ = _serialize(self.all_nodes)
        node_names_ = _serialize(self.node_names)
        all_services_ = _serialize(self.all_services)
        service_names_ = _serialize(self.service_names)
        instance_count_ = _serialize(self.instance_count)
        return {
            'allNodes': all_nodes_,
            'nodeNames': node_names_,
            'allServices': all_services_,
            'serviceNames': service_names_,
            'instanceCount': instance_count_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrGetServiceGroupsRequest(RequestMessage):
    """
    SvcMgrGetServiceGroupsRequest JSON request message.
    """
    MESSAGE_NAME = 'SvcMgrGetServiceGroupsRequest'

    def __init__(self,
                 service_name_=None):
        """
        :param service_name_: service_name
        :type service_name_: str
        """
        self.service_name = service_name_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('ServiceManager', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrGetServiceGroupsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrGetServiceGroupsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrGetServiceGroupsRequest`.
        :rtype: SvcMgrGetServiceGroupsRequest
        """
        service_name_ = _deserialize(body_dict.get('serviceName'), 'str')
        return cls(
            service_name_=service_name_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrGetServiceGroupsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrGetServiceGroupsRequest`.
        :rtype: SvcMgrGetServiceGroupsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrGetServiceGroupsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrGetServiceGroupsRequest`.
        :rtype: SvcMgrGetServiceGroupsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrGetServiceGroupsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrGetServiceGroupsRequest`.
        :rtype: SvcMgrGetServiceGroupsRequest
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        service_name_ = _serialize(self.service_name)
        return {
            'serviceName': service_name_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrGetServiceGroupsResponse(ResponseMessage):
    """
    SvcMgrGetServiceGroupsResponse JSON response message.
    """
    MESSAGE_NAME = 'SvcMgrGetServiceGroupsResponse'

    def __init__(self,
                 request_message,
                 groups_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param groups_: groups
        :type groups_: list(ServiceGroup)
        """
        self.groups = groups_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(SvcMgrGetServiceGroupsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`SvcMgrGetServiceGroupsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrGetServiceGroupsResponse`.
        :rtype: SvcMgrGetServiceGroupsResponse
        """
        groups_ = _deserialize(body_dict.get('groups'), 'list(ServiceGroup)')
        return cls(
            request_message,
            groups_=groups_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`SvcMgrGetServiceGroupsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrGetServiceGroupsResponse`.
        :rtype: SvcMgrGetServiceGroupsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`SvcMgrGetServiceGroupsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrGetServiceGroupsResponse`.
        :rtype: SvcMgrGetServiceGroupsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrGetServiceGroupsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrGetServiceGroupsResponse`.
        :rtype: SvcMgrGetServiceGroupsResponse
        """
        instance = cls.from_body_bytes(message, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        routing_key = MessageHeader.generate_routing_key(message.reply_to, cls.MESSAGE_NAME)
        instance.routing_key = routing_key
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        groups_ = _serialize(self.groups)
        return {
            'groups': groups_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_header.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrUpdateServiceGroupRequest(RequestMessage):
    """
    SvcMgrUpdateServiceGroupRequest JSON request message.
    """
    MESSAGE_NAME = 'SvcMgrUpdateServiceGroupRequest'

    def __init__(self,
                 service_name_=None,
                 group_=None):
        """
        :param service_name_: service_name
        :type service_name_: str
        :param group_: group
        :type group_: ServiceGroup
        """
        self.service_name = service_name_
        self.group = group_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('ServiceManager', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(SvcMgrUpdateServiceGroupRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`SvcMgrUpdateServiceGroupRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrUpdateServiceGroupRequest`.
        :rtype: SvcMgrUpdateServiceGroupRequest
        """
        service_name_ = _deserialize(body_dict.get('serviceName'), 'str')
        group_ = _deserialize(body_dict.get('group'), 'ServiceGroup')
        return cls(
            service_name_=service_name_,
            group_=group_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`SvcMgrUpdateServiceGroupRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrUpdateServiceGroupRequest`.
        :rtype: SvcMgrUpdateServiceGroupRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`SvcMgrUpdateServiceGroupRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrUpdateServiceGroupRequest`.
        :rtype: SvcMgrUpdateServiceGroupRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrUpdateServiceGroupRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrUpdateServiceGroupRequest`.
        :rtype: SvcMgrUpdateServiceGroupRequest
        """
        instance = cls.from_body_bytes(message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        return instance

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        service_name_ = _serialize(self.service_name)
        group_ = _serialize(self.group)
        return {
            'serviceName': service_name_,
            'group': group_
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body


class SvcMgrUpdateServiceGroupResponse(ResponseMessage):
    """
    SvcMgrUpdateServiceGroupResponse JSON response message.
    """
    MESSAGE_NAME = 'SvcMgrUpdateServiceGroupResponse'

    def __init__(self,
                 request_message):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(SvcMgrUpdateServiceGroupResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`SvcMgrUpdateServiceGroupResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`SvcMgrUpdateServiceGroupResponse`.
        :rtype: SvcMgrUpdateServiceGroupResponse
        """
        return cls(
            request_message
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`SvcMgrUpdateServiceGroupResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`SvcMgrUpdateServiceGroupResponse`.
        :rtype: SvcMgrUpdateServiceGroupResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`SvcMgrUpdateServiceGroupResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`SvcMgrUpdateServiceGroupResponse`.
        :rtype: SvcMgrUpdateServiceGroupResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`SvcMgrUpdateServiceGroupResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`SvcMgrUpdateServiceGroupResponse`.
        :rtype: SvcMgrUpdateServiceGroupResponse
        """
        instance = cls.from_body_bytes(message, message.body_bytes)
        instance.correlation_id = message.correlation_id
        instance.reply_to = message.reply_to
        routing_key = MessageHeader.generate_routing_key(message.reply_to, cls.MESSAGE_NAME)
        instance.routing_key = routing_key
        return instance

    def to_dict(self):  # pylint: disable=no-self-use
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        return {
        }

    def to_json(self):
        """
        Returns a JSON string representing the data in this object.

        :return: A JSON string representing the data in this object.
        :rtype: str
        """
        body_dict = self.to_dict()
        return json.dumps(body_dict, separators=(',', ':'))

    def to_body_bytes(self):
        """
        Returns a :class:`bytearray` body representing the data in this object.

        :return: A :class:`bytearray` body representing the data in this object.
        :rtype: bytearray
        """
        body_json = self.to_json()
        return bytearray(body_json, 'utf-8')

    def to_message(self, request_message=None):
        """
        Returns a :class:`systemlink.messagebus.message_base.MessageBase`
        object representing the data in this object.

        :param request_message: Request message if this is a response.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :return: A :class:`systemlink.messagebus.message_base.MessageBase`
            object representing the data in this object.
        :rtype: systemlink.messagebus.message_base.MessageBase
        """
        header = self.header
        if request_message:
            request_header = request_message.header
            header.correlation_id = request_header.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_header.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        body_bytes = self.to_body_bytes()
        return MessageBase(header, body_bytes)

    @property
    def body_bytes(self):
        """
        Returns a :class:`bytes` body representing the data in this object.

        :return: A :class:`bytes` body representing the data in this object.
        :rtype: bytes
        """
        self._body = self.to_body_bytes()  # pylint: disable=attribute-defined-outside-init
        return self._body
