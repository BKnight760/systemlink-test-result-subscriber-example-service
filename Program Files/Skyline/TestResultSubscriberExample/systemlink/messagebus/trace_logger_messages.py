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
# TraceLogger service
#


class LogType(object):  # pylint: disable=too-few-public-methods
    """
    LogType normal enum.
    """
    LOG = 0
    ERROR = 1
    INFO = 2
    _INT_TO_STRING = {
        0: 'LOG',
        1: 'ERROR',
        2: 'INFO'
    }
    _STRING_TO_INT = {
        'LOG': 0,
        'ERROR': 1,
        'INFO': 2
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
        Create a new instance of :class:`LogType` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`LogType`.
        :rtype: LogType
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


class LogEntry(object):
    """
    LogEntry custom data type.
    """
    def __init__(self,
                 module_name_=None,
                 timestamp_=None,
                 trace_point_name_=None,
                 text_=None,
                 type_=None):
        """
        :param module_name_: module_name
        :type module_name_: str
        :param timestamp_: timestamp
        :type timestamp_: datetime
        :param trace_point_name_: trace_point_name
        :type trace_point_name_: str
        :param text_: text
        :type text_: str
        :param type_: type
        :type type_: LogType
        """
        self.module_name = module_name_
        self.timestamp = timestamp_
        self.trace_point_name = trace_point_name_
        self.text = text_
        self.type = type_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`LogEntry` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`LogEntry`.
        :rtype: LogEntry
        """
        module_name_ = _deserialize(body_dict.get('moduleName'), 'str')
        timestamp_ = _deserialize(body_dict.get('timestamp'), 'datetime')
        trace_point_name_ = _deserialize(body_dict.get('tracePointName'), 'str')
        text_ = _deserialize(body_dict.get('text'), 'str')
        type_ = _deserialize(body_dict.get('type'), 'LogType')
        return cls(
            module_name_=module_name_,
            timestamp_=timestamp_,
            trace_point_name_=trace_point_name_,
            text_=text_,
            type_=type_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`LogEntry` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`LogEntry`.
        :rtype: LogEntry
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`LogEntry` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`LogEntry`.
        :rtype: LogEntry
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        module_name_ = _serialize(self.module_name)
        timestamp_ = _serialize(self.timestamp)
        trace_point_name_ = _serialize(self.trace_point_name)
        text_ = _serialize(self.text)
        type_ = _serialize(self.type)
        return {
            'moduleName': module_name_,
            'timestamp': timestamp_,
            'tracePointName': trace_point_name_,
            'text': text_,
            'type': type_
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


class TracePointSetting(object):
    """
    TracePointSetting custom data type.
    """
    def __init__(self,
                 name_=None,
                 enabled_=None,
                 exceptions_=None,
                 times_=None):
        """
        :param name_: name
        :type name_: str
        :param enabled_: enabled
        :type enabled_: bool
        :param exceptions_: exceptions
        :type exceptions_: list(str)
        :param times_: times
        :type times_: str
        """
        self.name = name_
        self.enabled = enabled_
        self.exceptions = exceptions_
        self.times = times_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TracePointSetting` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`TracePointSetting`.
        :rtype: TracePointSetting
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        enabled_ = _deserialize(body_dict.get('enabled'), 'bool')
        exceptions_ = _deserialize(body_dict.get('exceptions'), 'list(str)')
        times_ = _deserialize(body_dict.get('times'), 'str')
        return cls(
            name_=name_,
            enabled_=enabled_,
            exceptions_=exceptions_,
            times_=times_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TracePointSetting` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TracePointSetting`.
        :rtype: TracePointSetting
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TracePointSetting` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TracePointSetting`.
        :rtype: TracePointSetting
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
        enabled_ = _serialize(self.enabled)
        exceptions_ = _serialize(self.exceptions)
        times_ = _serialize(self.times)
        return {
            'name': name_,
            'enabled': enabled_,
            'exceptions': exceptions_,
            'times': times_
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


class TraceLoggerStoreEntriesRoutedMessage(RoutedMessage):
    """
    TraceLoggerStoreEntriesRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'TraceLoggerStoreEntriesRoutedMessage'

    def __init__(self,
                 entries_=None):
        """
        :param entries_: entries
        :type entries_: list(LogEntry)
        """
        self.entries = entries_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TraceLogger', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TraceLoggerStoreEntriesRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TraceLoggerStoreEntriesRoutedMessage` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerStoreEntriesRoutedMessage`.
        :rtype: TraceLoggerStoreEntriesRoutedMessage
        """
        entries_ = _deserialize(body_dict.get('entries'), 'list(LogEntry)')
        return cls(
            entries_=entries_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TraceLoggerStoreEntriesRoutedMessage` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerStoreEntriesRoutedMessage`.
        :rtype: TraceLoggerStoreEntriesRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerStoreEntriesRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerStoreEntriesRoutedMessage`.
        :rtype: TraceLoggerStoreEntriesRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerStoreEntriesRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerStoreEntriesRoutedMessage`.
        :rtype: TraceLoggerStoreEntriesRoutedMessage
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
        entries_ = _serialize(self.entries)
        return {
            'entries': entries_
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


class TraceLoggerRegisterTracePointRoutedMessage(RoutedMessage):
    """
    TraceLoggerRegisterTracePointRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'TraceLoggerRegisterTracePointRoutedMessage'

    def __init__(self,
                 trace_point_name_=None):
        """
        :param trace_point_name_: trace_point_name
        :type trace_point_name_: str
        """
        self.trace_point_name = trace_point_name_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TraceLogger', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TraceLoggerRegisterTracePointRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TraceLoggerRegisterTracePointRoutedMessage` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerRegisterTracePointRoutedMessage`.
        :rtype: TraceLoggerRegisterTracePointRoutedMessage
        """
        trace_point_name_ = _deserialize(body_dict.get('tracePointName'), 'str')
        return cls(
            trace_point_name_=trace_point_name_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TraceLoggerRegisterTracePointRoutedMessage` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerRegisterTracePointRoutedMessage`.
        :rtype: TraceLoggerRegisterTracePointRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerRegisterTracePointRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerRegisterTracePointRoutedMessage`.
        :rtype: TraceLoggerRegisterTracePointRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerRegisterTracePointRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerRegisterTracePointRoutedMessage`.
        :rtype: TraceLoggerRegisterTracePointRoutedMessage
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
        trace_point_name_ = _serialize(self.trace_point_name)
        return {
            'tracePointName': trace_point_name_
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


class TraceLoggerTracePointListRequest(RequestMessage):
    """
    TraceLoggerTracePointListRequest JSON request message.
    """
    MESSAGE_NAME = 'TraceLoggerTracePointListRequest'

    def __init__(self):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TraceLogger', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TraceLoggerTracePointListRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`TraceLoggerTracePointListRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerTracePointListRequest`.
        :rtype: TraceLoggerTracePointListRequest
        """
        return cls(
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TraceLoggerTracePointListRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerTracePointListRequest`.
        :rtype: TraceLoggerTracePointListRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerTracePointListRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerTracePointListRequest`.
        :rtype: TraceLoggerTracePointListRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerTracePointListRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerTracePointListRequest`.
        :rtype: TraceLoggerTracePointListRequest
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


class TraceLoggerTracePointListResponse(ResponseMessage):
    """
    TraceLoggerTracePointListResponse JSON response message.
    """
    MESSAGE_NAME = 'TraceLoggerTracePointListResponse'

    def __init__(self,
                 request_message,
                 settings_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param settings_: settings
        :type settings_: list(TracePointSetting)
        """
        self.settings = settings_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TraceLoggerTracePointListResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TraceLoggerTracePointListResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerTracePointListResponse`.
        :rtype: TraceLoggerTracePointListResponse
        """
        settings_ = _deserialize(body_dict.get('settings'), 'list(TracePointSetting)')
        return cls(
            request_message,
            settings_=settings_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TraceLoggerTracePointListResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerTracePointListResponse`.
        :rtype: TraceLoggerTracePointListResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerTracePointListResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerTracePointListResponse`.
        :rtype: TraceLoggerTracePointListResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerTracePointListResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerTracePointListResponse`.
        :rtype: TraceLoggerTracePointListResponse
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
        settings_ = _serialize(self.settings)
        return {
            'settings': settings_
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


class TraceLoggerCommandRequest(RequestMessage):
    """
    TraceLoggerCommandRequest JSON request message.
    """
    MESSAGE_NAME = 'TraceLoggerCommandRequest'

    def __init__(self,
                 arguments_=None):
        """
        :param arguments_: arguments
        :type arguments_: list(str)
        """
        self.arguments = arguments_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TraceLogger', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TraceLoggerCommandRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TraceLoggerCommandRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerCommandRequest`.
        :rtype: TraceLoggerCommandRequest
        """
        arguments_ = _deserialize(body_dict.get('arguments'), 'list(str)')
        return cls(
            arguments_=arguments_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TraceLoggerCommandRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerCommandRequest`.
        :rtype: TraceLoggerCommandRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerCommandRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerCommandRequest`.
        :rtype: TraceLoggerCommandRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerCommandRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerCommandRequest`.
        :rtype: TraceLoggerCommandRequest
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
        arguments_ = _serialize(self.arguments)
        return {
            'arguments': arguments_
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


class TraceLoggerCommandResponse(ResponseMessage):
    """
    TraceLoggerCommandResponse JSON response message.
    """
    MESSAGE_NAME = 'TraceLoggerCommandResponse'

    def __init__(self,
                 request_message,
                 response_text_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param response_text_: response_text
        :type response_text_: list(str)
        """
        self.response_text = response_text_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TraceLoggerCommandResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TraceLoggerCommandResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerCommandResponse`.
        :rtype: TraceLoggerCommandResponse
        """
        response_text_ = _deserialize(body_dict.get('responseText'), 'list(str)')
        return cls(
            request_message,
            response_text_=response_text_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TraceLoggerCommandResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerCommandResponse`.
        :rtype: TraceLoggerCommandResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerCommandResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerCommandResponse`.
        :rtype: TraceLoggerCommandResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerCommandResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerCommandResponse`.
        :rtype: TraceLoggerCommandResponse
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
        response_text_ = _serialize(self.response_text)
        return {
            'responseText': response_text_
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


class TraceLoggerBroadcastTracePointsRoutedMessage(RoutedMessage):
    """
    TraceLoggerBroadcastTracePointsRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'TraceLoggerBroadcastTracePointsRoutedMessage'

    def __init__(self):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TraceLogger', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TraceLoggerBroadcastTracePointsRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`TraceLoggerBroadcastTracePointsRoutedMessage` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerBroadcastTracePointsRoutedMessage`.
        :rtype: TraceLoggerBroadcastTracePointsRoutedMessage
        """
        return cls(
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TraceLoggerBroadcastTracePointsRoutedMessage` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerBroadcastTracePointsRoutedMessage`.
        :rtype: TraceLoggerBroadcastTracePointsRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerBroadcastTracePointsRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerBroadcastTracePointsRoutedMessage`.
        :rtype: TraceLoggerBroadcastTracePointsRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerBroadcastTracePointsRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerBroadcastTracePointsRoutedMessage`.
        :rtype: TraceLoggerBroadcastTracePointsRoutedMessage
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


class TraceLoggerSnapshotBroadcast(BroadcastMessage):
    """
    TraceLoggerSnapshotBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'TraceLoggerSnapshotBroadcast'

    def __init__(self,
                 settings_=None):
        """
        :param settings_: settings
        :type settings_: list(TracePointSetting)
        """
        self.settings = settings_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TraceLoggerSnapshotBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TraceLoggerSnapshotBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerSnapshotBroadcast`.
        :rtype: TraceLoggerSnapshotBroadcast
        """
        settings_ = _deserialize(body_dict.get('settings'), 'list(TracePointSetting)')
        return cls(
            settings_=settings_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TraceLoggerSnapshotBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerSnapshotBroadcast`.
        :rtype: TraceLoggerSnapshotBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerSnapshotBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerSnapshotBroadcast`.
        :rtype: TraceLoggerSnapshotBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerSnapshotBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerSnapshotBroadcast`.
        :rtype: TraceLoggerSnapshotBroadcast
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
        settings_ = _serialize(self.settings)
        return {
            'settings': settings_
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


class TraceLoggerGetIsCeipEnabledRequest(RequestMessage):
    """
    TraceLoggerGetIsCeipEnabledRequest JSON request message.
    """
    MESSAGE_NAME = 'TraceLoggerGetIsCeipEnabledRequest'

    def __init__(self):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TraceLogger', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TraceLoggerGetIsCeipEnabledRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`TraceLoggerGetIsCeipEnabledRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerGetIsCeipEnabledRequest`.
        :rtype: TraceLoggerGetIsCeipEnabledRequest
        """
        return cls(
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TraceLoggerGetIsCeipEnabledRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerGetIsCeipEnabledRequest`.
        :rtype: TraceLoggerGetIsCeipEnabledRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerGetIsCeipEnabledRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerGetIsCeipEnabledRequest`.
        :rtype: TraceLoggerGetIsCeipEnabledRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerGetIsCeipEnabledRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerGetIsCeipEnabledRequest`.
        :rtype: TraceLoggerGetIsCeipEnabledRequest
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


class TraceLoggerGetIsCeipEnabledResponse(ResponseMessage):
    """
    TraceLoggerGetIsCeipEnabledResponse JSON response message.
    """
    MESSAGE_NAME = 'TraceLoggerGetIsCeipEnabledResponse'

    def __init__(self,
                 request_message,
                 enabled_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param enabled_: enabled
        :type enabled_: bool
        """
        self.enabled = enabled_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TraceLoggerGetIsCeipEnabledResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TraceLoggerGetIsCeipEnabledResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TraceLoggerGetIsCeipEnabledResponse`.
        :rtype: TraceLoggerGetIsCeipEnabledResponse
        """
        enabled_ = _deserialize(body_dict.get('enabled'), 'bool')
        return cls(
            request_message,
            enabled_=enabled_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TraceLoggerGetIsCeipEnabledResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TraceLoggerGetIsCeipEnabledResponse`.
        :rtype: TraceLoggerGetIsCeipEnabledResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TraceLoggerGetIsCeipEnabledResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TraceLoggerGetIsCeipEnabledResponse`.
        :rtype: TraceLoggerGetIsCeipEnabledResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TraceLoggerGetIsCeipEnabledResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TraceLoggerGetIsCeipEnabledResponse`.
        :rtype: TraceLoggerGetIsCeipEnabledResponse
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
        enabled_ = _serialize(self.enabled)
        return {
            'enabled': enabled_
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
