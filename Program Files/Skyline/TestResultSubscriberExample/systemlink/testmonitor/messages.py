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
# TestMonitor service
#


class StatusType(object):  # pylint: disable=too-few-public-methods
    """
    StatusType normal enum.
    """
    LOOPING = 0
    SKIPPED = 1
    CUSTOM = 2
    DONE = 3
    PASSED = 4
    FAILED = 5
    RUNNING = 6
    WAITING = 7
    TERMINATED = 8
    ERRORED = 9
    TIMED_OUT = 10
    _INT_TO_STRING = {
        0: 'LOOPING',
        1: 'SKIPPED',
        2: 'CUSTOM',
        3: 'DONE',
        4: 'PASSED',
        5: 'FAILED',
        6: 'RUNNING',
        7: 'WAITING',
        8: 'TERMINATED',
        9: 'ERRORED',
        10: 'TIMED_OUT'
    }
    _STRING_TO_INT = {
        'LOOPING': 0,
        'SKIPPED': 1,
        'CUSTOM': 2,
        'DONE': 3,
        'PASSED': 4,
        'FAILED': 5,
        'RUNNING': 6,
        'WAITING': 7,
        'TERMINATED': 8,
        'ERRORED': 9,
        'TIMED_OUT': 10
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
        Create a new instance of :class:`StatusType` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`StatusType`.
        :rtype: StatusType
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


class StepField(object):  # pylint: disable=too-few-public-methods
    """
    StepField normal enum.
    """
    NAME = 0
    STEP_TYPE = 1
    STEP_ID = 2
    PARENT_ID = 3
    RESULT_ID = 4
    PATH = 5
    PATH_IDS = 6
    STATUS = 7
    TOTAL_TIME_IN_SECONDS = 8
    STARTED_AT = 9
    UPDATED_AT = 10
    INPUTS = 11
    OUTPUTS = 12
    DATA_MODEL = 13
    DATA = 14
    _INT_TO_STRING = {
        0: 'NAME',
        1: 'STEP_TYPE',
        2: 'STEP_ID',
        3: 'PARENT_ID',
        4: 'RESULT_ID',
        5: 'PATH',
        6: 'PATH_IDS',
        7: 'STATUS',
        8: 'TOTAL_TIME_IN_SECONDS',
        9: 'STARTED_AT',
        10: 'UPDATED_AT',
        11: 'INPUTS',
        12: 'OUTPUTS',
        13: 'DATA_MODEL',
        14: 'DATA'
    }
    _STRING_TO_INT = {
        'NAME': 0,
        'STEP_TYPE': 1,
        'STEP_ID': 2,
        'PARENT_ID': 3,
        'RESULT_ID': 4,
        'PATH': 5,
        'PATH_IDS': 6,
        'STATUS': 7,
        'TOTAL_TIME_IN_SECONDS': 8,
        'STARTED_AT': 9,
        'UPDATED_AT': 10,
        'INPUTS': 11,
        'OUTPUTS': 12,
        'DATA_MODEL': 13,
        'DATA': 14
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
        Create a new instance of :class:`StepField` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`StepField`.
        :rtype: StepField
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


class ResultField(object):  # pylint: disable=too-few-public-methods
    """
    ResultField normal enum.
    """
    ID = 0
    STATUS = 1
    STARTED_AT = 2
    UPDATED_AT = 3
    PROGRAM_NAME = 4
    SYSTEM_ID = 5
    HOST_NAME = 6
    OPERATOR = 7
    SERIAL_NUMBER = 8
    PRODUCT = 9
    TOTAL_TIME_IN_SECONDS = 10
    KEYWORDS = 11
    PROPERTIES = 12
    FILE_IDS = 13
    STATUS_TYPE_SUMMARY = 14
    _INT_TO_STRING = {
        0: 'ID',
        1: 'STATUS',
        2: 'STARTED_AT',
        3: 'UPDATED_AT',
        4: 'PROGRAM_NAME',
        5: 'SYSTEM_ID',
        6: 'HOST_NAME',
        7: 'OPERATOR',
        8: 'SERIAL_NUMBER',
        9: 'PRODUCT',
        10: 'TOTAL_TIME_IN_SECONDS',
        11: 'KEYWORDS',
        12: 'PROPERTIES',
        13: 'FILE_IDS',
        14: 'STATUS_TYPE_SUMMARY'
    }
    _STRING_TO_INT = {
        'ID': 0,
        'STATUS': 1,
        'STARTED_AT': 2,
        'UPDATED_AT': 3,
        'PROGRAM_NAME': 4,
        'SYSTEM_ID': 5,
        'HOST_NAME': 6,
        'OPERATOR': 7,
        'SERIAL_NUMBER': 8,
        'PRODUCT': 9,
        'TOTAL_TIME_IN_SECONDS': 10,
        'KEYWORDS': 11,
        'PROPERTIES': 12,
        'FILE_IDS': 13,
        'STATUS_TYPE_SUMMARY': 14
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
        Create a new instance of :class:`ResultField` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`ResultField`.
        :rtype: ResultField
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


class ProductField(object):  # pylint: disable=too-few-public-methods
    """
    ProductField normal enum.
    """
    ID = 0
    PART_NUMBER = 1
    NAME = 2
    FAMILY = 3
    UPDATED_AT = 4
    KEYWORDS = 5
    PROPERTIES = 6
    FILE_IDS = 7
    _INT_TO_STRING = {
        0: 'ID',
        1: 'PART_NUMBER',
        2: 'NAME',
        3: 'FAMILY',
        4: 'UPDATED_AT',
        5: 'KEYWORDS',
        6: 'PROPERTIES',
        7: 'FILE_IDS'
    }
    _STRING_TO_INT = {
        'ID': 0,
        'PART_NUMBER': 1,
        'NAME': 2,
        'FAMILY': 3,
        'UPDATED_AT': 4,
        'KEYWORDS': 5,
        'PROPERTIES': 6,
        'FILE_IDS': 7
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
        Create a new instance of :class:`ProductField` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`ProductField`.
        :rtype: ProductField
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


class TimeUnit(object):  # pylint: disable=too-few-public-methods
    """
    TimeUnit normal enum.
    """
    DAYS = 0
    HOURS = 1
    MINUTES = 2
    SECONDS = 3
    _INT_TO_STRING = {
        0: 'DAYS',
        1: 'HOURS',
        2: 'MINUTES',
        3: 'SECONDS'
    }
    _STRING_TO_INT = {
        'DAYS': 0,
        'HOURS': 1,
        'MINUTES': 2,
        'SECONDS': 3
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
        Create a new instance of :class:`TimeUnit` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`TimeUnit`.
        :rtype: TimeUnit
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


class QueryOperator(object):  # pylint: disable=too-few-public-methods
    """
    QueryOperator normal enum.
    """
    EQUAL = 0
    NOT_EQUAL = 1
    LESS_THAN = 2
    GREATER_THAN = 3
    LESS_THAN_OR_EQUAL = 4
    GREATER_THAN_OR_EQUAL = 5
    _INT_TO_STRING = {
        0: 'EQUAL',
        1: 'NOT_EQUAL',
        2: 'LESS_THAN',
        3: 'GREATER_THAN',
        4: 'LESS_THAN_OR_EQUAL',
        5: 'GREATER_THAN_OR_EQUAL'
    }
    _STRING_TO_INT = {
        'EQUAL': 0,
        'NOT_EQUAL': 1,
        'LESS_THAN': 2,
        'GREATER_THAN': 3,
        'LESS_THAN_OR_EQUAL': 4,
        'GREATER_THAN_OR_EQUAL': 5
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
        Create a new instance of :class:`QueryOperator` using a string.

        :param value_string: The string value of the enum.
        :type value_string: str
        :return: A new instance of :class:`QueryOperator`.
        :rtype: QueryOperator
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


class NamedValue(object):
    """
    NamedValue custom data type.
    """
    def __init__(self,
                 name_=None,
                 value_=None):
        """
        :param name_: name
        :type name_: str
        :param value_: value
        :type value_: object
        """
        self.name = name_
        self.value = value_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`NamedValue` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`NamedValue`.
        :rtype: NamedValue
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        value_ = _deserialize(body_dict.get('value'), 'object')
        return cls(
            name_=name_,
            value_=value_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`NamedValue` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`NamedValue`.
        :rtype: NamedValue
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`NamedValue` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`NamedValue`.
        :rtype: NamedValue
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
        value_ = _serialize(self.value)
        return {
            'name': name_,
            'value': value_
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


class Status(object):
    """
    Status custom data type.
    """
    def __init__(self,
                 status_type_=None,
                 status_name_=None):
        """
        :param status_type_: status_type
        :type status_type_: StatusType
        :param status_name_: status_name
        :type status_name_: str
        """
        self.status_type = status_type_
        self.status_name = status_name_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`Status` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`Status`.
        :rtype: Status
        """
        status_type_ = _deserialize(body_dict.get('statusType'), 'StatusType')
        status_name_ = _deserialize(body_dict.get('statusName'), 'str')
        return cls(
            status_type_=status_type_,
            status_name_=status_name_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`Status` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`Status`.
        :rtype: Status
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`Status` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`Status`.
        :rtype: Status
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        status_type_ = _serialize(self.status_type)
        status_name_ = _serialize(self.status_name)
        return {
            'statusType': status_type_,
            'statusName': status_name_
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


class StepData(object):
    """
    StepData custom data type.
    """
    def __init__(self,
                 text_=None,
                 parameters_=None):
        """
        :param text_: text
        :type text_: str
        :param parameters_: parameters
        :type parameters_: list(dict(str,str))
        """
        self.text = text_
        self.parameters = parameters_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`StepData` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`StepData`.
        :rtype: StepData
        """
        text_ = _deserialize(body_dict.get('text'), 'str')
        parameters_ = _deserialize(body_dict.get('parameters'), 'list(dict(str,str))')
        return cls(
            text_=text_,
            parameters_=parameters_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`StepData` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`StepData`.
        :rtype: StepData
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`StepData` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`StepData`.
        :rtype: StepData
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        text_ = _serialize(self.text)
        parameters_ = _serialize(self.parameters)
        return {
            'text': text_,
            'parameters': parameters_
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


class AdvancedQueryFilter(object):
    """
    AdvancedQueryFilter custom data type.
    """
    def __init__(self,
                 filter_=None,
                 substitutions_=None):
        """
        :param filter_: filter
        :type filter_: str
        :param substitutions_: substitutions
        :type substitutions_: list(object)
        """
        self.filter = filter_
        self.substitutions = substitutions_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`AdvancedQueryFilter` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`AdvancedQueryFilter`.
        :rtype: AdvancedQueryFilter
        """
        filter_ = _deserialize(body_dict.get('filter'), 'str')
        substitutions_ = _deserialize(body_dict.get('substitutions'), 'list(object)')
        return cls(
            filter_=filter_,
            substitutions_=substitutions_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AdvancedQueryFilter` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AdvancedQueryFilter`.
        :rtype: AdvancedQueryFilter
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AdvancedQueryFilter` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AdvancedQueryFilter`.
        :rtype: AdvancedQueryFilter
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        filter_ = _serialize(self.filter)
        substitutions_ = _serialize(self.substitutions)
        return {
            'filter': filter_,
            'substitutions': substitutions_
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


class StepCreateRequest(object):
    """
    StepCreateRequest custom data type.
    """
    def __init__(self,
                 name_=None,
                 step_type_=None,
                 step_id_=None,
                 parent_id_=None,
                 result_id_=None,
                 status_=None,
                 total_time_in_seconds_=None,
                 started_at_=None,
                 inputs_=None,
                 outputs_=None,
                 data_model_=None,
                 data_=None,
                 children_=None):
        """
        :param name_: name
        :type name_: str
        :param step_type_: step_type
        :type step_type_: str
        :param step_id_: step_id
        :type step_id_: str
        :param parent_id_: parent_id
        :type parent_id_: str
        :param result_id_: result_id
        :type result_id_: str
        :param status_: status
        :type status_: Status
        :param total_time_in_seconds_: total_time_in_seconds
        :type total_time_in_seconds_: float
        :param started_at_: started_at
        :type started_at_: datetime
        :param inputs_: inputs
        :type inputs_: list(NamedValue)
        :param outputs_: outputs
        :type outputs_: list(NamedValue)
        :param data_model_: data_model
        :type data_model_: str
        :param data_: data
        :type data_: StepData
        :param children_: children
        :type children_: list(StepCreateRequest)
        """
        self.name = name_
        self.step_type = step_type_
        self.step_id = step_id_
        self.parent_id = parent_id_
        self.result_id = result_id_
        self.status = status_
        self.total_time_in_seconds = total_time_in_seconds_
        self.started_at = started_at_
        self.inputs = inputs_
        self.outputs = outputs_
        self.data_model = data_model_
        self.data = data_
        self.children = children_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`StepCreateRequest` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`StepCreateRequest`.
        :rtype: StepCreateRequest
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        step_type_ = _deserialize(body_dict.get('stepType'), 'str')
        step_id_ = _deserialize(body_dict.get('stepId'), 'str')
        parent_id_ = _deserialize(body_dict.get('parentId'), 'str')
        result_id_ = _deserialize(body_dict.get('resultId'), 'str')
        status_ = _deserialize(body_dict.get('status'), 'Status')
        total_time_in_seconds_ = _deserialize(body_dict.get('totalTimeInSeconds'), 'float')
        started_at_ = _deserialize(body_dict.get('startedAt'), 'datetime')
        inputs_ = _deserialize(body_dict.get('inputs'), 'list(NamedValue)')
        outputs_ = _deserialize(body_dict.get('outputs'), 'list(NamedValue)')
        data_model_ = _deserialize(body_dict.get('dataModel'), 'str')
        data_ = _deserialize(body_dict.get('data'), 'StepData')
        children_ = _deserialize(body_dict.get('children'), 'list(StepCreateRequest)')
        return cls(
            name_=name_,
            step_type_=step_type_,
            step_id_=step_id_,
            parent_id_=parent_id_,
            result_id_=result_id_,
            status_=status_,
            total_time_in_seconds_=total_time_in_seconds_,
            started_at_=started_at_,
            inputs_=inputs_,
            outputs_=outputs_,
            data_model_=data_model_,
            data_=data_,
            children_=children_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`StepCreateRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`StepCreateRequest`.
        :rtype: StepCreateRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`StepCreateRequest` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`StepCreateRequest`.
        :rtype: StepCreateRequest
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
        step_type_ = _serialize(self.step_type)
        step_id_ = _serialize(self.step_id)
        parent_id_ = _serialize(self.parent_id)
        result_id_ = _serialize(self.result_id)
        status_ = _serialize(self.status)
        total_time_in_seconds_ = _serialize(self.total_time_in_seconds)
        started_at_ = _serialize(self.started_at)
        inputs_ = _serialize(self.inputs)
        outputs_ = _serialize(self.outputs)
        data_model_ = _serialize(self.data_model)
        data_ = _serialize(self.data)
        children_ = _serialize(self.children)
        return {
            'name': name_,
            'stepType': step_type_,
            'stepId': step_id_,
            'parentId': parent_id_,
            'resultId': result_id_,
            'status': status_,
            'totalTimeInSeconds': total_time_in_seconds_,
            'startedAt': started_at_,
            'inputs': inputs_,
            'outputs': outputs_,
            'dataModel': data_model_,
            'data': data_,
            'children': children_
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


class StepUpdateRequest(object):
    """
    StepUpdateRequest custom data type.
    """
    def __init__(self,
                 name_=None,
                 step_type_=None,
                 step_id_=None,
                 result_id_=None,
                 status_=None,
                 total_time_in_seconds_=None,
                 started_at_=None,
                 inputs_=None,
                 outputs_=None,
                 data_model_=None,
                 data_=None):
        """
        :param name_: name
        :type name_: str
        :param step_type_: step_type
        :type step_type_: str
        :param step_id_: step_id
        :type step_id_: str
        :param result_id_: result_id
        :type result_id_: str
        :param status_: status
        :type status_: Status
        :param total_time_in_seconds_: total_time_in_seconds
        :type total_time_in_seconds_: float
        :param started_at_: started_at
        :type started_at_: datetime
        :param inputs_: inputs
        :type inputs_: list(NamedValue)
        :param outputs_: outputs
        :type outputs_: list(NamedValue)
        :param data_model_: data_model
        :type data_model_: str
        :param data_: data
        :type data_: StepData
        """
        self.name = name_
        self.step_type = step_type_
        self.step_id = step_id_
        self.result_id = result_id_
        self.status = status_
        self.total_time_in_seconds = total_time_in_seconds_
        self.started_at = started_at_
        self.inputs = inputs_
        self.outputs = outputs_
        self.data_model = data_model_
        self.data = data_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`StepUpdateRequest` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`StepUpdateRequest`.
        :rtype: StepUpdateRequest
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        step_type_ = _deserialize(body_dict.get('stepType'), 'str')
        step_id_ = _deserialize(body_dict.get('stepId'), 'str')
        result_id_ = _deserialize(body_dict.get('resultId'), 'str')
        status_ = _deserialize(body_dict.get('status'), 'Status')
        total_time_in_seconds_ = _deserialize(body_dict.get('totalTimeInSeconds'), 'float')
        started_at_ = _deserialize(body_dict.get('startedAt'), 'datetime')
        inputs_ = _deserialize(body_dict.get('inputs'), 'list(NamedValue)')
        outputs_ = _deserialize(body_dict.get('outputs'), 'list(NamedValue)')
        data_model_ = _deserialize(body_dict.get('dataModel'), 'str')
        data_ = _deserialize(body_dict.get('data'), 'StepData')
        return cls(
            name_=name_,
            step_type_=step_type_,
            step_id_=step_id_,
            result_id_=result_id_,
            status_=status_,
            total_time_in_seconds_=total_time_in_seconds_,
            started_at_=started_at_,
            inputs_=inputs_,
            outputs_=outputs_,
            data_model_=data_model_,
            data_=data_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`StepUpdateRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`StepUpdateRequest`.
        :rtype: StepUpdateRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`StepUpdateRequest` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`StepUpdateRequest`.
        :rtype: StepUpdateRequest
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
        step_type_ = _serialize(self.step_type)
        step_id_ = _serialize(self.step_id)
        result_id_ = _serialize(self.result_id)
        status_ = _serialize(self.status)
        total_time_in_seconds_ = _serialize(self.total_time_in_seconds)
        started_at_ = _serialize(self.started_at)
        inputs_ = _serialize(self.inputs)
        outputs_ = _serialize(self.outputs)
        data_model_ = _serialize(self.data_model)
        data_ = _serialize(self.data)
        return {
            'name': name_,
            'stepType': step_type_,
            'stepId': step_id_,
            'resultId': result_id_,
            'status': status_,
            'totalTimeInSeconds': total_time_in_seconds_,
            'startedAt': started_at_,
            'inputs': inputs_,
            'outputs': outputs_,
            'dataModel': data_model_,
            'data': data_
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


class StepDeleteRequest(object):
    """
    StepDeleteRequest custom data type.
    """
    def __init__(self,
                 step_id_=None,
                 result_id_=None):
        """
        :param step_id_: step_id
        :type step_id_: str
        :param result_id_: result_id
        :type result_id_: str
        """
        self.step_id = step_id_
        self.result_id = result_id_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`StepDeleteRequest` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`StepDeleteRequest`.
        :rtype: StepDeleteRequest
        """
        step_id_ = _deserialize(body_dict.get('stepId'), 'str')
        result_id_ = _deserialize(body_dict.get('resultId'), 'str')
        return cls(
            step_id_=step_id_,
            result_id_=result_id_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`StepDeleteRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`StepDeleteRequest`.
        :rtype: StepDeleteRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`StepDeleteRequest` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`StepDeleteRequest`.
        :rtype: StepDeleteRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        step_id_ = _serialize(self.step_id)
        result_id_ = _serialize(self.result_id)
        return {
            'stepId': step_id_,
            'resultId': result_id_
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


class StepResponse(object):
    """
    StepResponse custom data type.
    """
    def __init__(self,
                 name_=None,
                 step_type_=None,
                 step_id_=None,
                 parent_id_=None,
                 result_id_=None,
                 path_=None,
                 path_ids_=None,
                 status_=None,
                 total_time_in_seconds_=None,
                 started_at_=None,
                 updated_at_=None,
                 inputs_=None,
                 outputs_=None,
                 data_model_=None,
                 data_=None):
        """
        :param name_: name
        :type name_: str
        :param step_type_: step_type
        :type step_type_: str
        :param step_id_: step_id
        :type step_id_: str
        :param parent_id_: parent_id
        :type parent_id_: str
        :param result_id_: result_id
        :type result_id_: str
        :param path_: path
        :type path_: str
        :param path_ids_: path_ids
        :type path_ids_: list(str)
        :param status_: status
        :type status_: Status
        :param total_time_in_seconds_: total_time_in_seconds
        :type total_time_in_seconds_: float
        :param started_at_: started_at
        :type started_at_: datetime
        :param updated_at_: updated_at
        :type updated_at_: datetime
        :param inputs_: inputs
        :type inputs_: list(NamedValue)
        :param outputs_: outputs
        :type outputs_: list(NamedValue)
        :param data_model_: data_model
        :type data_model_: str
        :param data_: data
        :type data_: StepData
        """
        self.name = name_
        self.step_type = step_type_
        self.step_id = step_id_
        self.parent_id = parent_id_
        self.result_id = result_id_
        self.path = path_
        self.path_ids = path_ids_
        self.status = status_
        self.total_time_in_seconds = total_time_in_seconds_
        self.started_at = started_at_
        self.updated_at = updated_at_
        self.inputs = inputs_
        self.outputs = outputs_
        self.data_model = data_model_
        self.data = data_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`StepResponse` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`StepResponse`.
        :rtype: StepResponse
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        step_type_ = _deserialize(body_dict.get('stepType'), 'str')
        step_id_ = _deserialize(body_dict.get('stepId'), 'str')
        parent_id_ = _deserialize(body_dict.get('parentId'), 'str')
        result_id_ = _deserialize(body_dict.get('resultId'), 'str')
        path_ = _deserialize(body_dict.get('path'), 'str')
        path_ids_ = _deserialize(body_dict.get('pathIds'), 'list(str)')
        status_ = _deserialize(body_dict.get('status'), 'Status')
        total_time_in_seconds_ = _deserialize(body_dict.get('totalTimeInSeconds'), 'float')
        started_at_ = _deserialize(body_dict.get('startedAt'), 'datetime')
        updated_at_ = _deserialize(body_dict.get('updatedAt'), 'datetime')
        inputs_ = _deserialize(body_dict.get('inputs'), 'list(NamedValue)')
        outputs_ = _deserialize(body_dict.get('outputs'), 'list(NamedValue)')
        data_model_ = _deserialize(body_dict.get('dataModel'), 'str')
        data_ = _deserialize(body_dict.get('data'), 'StepData')
        return cls(
            name_=name_,
            step_type_=step_type_,
            step_id_=step_id_,
            parent_id_=parent_id_,
            result_id_=result_id_,
            path_=path_,
            path_ids_=path_ids_,
            status_=status_,
            total_time_in_seconds_=total_time_in_seconds_,
            started_at_=started_at_,
            updated_at_=updated_at_,
            inputs_=inputs_,
            outputs_=outputs_,
            data_model_=data_model_,
            data_=data_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`StepResponse` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`StepResponse`.
        :rtype: StepResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`StepResponse` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`StepResponse`.
        :rtype: StepResponse
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
        step_type_ = _serialize(self.step_type)
        step_id_ = _serialize(self.step_id)
        parent_id_ = _serialize(self.parent_id)
        result_id_ = _serialize(self.result_id)
        path_ = _serialize(self.path)
        path_ids_ = _serialize(self.path_ids)
        status_ = _serialize(self.status)
        total_time_in_seconds_ = _serialize(self.total_time_in_seconds)
        started_at_ = _serialize(self.started_at)
        updated_at_ = _serialize(self.updated_at)
        inputs_ = _serialize(self.inputs)
        outputs_ = _serialize(self.outputs)
        data_model_ = _serialize(self.data_model)
        data_ = _serialize(self.data)
        return {
            'name': name_,
            'stepType': step_type_,
            'stepId': step_id_,
            'parentId': parent_id_,
            'resultId': result_id_,
            'path': path_,
            'pathIds': path_ids_,
            'status': status_,
            'totalTimeInSeconds': total_time_in_seconds_,
            'startedAt': started_at_,
            'updatedAt': updated_at_,
            'inputs': inputs_,
            'outputs': outputs_,
            'dataModel': data_model_,
            'data': data_
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


class DictionaryQuery(object):
    """
    DictionaryQuery custom data type.
    """
    def __init__(self,
                 name_=None,
                 value_=None,
                 operation_=None):
        """
        :param name_: name
        :type name_: str
        :param value_: value
        :type value_: object
        :param operation_: operation
        :type operation_: QueryOperator
        """
        self.name = name_
        self.value = value_
        self.operation = operation_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`DictionaryQuery` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`DictionaryQuery`.
        :rtype: DictionaryQuery
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        value_ = _deserialize(body_dict.get('value'), 'object')
        operation_ = _deserialize(body_dict.get('operation'), 'QueryOperator')
        return cls(
            name_=name_,
            value_=value_,
            operation_=operation_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`DictionaryQuery` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`DictionaryQuery`.
        :rtype: DictionaryQuery
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`DictionaryQuery` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`DictionaryQuery`.
        :rtype: DictionaryQuery
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
        value_ = _serialize(self.value)
        operation_ = _serialize(self.operation)
        return {
            'name': name_,
            'value': value_,
            'operation': operation_
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


class TimeQuery(object):
    """
    TimeQuery custom data type.
    """
    def __init__(self,
                 operation_=None,
                 comparison_value_=None):
        """
        :param operation_: operation
        :type operation_: QueryOperator
        :param comparison_value_: comparison_value
        :type comparison_value_: datetime
        """
        self.operation = operation_
        self.comparison_value = comparison_value_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TimeQuery` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`TimeQuery`.
        :rtype: TimeQuery
        """
        operation_ = _deserialize(body_dict.get('operation'), 'QueryOperator')
        comparison_value_ = _deserialize(body_dict.get('comparisonValue'), 'datetime')
        return cls(
            operation_=operation_,
            comparison_value_=comparison_value_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TimeQuery` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TimeQuery`.
        :rtype: TimeQuery
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TimeQuery` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TimeQuery`.
        :rtype: TimeQuery
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        operation_ = _serialize(self.operation)
        comparison_value_ = _serialize(self.comparison_value)
        return {
            'operation': operation_,
            'comparisonValue': comparison_value_
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


class RelativeTimeQuery(object):
    """
    RelativeTimeQuery custom data type.
    """
    def __init__(self,
                 unit_=None,
                 value_=None):
        """
        :param unit_: unit
        :type unit_: TimeUnit
        :param value_: value
        :type value_: int
        """
        self.unit = unit_
        self.value = value_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`RelativeTimeQuery` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`RelativeTimeQuery`.
        :rtype: RelativeTimeQuery
        """
        unit_ = _deserialize(body_dict.get('unit'), 'TimeUnit')
        value_ = _deserialize(body_dict.get('value'), 'int')
        return cls(
            unit_=unit_,
            value_=value_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`RelativeTimeQuery` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`RelativeTimeQuery`.
        :rtype: RelativeTimeQuery
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`RelativeTimeQuery` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`RelativeTimeQuery`.
        :rtype: RelativeTimeQuery
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        unit_ = _serialize(self.unit)
        value_ = _serialize(self.value)
        return {
            'unit': unit_,
            'value': value_
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


class StepSortDefinition(object):
    """
    StepSortDefinition custom data type.
    """
    def __init__(self,
                 field_=None,
                 order_by_descending_=None):
        """
        :param field_: field
        :type field_: StepField
        :param order_by_descending_: order_by_descending
        :type order_by_descending_: bool
        """
        self.field = field_
        self.order_by_descending = order_by_descending_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`StepSortDefinition` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`StepSortDefinition`.
        :rtype: StepSortDefinition
        """
        field_ = _deserialize(body_dict.get('field'), 'StepField')
        order_by_descending_ = _deserialize(body_dict.get('orderByDescending'), 'bool')
        return cls(
            field_=field_,
            order_by_descending_=order_by_descending_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`StepSortDefinition` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`StepSortDefinition`.
        :rtype: StepSortDefinition
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`StepSortDefinition` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`StepSortDefinition`.
        :rtype: StepSortDefinition
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        field_ = _serialize(self.field)
        order_by_descending_ = _serialize(self.order_by_descending)
        return {
            'field': field_,
            'orderByDescending': order_by_descending_
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


class ResultSortDefinition(object):
    """
    ResultSortDefinition custom data type.
    """
    def __init__(self,
                 field_=None,
                 order_by_descending_=None):
        """
        :param field_: field
        :type field_: ResultField
        :param order_by_descending_: order_by_descending
        :type order_by_descending_: bool
        """
        self.field = field_
        self.order_by_descending = order_by_descending_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ResultSortDefinition` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ResultSortDefinition`.
        :rtype: ResultSortDefinition
        """
        field_ = _deserialize(body_dict.get('field'), 'ResultField')
        order_by_descending_ = _deserialize(body_dict.get('orderByDescending'), 'bool')
        return cls(
            field_=field_,
            order_by_descending_=order_by_descending_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ResultSortDefinition` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ResultSortDefinition`.
        :rtype: ResultSortDefinition
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ResultSortDefinition` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ResultSortDefinition`.
        :rtype: ResultSortDefinition
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        field_ = _serialize(self.field)
        order_by_descending_ = _serialize(self.order_by_descending)
        return {
            'field': field_,
            'orderByDescending': order_by_descending_
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


class ProductSortDefinition(object):
    """
    ProductSortDefinition custom data type.
    """
    def __init__(self,
                 field_=None,
                 order_by_descending_=None):
        """
        :param field_: field
        :type field_: ProductField
        :param order_by_descending_: order_by_descending
        :type order_by_descending_: bool
        """
        self.field = field_
        self.order_by_descending = order_by_descending_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ProductSortDefinition` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ProductSortDefinition`.
        :rtype: ProductSortDefinition
        """
        field_ = _deserialize(body_dict.get('field'), 'ProductField')
        order_by_descending_ = _deserialize(body_dict.get('orderByDescending'), 'bool')
        return cls(
            field_=field_,
            order_by_descending_=order_by_descending_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ProductSortDefinition` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ProductSortDefinition`.
        :rtype: ProductSortDefinition
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ProductSortDefinition` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ProductSortDefinition`.
        :rtype: ProductSortDefinition
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        field_ = _serialize(self.field)
        order_by_descending_ = _serialize(self.order_by_descending)
        return {
            'field': field_,
            'orderByDescending': order_by_descending_
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


class ProductCreateRequest(object):
    """
    ProductCreateRequest custom data type.
    """
    def __init__(self,
                 part_number_=None,
                 name_=None,
                 family_=None,
                 keywords_=None,
                 properties_=None,
                 file_ids_=None):
        """
        :param part_number_: part_number
        :type part_number_: str
        :param name_: name
        :type name_: str
        :param family_: family
        :type family_: str
        :param keywords_: keywords
        :type keywords_: list(str)
        :param properties_: properties
        :type properties_: dict(str,str)
        :param file_ids_: file_ids
        :type file_ids_: list(str)
        """
        self.part_number = part_number_
        self.name = name_
        self.family = family_
        self.keywords = keywords_
        self.properties = properties_
        self.file_ids = file_ids_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ProductCreateRequest` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ProductCreateRequest`.
        :rtype: ProductCreateRequest
        """
        part_number_ = _deserialize(body_dict.get('partNumber'), 'str')
        name_ = _deserialize(body_dict.get('name'), 'str')
        family_ = _deserialize(body_dict.get('family'), 'str')
        keywords_ = _deserialize(body_dict.get('keywords'), 'list(str)')
        properties_ = _deserialize(body_dict.get('properties'), 'dict(str,str)')
        file_ids_ = _deserialize(body_dict.get('fileIds'), 'list(str)')
        return cls(
            part_number_=part_number_,
            name_=name_,
            family_=family_,
            keywords_=keywords_,
            properties_=properties_,
            file_ids_=file_ids_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ProductCreateRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ProductCreateRequest`.
        :rtype: ProductCreateRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ProductCreateRequest` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ProductCreateRequest`.
        :rtype: ProductCreateRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        part_number_ = _serialize(self.part_number)
        name_ = _serialize(self.name)
        family_ = _serialize(self.family)
        keywords_ = _serialize(self.keywords)
        properties_ = _serialize(self.properties)
        file_ids_ = _serialize(self.file_ids)
        return {
            'partNumber': part_number_,
            'name': name_,
            'family': family_,
            'keywords': keywords_,
            'properties': properties_,
            'fileIds': file_ids_
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


class ProductUpdateRequest(object):
    """
    ProductUpdateRequest custom data type.
    """
    def __init__(self,
                 id_=None,
                 name_=None,
                 family_=None,
                 keywords_=None,
                 properties_=None,
                 file_ids_=None):
        """
        :param id_: id
        :type id_: str
        :param name_: name
        :type name_: str
        :param family_: family
        :type family_: str
        :param keywords_: keywords
        :type keywords_: list(str)
        :param properties_: properties
        :type properties_: dict(str,str)
        :param file_ids_: file_ids
        :type file_ids_: list(str)
        """
        self.id = id_  # pylint: disable=invalid-name
        self.name = name_
        self.family = family_
        self.keywords = keywords_
        self.properties = properties_
        self.file_ids = file_ids_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ProductUpdateRequest` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ProductUpdateRequest`.
        :rtype: ProductUpdateRequest
        """
        id_ = _deserialize(body_dict.get('id'), 'str')  # pylint: disable=invalid-name
        name_ = _deserialize(body_dict.get('name'), 'str')
        family_ = _deserialize(body_dict.get('family'), 'str')
        keywords_ = _deserialize(body_dict.get('keywords'), 'list(str)')
        properties_ = _deserialize(body_dict.get('properties'), 'dict(str,str)')
        file_ids_ = _deserialize(body_dict.get('fileIds'), 'list(str)')
        return cls(
            id_=id_,
            name_=name_,
            family_=family_,
            keywords_=keywords_,
            properties_=properties_,
            file_ids_=file_ids_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ProductUpdateRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ProductUpdateRequest`.
        :rtype: ProductUpdateRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ProductUpdateRequest` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ProductUpdateRequest`.
        :rtype: ProductUpdateRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        id_ = _serialize(self.id)  # pylint: disable=invalid-name
        name_ = _serialize(self.name)
        family_ = _serialize(self.family)
        keywords_ = _serialize(self.keywords)
        properties_ = _serialize(self.properties)
        file_ids_ = _serialize(self.file_ids)
        return {
            'id': id_,
            'name': name_,
            'family': family_,
            'keywords': keywords_,
            'properties': properties_,
            'fileIds': file_ids_
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


class ProductResponse(object):
    """
    ProductResponse custom data type.
    """
    def __init__(self,
                 id_=None,
                 part_number_=None,
                 name_=None,
                 family_=None,
                 updated_at_=None,
                 keywords_=None,
                 properties_=None,
                 file_ids_=None):
        """
        :param id_: id
        :type id_: str
        :param part_number_: part_number
        :type part_number_: str
        :param name_: name
        :type name_: str
        :param family_: family
        :type family_: str
        :param updated_at_: updated_at
        :type updated_at_: datetime
        :param keywords_: keywords
        :type keywords_: list(str)
        :param properties_: properties
        :type properties_: dict(str,str)
        :param file_ids_: file_ids
        :type file_ids_: list(str)
        """
        self.id = id_  # pylint: disable=invalid-name
        self.part_number = part_number_
        self.name = name_
        self.family = family_
        self.updated_at = updated_at_
        self.keywords = keywords_
        self.properties = properties_
        self.file_ids = file_ids_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ProductResponse` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ProductResponse`.
        :rtype: ProductResponse
        """
        id_ = _deserialize(body_dict.get('id'), 'str')  # pylint: disable=invalid-name
        part_number_ = _deserialize(body_dict.get('partNumber'), 'str')
        name_ = _deserialize(body_dict.get('name'), 'str')
        family_ = _deserialize(body_dict.get('family'), 'str')
        updated_at_ = _deserialize(body_dict.get('updatedAt'), 'datetime')
        keywords_ = _deserialize(body_dict.get('keywords'), 'list(str)')
        properties_ = _deserialize(body_dict.get('properties'), 'dict(str,str)')
        file_ids_ = _deserialize(body_dict.get('fileIds'), 'list(str)')
        return cls(
            id_=id_,
            part_number_=part_number_,
            name_=name_,
            family_=family_,
            updated_at_=updated_at_,
            keywords_=keywords_,
            properties_=properties_,
            file_ids_=file_ids_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ProductResponse` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ProductResponse`.
        :rtype: ProductResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ProductResponse` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ProductResponse`.
        :rtype: ProductResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        id_ = _serialize(self.id)  # pylint: disable=invalid-name
        part_number_ = _serialize(self.part_number)
        name_ = _serialize(self.name)
        family_ = _serialize(self.family)
        updated_at_ = _serialize(self.updated_at)
        keywords_ = _serialize(self.keywords)
        properties_ = _serialize(self.properties)
        file_ids_ = _serialize(self.file_ids)
        return {
            'id': id_,
            'partNumber': part_number_,
            'name': name_,
            'family': family_,
            'updatedAt': updated_at_,
            'keywords': keywords_,
            'properties': properties_,
            'fileIds': file_ids_
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


class StepQuery(object):
    """
    StepQuery custom data type.
    """
    def __init__(self,
                 names_=None,
                 step_ids_=None,
                 parent_ids_=None,
                 result_ids_=None,
                 path_=None,
                 path_ids_=None,
                 statuses_=None,
                 started_at_query_=None,
                 updated_at_query_=None,
                 sort_by_=None,
                 inputs_=None,
                 outputs_=None):
        """
        :param names_: names
        :type names_: list(str)
        :param step_ids_: step_ids
        :type step_ids_: list(str)
        :param parent_ids_: parent_ids
        :type parent_ids_: list(str)
        :param result_ids_: result_ids
        :type result_ids_: list(str)
        :param path_: path
        :type path_: str
        :param path_ids_: path_ids
        :type path_ids_: list(str)
        :param statuses_: statuses
        :type statuses_: list(Status)
        :param started_at_query_: started_at_query
        :type started_at_query_: list(TimeQuery)
        :param updated_at_query_: updated_at_query
        :type updated_at_query_: list(TimeQuery)
        :param sort_by_: sort_by
        :type sort_by_: list(StepSortDefinition)
        :param inputs_: inputs
        :type inputs_: list(list(DictionaryQuery))
        :param outputs_: outputs
        :type outputs_: list(list(DictionaryQuery))
        """
        self.names = names_
        self.step_ids = step_ids_
        self.parent_ids = parent_ids_
        self.result_ids = result_ids_
        self.path = path_
        self.path_ids = path_ids_
        self.statuses = statuses_
        self.started_at_query = started_at_query_
        self.updated_at_query = updated_at_query_
        self.sort_by = sort_by_
        self.inputs = inputs_
        self.outputs = outputs_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`StepQuery` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`StepQuery`.
        :rtype: StepQuery
        """
        names_ = _deserialize(body_dict.get('names'), 'list(str)')
        step_ids_ = _deserialize(body_dict.get('stepIds'), 'list(str)')
        parent_ids_ = _deserialize(body_dict.get('parentIds'), 'list(str)')
        result_ids_ = _deserialize(body_dict.get('resultIds'), 'list(str)')
        path_ = _deserialize(body_dict.get('path'), 'str')
        path_ids_ = _deserialize(body_dict.get('pathIds'), 'list(str)')
        statuses_ = _deserialize(body_dict.get('statuses'), 'list(Status)')
        started_at_query_ = _deserialize(body_dict.get('startedAtQuery'), 'list(TimeQuery)')
        updated_at_query_ = _deserialize(body_dict.get('updatedAtQuery'), 'list(TimeQuery)')
        sort_by_ = _deserialize(body_dict.get('sortBy'), 'list(StepSortDefinition)')
        inputs_ = _deserialize(body_dict.get('inputs'), 'list(list(DictionaryQuery))')
        outputs_ = _deserialize(body_dict.get('outputs'), 'list(list(DictionaryQuery))')
        return cls(
            names_=names_,
            step_ids_=step_ids_,
            parent_ids_=parent_ids_,
            result_ids_=result_ids_,
            path_=path_,
            path_ids_=path_ids_,
            statuses_=statuses_,
            started_at_query_=started_at_query_,
            updated_at_query_=updated_at_query_,
            sort_by_=sort_by_,
            inputs_=inputs_,
            outputs_=outputs_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`StepQuery` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`StepQuery`.
        :rtype: StepQuery
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`StepQuery` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`StepQuery`.
        :rtype: StepQuery
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        names_ = _serialize(self.names)
        step_ids_ = _serialize(self.step_ids)
        parent_ids_ = _serialize(self.parent_ids)
        result_ids_ = _serialize(self.result_ids)
        path_ = _serialize(self.path)
        path_ids_ = _serialize(self.path_ids)
        statuses_ = _serialize(self.statuses)
        started_at_query_ = _serialize(self.started_at_query)
        updated_at_query_ = _serialize(self.updated_at_query)
        sort_by_ = _serialize(self.sort_by)
        inputs_ = _serialize(self.inputs)
        outputs_ = _serialize(self.outputs)
        return {
            'names': names_,
            'stepIds': step_ids_,
            'parentIds': parent_ids_,
            'resultIds': result_ids_,
            'path': path_,
            'pathIds': path_ids_,
            'statuses': statuses_,
            'startedAtQuery': started_at_query_,
            'updatedAtQuery': updated_at_query_,
            'sortBy': sort_by_,
            'inputs': inputs_,
            'outputs': outputs_
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


class ResultCreateRequest(object):
    """
    ResultCreateRequest custom data type.
    """
    def __init__(self,
                 status_=None,
                 started_at_=None,
                 program_name_=None,
                 system_id_=None,
                 host_name_=None,
                 operator_=None,
                 serial_number_=None,
                 product_=None,
                 total_time_in_seconds_=None,
                 keywords_=None,
                 properties_=None,
                 file_ids_=None):
        """
        :param status_: status
        :type status_: Status
        :param started_at_: started_at
        :type started_at_: datetime
        :param program_name_: program_name
        :type program_name_: str
        :param system_id_: system_id
        :type system_id_: str
        :param host_name_: host_name
        :type host_name_: str
        :param operator_: operator
        :type operator_: str
        :param serial_number_: serial_number
        :type serial_number_: str
        :param product_: product
        :type product_: str
        :param total_time_in_seconds_: total_time_in_seconds
        :type total_time_in_seconds_: float
        :param keywords_: keywords
        :type keywords_: list(str)
        :param properties_: properties
        :type properties_: dict(str,str)
        :param file_ids_: file_ids
        :type file_ids_: list(str)
        """
        self.status = status_
        self.started_at = started_at_
        self.program_name = program_name_
        self.system_id = system_id_
        self.host_name = host_name_
        self.operator = operator_
        self.serial_number = serial_number_
        self.product = product_
        self.total_time_in_seconds = total_time_in_seconds_
        self.keywords = keywords_
        self.properties = properties_
        self.file_ids = file_ids_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ResultCreateRequest` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ResultCreateRequest`.
        :rtype: ResultCreateRequest
        """
        status_ = _deserialize(body_dict.get('status'), 'Status')
        started_at_ = _deserialize(body_dict.get('startedAt'), 'datetime')
        program_name_ = _deserialize(body_dict.get('programName'), 'str')
        system_id_ = _deserialize(body_dict.get('systemId'), 'str')
        host_name_ = _deserialize(body_dict.get('hostName'), 'str')
        operator_ = _deserialize(body_dict.get('operator'), 'str')
        serial_number_ = _deserialize(body_dict.get('serialNumber'), 'str')
        product_ = _deserialize(body_dict.get('product'), 'str')
        total_time_in_seconds_ = _deserialize(body_dict.get('totalTimeInSeconds'), 'float')
        keywords_ = _deserialize(body_dict.get('keywords'), 'list(str)')
        properties_ = _deserialize(body_dict.get('properties'), 'dict(str,str)')
        file_ids_ = _deserialize(body_dict.get('fileIds'), 'list(str)')
        return cls(
            status_=status_,
            started_at_=started_at_,
            program_name_=program_name_,
            system_id_=system_id_,
            host_name_=host_name_,
            operator_=operator_,
            serial_number_=serial_number_,
            product_=product_,
            total_time_in_seconds_=total_time_in_seconds_,
            keywords_=keywords_,
            properties_=properties_,
            file_ids_=file_ids_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ResultCreateRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ResultCreateRequest`.
        :rtype: ResultCreateRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ResultCreateRequest` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ResultCreateRequest`.
        :rtype: ResultCreateRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        status_ = _serialize(self.status)
        started_at_ = _serialize(self.started_at)
        program_name_ = _serialize(self.program_name)
        system_id_ = _serialize(self.system_id)
        host_name_ = _serialize(self.host_name)
        operator_ = _serialize(self.operator)
        serial_number_ = _serialize(self.serial_number)
        product_ = _serialize(self.product)
        total_time_in_seconds_ = _serialize(self.total_time_in_seconds)
        keywords_ = _serialize(self.keywords)
        properties_ = _serialize(self.properties)
        file_ids_ = _serialize(self.file_ids)
        return {
            'status': status_,
            'startedAt': started_at_,
            'programName': program_name_,
            'systemId': system_id_,
            'hostName': host_name_,
            'operator': operator_,
            'serialNumber': serial_number_,
            'product': product_,
            'totalTimeInSeconds': total_time_in_seconds_,
            'keywords': keywords_,
            'properties': properties_,
            'fileIds': file_ids_
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


class ResultUpdateRequest(object):
    """
    ResultUpdateRequest custom data type.
    """
    def __init__(self,
                 status_=None,
                 started_at_=None,
                 program_name_=None,
                 id_=None,
                 system_id_=None,
                 host_name_=None,
                 operator_=None,
                 serial_number_=None,
                 product_=None,
                 total_time_in_seconds_=None,
                 keywords_=None,
                 properties_=None,
                 file_ids_=None):
        """
        :param status_: status
        :type status_: Status
        :param started_at_: started_at
        :type started_at_: datetime
        :param program_name_: program_name
        :type program_name_: str
        :param id_: id
        :type id_: str
        :param system_id_: system_id
        :type system_id_: str
        :param host_name_: host_name
        :type host_name_: str
        :param operator_: operator
        :type operator_: str
        :param serial_number_: serial_number
        :type serial_number_: str
        :param product_: product
        :type product_: str
        :param total_time_in_seconds_: total_time_in_seconds
        :type total_time_in_seconds_: float
        :param keywords_: keywords
        :type keywords_: list(str)
        :param properties_: properties
        :type properties_: dict(str,str)
        :param file_ids_: file_ids
        :type file_ids_: list(str)
        """
        self.status = status_
        self.started_at = started_at_
        self.program_name = program_name_
        self.id = id_  # pylint: disable=invalid-name
        self.system_id = system_id_
        self.host_name = host_name_
        self.operator = operator_
        self.serial_number = serial_number_
        self.product = product_
        self.total_time_in_seconds = total_time_in_seconds_
        self.keywords = keywords_
        self.properties = properties_
        self.file_ids = file_ids_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ResultUpdateRequest` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ResultUpdateRequest`.
        :rtype: ResultUpdateRequest
        """
        status_ = _deserialize(body_dict.get('status'), 'Status')
        started_at_ = _deserialize(body_dict.get('startedAt'), 'datetime')
        program_name_ = _deserialize(body_dict.get('programName'), 'str')
        id_ = _deserialize(body_dict.get('id'), 'str')  # pylint: disable=invalid-name
        system_id_ = _deserialize(body_dict.get('systemId'), 'str')
        host_name_ = _deserialize(body_dict.get('hostName'), 'str')
        operator_ = _deserialize(body_dict.get('operator'), 'str')
        serial_number_ = _deserialize(body_dict.get('serialNumber'), 'str')
        product_ = _deserialize(body_dict.get('product'), 'str')
        total_time_in_seconds_ = _deserialize(body_dict.get('totalTimeInSeconds'), 'float')
        keywords_ = _deserialize(body_dict.get('keywords'), 'list(str)')
        properties_ = _deserialize(body_dict.get('properties'), 'dict(str,str)')
        file_ids_ = _deserialize(body_dict.get('fileIds'), 'list(str)')
        return cls(
            status_=status_,
            started_at_=started_at_,
            program_name_=program_name_,
            id_=id_,
            system_id_=system_id_,
            host_name_=host_name_,
            operator_=operator_,
            serial_number_=serial_number_,
            product_=product_,
            total_time_in_seconds_=total_time_in_seconds_,
            keywords_=keywords_,
            properties_=properties_,
            file_ids_=file_ids_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ResultUpdateRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ResultUpdateRequest`.
        :rtype: ResultUpdateRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ResultUpdateRequest` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ResultUpdateRequest`.
        :rtype: ResultUpdateRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        status_ = _serialize(self.status)
        started_at_ = _serialize(self.started_at)
        program_name_ = _serialize(self.program_name)
        id_ = _serialize(self.id)  # pylint: disable=invalid-name
        system_id_ = _serialize(self.system_id)
        host_name_ = _serialize(self.host_name)
        operator_ = _serialize(self.operator)
        serial_number_ = _serialize(self.serial_number)
        product_ = _serialize(self.product)
        total_time_in_seconds_ = _serialize(self.total_time_in_seconds)
        keywords_ = _serialize(self.keywords)
        properties_ = _serialize(self.properties)
        file_ids_ = _serialize(self.file_ids)
        return {
            'status': status_,
            'startedAt': started_at_,
            'programName': program_name_,
            'id': id_,
            'systemId': system_id_,
            'hostName': host_name_,
            'operator': operator_,
            'serialNumber': serial_number_,
            'product': product_,
            'totalTimeInSeconds': total_time_in_seconds_,
            'keywords': keywords_,
            'properties': properties_,
            'fileIds': file_ids_
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


class ResultResponse(object):
    """
    ResultResponse custom data type.
    """
    def __init__(self,
                 status_=None,
                 started_at_=None,
                 updated_at_=None,
                 program_name_=None,
                 id_=None,
                 system_id_=None,
                 host_name_=None,
                 operator_=None,
                 serial_number_=None,
                 product_=None,
                 total_time_in_seconds_=None,
                 keywords_=None,
                 properties_=None,
                 file_ids_=None,
                 status_type_summary_=None):
        """
        :param status_: status
        :type status_: Status
        :param started_at_: started_at
        :type started_at_: datetime
        :param updated_at_: updated_at
        :type updated_at_: datetime
        :param program_name_: program_name
        :type program_name_: str
        :param id_: id
        :type id_: str
        :param system_id_: system_id
        :type system_id_: str
        :param host_name_: host_name
        :type host_name_: str
        :param operator_: operator
        :type operator_: str
        :param serial_number_: serial_number
        :type serial_number_: str
        :param product_: product
        :type product_: str
        :param total_time_in_seconds_: total_time_in_seconds
        :type total_time_in_seconds_: float
        :param keywords_: keywords
        :type keywords_: list(str)
        :param properties_: properties
        :type properties_: dict(str,str)
        :param file_ids_: file_ids
        :type file_ids_: list(str)
        :param status_type_summary_: status_type_summary
        :type status_type_summary_: dict(StatusType,int)
        """
        self.status = status_
        self.started_at = started_at_
        self.updated_at = updated_at_
        self.program_name = program_name_
        self.id = id_  # pylint: disable=invalid-name
        self.system_id = system_id_
        self.host_name = host_name_
        self.operator = operator_
        self.serial_number = serial_number_
        self.product = product_
        self.total_time_in_seconds = total_time_in_seconds_
        self.keywords = keywords_
        self.properties = properties_
        self.file_ids = file_ids_
        self.status_type_summary = status_type_summary_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ResultResponse` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ResultResponse`.
        :rtype: ResultResponse
        """
        status_ = _deserialize(body_dict.get('status'), 'Status')
        started_at_ = _deserialize(body_dict.get('startedAt'), 'datetime')
        updated_at_ = _deserialize(body_dict.get('updatedAt'), 'datetime')
        program_name_ = _deserialize(body_dict.get('programName'), 'str')
        id_ = _deserialize(body_dict.get('id'), 'str')  # pylint: disable=invalid-name
        system_id_ = _deserialize(body_dict.get('systemId'), 'str')
        host_name_ = _deserialize(body_dict.get('hostName'), 'str')
        operator_ = _deserialize(body_dict.get('operator'), 'str')
        serial_number_ = _deserialize(body_dict.get('serialNumber'), 'str')
        product_ = _deserialize(body_dict.get('product'), 'str')
        total_time_in_seconds_ = _deserialize(body_dict.get('totalTimeInSeconds'), 'float')
        keywords_ = _deserialize(body_dict.get('keywords'), 'list(str)')
        properties_ = _deserialize(body_dict.get('properties'), 'dict(str,str)')
        file_ids_ = _deserialize(body_dict.get('fileIds'), 'list(str)')
        status_type_summary_ = _deserialize(body_dict.get('statusTypeSummary'), 'dict(StatusType,int)')
        return cls(
            status_=status_,
            started_at_=started_at_,
            updated_at_=updated_at_,
            program_name_=program_name_,
            id_=id_,
            system_id_=system_id_,
            host_name_=host_name_,
            operator_=operator_,
            serial_number_=serial_number_,
            product_=product_,
            total_time_in_seconds_=total_time_in_seconds_,
            keywords_=keywords_,
            properties_=properties_,
            file_ids_=file_ids_,
            status_type_summary_=status_type_summary_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ResultResponse` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ResultResponse`.
        :rtype: ResultResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ResultResponse` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ResultResponse`.
        :rtype: ResultResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        status_ = _serialize(self.status)
        started_at_ = _serialize(self.started_at)
        updated_at_ = _serialize(self.updated_at)
        program_name_ = _serialize(self.program_name)
        id_ = _serialize(self.id)  # pylint: disable=invalid-name
        system_id_ = _serialize(self.system_id)
        host_name_ = _serialize(self.host_name)
        operator_ = _serialize(self.operator)
        serial_number_ = _serialize(self.serial_number)
        product_ = _serialize(self.product)
        total_time_in_seconds_ = _serialize(self.total_time_in_seconds)
        keywords_ = _serialize(self.keywords)
        properties_ = _serialize(self.properties)
        file_ids_ = _serialize(self.file_ids)
        status_type_summary_ = _serialize(self.status_type_summary)
        return {
            'status': status_,
            'startedAt': started_at_,
            'updatedAt': updated_at_,
            'programName': program_name_,
            'id': id_,
            'systemId': system_id_,
            'hostName': host_name_,
            'operator': operator_,
            'serialNumber': serial_number_,
            'product': product_,
            'totalTimeInSeconds': total_time_in_seconds_,
            'keywords': keywords_,
            'properties': properties_,
            'fileIds': file_ids_,
            'statusTypeSummary': status_type_summary_
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


class ResultQuery(object):
    """
    ResultQuery custom data type.
    """
    def __init__(self,
                 statuses_=None,
                 started_at_query_=None,
                 updated_at_query_=None,
                 started_within_=None,
                 updated_within_=None,
                 program_names_=None,
                 ids_=None,
                 system_ids_=None,
                 host_names_=None,
                 operators_=None,
                 serial_numbers_=None,
                 products_=None,
                 keywords_=None,
                 properties_=None,
                 file_ids_=None,
                 sort_by_=None):
        """
        :param statuses_: statuses
        :type statuses_: list(Status)
        :param started_at_query_: started_at_query
        :type started_at_query_: list(TimeQuery)
        :param updated_at_query_: updated_at_query
        :type updated_at_query_: list(TimeQuery)
        :param started_within_: started_within
        :type started_within_: RelativeTimeQuery
        :param updated_within_: updated_within
        :type updated_within_: RelativeTimeQuery
        :param program_names_: program_names
        :type program_names_: list(str)
        :param ids_: ids
        :type ids_: list(str)
        :param system_ids_: system_ids
        :type system_ids_: list(str)
        :param host_names_: host_names
        :type host_names_: list(str)
        :param operators_: operators
        :type operators_: list(str)
        :param serial_numbers_: serial_numbers
        :type serial_numbers_: list(str)
        :param products_: products
        :type products_: list(str)
        :param keywords_: keywords
        :type keywords_: list(str)
        :param properties_: properties
        :type properties_: dict(str,str)
        :param file_ids_: file_ids
        :type file_ids_: list(str)
        :param sort_by_: sort_by
        :type sort_by_: list(ResultSortDefinition)
        """
        self.statuses = statuses_
        self.started_at_query = started_at_query_
        self.updated_at_query = updated_at_query_
        self.started_within = started_within_
        self.updated_within = updated_within_
        self.program_names = program_names_
        self.ids = ids_
        self.system_ids = system_ids_
        self.host_names = host_names_
        self.operators = operators_
        self.serial_numbers = serial_numbers_
        self.products = products_
        self.keywords = keywords_
        self.properties = properties_
        self.file_ids = file_ids_
        self.sort_by = sort_by_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ResultQuery` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ResultQuery`.
        :rtype: ResultQuery
        """
        statuses_ = _deserialize(body_dict.get('statuses'), 'list(Status)')
        started_at_query_ = _deserialize(body_dict.get('startedAtQuery'), 'list(TimeQuery)')
        updated_at_query_ = _deserialize(body_dict.get('updatedAtQuery'), 'list(TimeQuery)')
        started_within_ = _deserialize(body_dict.get('startedWithin'), 'RelativeTimeQuery')
        updated_within_ = _deserialize(body_dict.get('updatedWithin'), 'RelativeTimeQuery')
        program_names_ = _deserialize(body_dict.get('programNames'), 'list(str)')
        ids_ = _deserialize(body_dict.get('ids'), 'list(str)')
        system_ids_ = _deserialize(body_dict.get('systemIds'), 'list(str)')
        host_names_ = _deserialize(body_dict.get('hostNames'), 'list(str)')
        operators_ = _deserialize(body_dict.get('operators'), 'list(str)')
        serial_numbers_ = _deserialize(body_dict.get('serialNumbers'), 'list(str)')
        products_ = _deserialize(body_dict.get('products'), 'list(str)')
        keywords_ = _deserialize(body_dict.get('keywords'), 'list(str)')
        properties_ = _deserialize(body_dict.get('properties'), 'dict(str,str)')
        file_ids_ = _deserialize(body_dict.get('fileIds'), 'list(str)')
        sort_by_ = _deserialize(body_dict.get('sortBy'), 'list(ResultSortDefinition)')
        return cls(
            statuses_=statuses_,
            started_at_query_=started_at_query_,
            updated_at_query_=updated_at_query_,
            started_within_=started_within_,
            updated_within_=updated_within_,
            program_names_=program_names_,
            ids_=ids_,
            system_ids_=system_ids_,
            host_names_=host_names_,
            operators_=operators_,
            serial_numbers_=serial_numbers_,
            products_=products_,
            keywords_=keywords_,
            properties_=properties_,
            file_ids_=file_ids_,
            sort_by_=sort_by_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ResultQuery` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ResultQuery`.
        :rtype: ResultQuery
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ResultQuery` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ResultQuery`.
        :rtype: ResultQuery
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        statuses_ = _serialize(self.statuses)
        started_at_query_ = _serialize(self.started_at_query)
        updated_at_query_ = _serialize(self.updated_at_query)
        started_within_ = _serialize(self.started_within)
        updated_within_ = _serialize(self.updated_within)
        program_names_ = _serialize(self.program_names)
        ids_ = _serialize(self.ids)
        system_ids_ = _serialize(self.system_ids)
        host_names_ = _serialize(self.host_names)
        operators_ = _serialize(self.operators)
        serial_numbers_ = _serialize(self.serial_numbers)
        products_ = _serialize(self.products)
        keywords_ = _serialize(self.keywords)
        properties_ = _serialize(self.properties)
        file_ids_ = _serialize(self.file_ids)
        sort_by_ = _serialize(self.sort_by)
        return {
            'statuses': statuses_,
            'startedAtQuery': started_at_query_,
            'updatedAtQuery': updated_at_query_,
            'startedWithin': started_within_,
            'updatedWithin': updated_within_,
            'programNames': program_names_,
            'ids': ids_,
            'systemIds': system_ids_,
            'hostNames': host_names_,
            'operators': operators_,
            'serialNumbers': serial_numbers_,
            'products': products_,
            'keywords': keywords_,
            'properties': properties_,
            'fileIds': file_ids_,
            'sortBy': sort_by_
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


class ErrorEntry(object):
    """
    ErrorEntry custom data type.
    """
    def __init__(self,
                 name_=None,
                 message_=None,
                 args_=None,
                 inner_errors_=None):
        """
        :param name_: name
        :type name_: str
        :param message_: message
        :type message_: str
        :param args_: args
        :type args_: list(str)
        :param inner_errors_: inner_errors
        :type inner_errors_: list(ErrorEntry)
        """
        self.name = name_
        self.message = message_
        self.args = args_
        self.inner_errors = inner_errors_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`ErrorEntry` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`ErrorEntry`.
        :rtype: ErrorEntry
        """
        name_ = _deserialize(body_dict.get('name'), 'str')
        message_ = _deserialize(body_dict.get('message'), 'str')
        args_ = _deserialize(body_dict.get('args'), 'list(str)')
        inner_errors_ = _deserialize(body_dict.get('innerErrors'), 'list(ErrorEntry)')
        return cls(
            name_=name_,
            message_=message_,
            args_=args_,
            inner_errors_=inner_errors_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`ErrorEntry` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`ErrorEntry`.
        :rtype: ErrorEntry
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`ErrorEntry` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`ErrorEntry`.
        :rtype: ErrorEntry
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
        message_ = _serialize(self.message)
        args_ = _serialize(self.args)
        inner_errors_ = _serialize(self.inner_errors)
        return {
            'name': name_,
            'message': message_,
            'args': args_,
            'innerErrors': inner_errors_
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


class TestMonitorCreateProductsRequest(RequestMessage):
    """
    TestMonitorCreateProductsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorCreateProductsRequest'

    def __init__(self,
                 products_=None):
        """
        :param products_: products
        :type products_: list(ProductCreateRequest)
        """
        self.products = products_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorCreateProductsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorCreateProductsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorCreateProductsRequest`.
        :rtype: TestMonitorCreateProductsRequest
        """
        products_ = _deserialize(body_dict.get('products'), 'list(ProductCreateRequest)')
        return cls(
            products_=products_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorCreateProductsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorCreateProductsRequest`.
        :rtype: TestMonitorCreateProductsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorCreateProductsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorCreateProductsRequest`.
        :rtype: TestMonitorCreateProductsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorCreateProductsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorCreateProductsRequest`.
        :rtype: TestMonitorCreateProductsRequest
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
        products_ = _serialize(self.products)
        return {
            'products': products_
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


class TestMonitorCreateProductsResponse(ResponseMessage):
    """
    TestMonitorCreateProductsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorCreateProductsResponse'

    def __init__(self,
                 request_message,
                 products_=None,
                 failed_=None,
                 errors_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param products_: products
        :type products_: list(ProductResponse)
        :param failed_: failed
        :type failed_: list(ProductCreateRequest)
        :param errors_: errors
        :type errors_: ErrorEntry
        """
        self.products = products_
        self.failed = failed_
        self.errors = errors_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorCreateProductsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorCreateProductsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorCreateProductsResponse`.
        :rtype: TestMonitorCreateProductsResponse
        """
        products_ = _deserialize(body_dict.get('products'), 'list(ProductResponse)')
        failed_ = _deserialize(body_dict.get('failed'), 'list(ProductCreateRequest)')
        errors_ = _deserialize(body_dict.get('errors'), 'ErrorEntry')
        return cls(
            request_message,
            products_=products_,
            failed_=failed_,
            errors_=errors_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorCreateProductsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorCreateProductsResponse`.
        :rtype: TestMonitorCreateProductsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorCreateProductsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorCreateProductsResponse`.
        :rtype: TestMonitorCreateProductsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorCreateProductsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorCreateProductsResponse`.
        :rtype: TestMonitorCreateProductsResponse
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
        products_ = _serialize(self.products)
        failed_ = _serialize(self.failed)
        errors_ = _serialize(self.errors)
        return {
            'products': products_,
            'failed': failed_,
            'errors': errors_
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


class TestMonitorUpdateProductsRequest(RequestMessage):
    """
    TestMonitorUpdateProductsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorUpdateProductsRequest'

    def __init__(self,
                 products_=None,
                 replace_=None):
        """
        :param products_: products
        :type products_: list(ProductUpdateRequest)
        :param replace_: replace
        :type replace_: bool
        """
        self.products = products_
        self.replace = replace_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorUpdateProductsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorUpdateProductsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorUpdateProductsRequest`.
        :rtype: TestMonitorUpdateProductsRequest
        """
        products_ = _deserialize(body_dict.get('products'), 'list(ProductUpdateRequest)')
        replace_ = _deserialize(body_dict.get('replace'), 'bool')
        return cls(
            products_=products_,
            replace_=replace_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorUpdateProductsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorUpdateProductsRequest`.
        :rtype: TestMonitorUpdateProductsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorUpdateProductsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorUpdateProductsRequest`.
        :rtype: TestMonitorUpdateProductsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorUpdateProductsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorUpdateProductsRequest`.
        :rtype: TestMonitorUpdateProductsRequest
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
        products_ = _serialize(self.products)
        replace_ = _serialize(self.replace)
        return {
            'products': products_,
            'replace': replace_
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


class TestMonitorUpdateProductsResponse(ResponseMessage):
    """
    TestMonitorUpdateProductsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorUpdateProductsResponse'

    def __init__(self,
                 request_message,
                 products_=None,
                 failed_=None,
                 errors_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param products_: products
        :type products_: list(ProductResponse)
        :param failed_: failed
        :type failed_: list(ProductUpdateRequest)
        :param errors_: errors
        :type errors_: ErrorEntry
        """
        self.products = products_
        self.failed = failed_
        self.errors = errors_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorUpdateProductsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorUpdateProductsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorUpdateProductsResponse`.
        :rtype: TestMonitorUpdateProductsResponse
        """
        products_ = _deserialize(body_dict.get('products'), 'list(ProductResponse)')
        failed_ = _deserialize(body_dict.get('failed'), 'list(ProductUpdateRequest)')
        errors_ = _deserialize(body_dict.get('errors'), 'ErrorEntry')
        return cls(
            request_message,
            products_=products_,
            failed_=failed_,
            errors_=errors_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorUpdateProductsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorUpdateProductsResponse`.
        :rtype: TestMonitorUpdateProductsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorUpdateProductsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorUpdateProductsResponse`.
        :rtype: TestMonitorUpdateProductsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorUpdateProductsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorUpdateProductsResponse`.
        :rtype: TestMonitorUpdateProductsResponse
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
        products_ = _serialize(self.products)
        failed_ = _serialize(self.failed)
        errors_ = _serialize(self.errors)
        return {
            'products': products_,
            'failed': failed_,
            'errors': errors_
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


class TestMonitorDeleteProductsRequest(RequestMessage):
    """
    TestMonitorDeleteProductsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorDeleteProductsRequest'

    def __init__(self,
                 ids_=None):
        """
        :param ids_: ids
        :type ids_: list(str)
        """
        self.ids = ids_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorDeleteProductsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorDeleteProductsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorDeleteProductsRequest`.
        :rtype: TestMonitorDeleteProductsRequest
        """
        ids_ = _deserialize(body_dict.get('ids'), 'list(str)')
        return cls(
            ids_=ids_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorDeleteProductsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorDeleteProductsRequest`.
        :rtype: TestMonitorDeleteProductsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorDeleteProductsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorDeleteProductsRequest`.
        :rtype: TestMonitorDeleteProductsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorDeleteProductsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorDeleteProductsRequest`.
        :rtype: TestMonitorDeleteProductsRequest
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
        ids_ = _serialize(self.ids)
        return {
            'ids': ids_
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


class TestMonitorDeleteProductsResponse(ResponseMessage):
    """
    TestMonitorDeleteProductsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorDeleteProductsResponse'

    def __init__(self,
                 request_message,
                 ids_=None,
                 failed_=None,
                 errors_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param ids_: ids
        :type ids_: list(str)
        :param failed_: failed
        :type failed_: list(str)
        :param errors_: errors
        :type errors_: ErrorEntry
        """
        self.ids = ids_
        self.failed = failed_
        self.errors = errors_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorDeleteProductsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorDeleteProductsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorDeleteProductsResponse`.
        :rtype: TestMonitorDeleteProductsResponse
        """
        ids_ = _deserialize(body_dict.get('ids'), 'list(str)')
        failed_ = _deserialize(body_dict.get('failed'), 'list(str)')
        errors_ = _deserialize(body_dict.get('errors'), 'ErrorEntry')
        return cls(
            request_message,
            ids_=ids_,
            failed_=failed_,
            errors_=errors_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorDeleteProductsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorDeleteProductsResponse`.
        :rtype: TestMonitorDeleteProductsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorDeleteProductsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorDeleteProductsResponse`.
        :rtype: TestMonitorDeleteProductsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorDeleteProductsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorDeleteProductsResponse`.
        :rtype: TestMonitorDeleteProductsResponse
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
        ids_ = _serialize(self.ids)
        failed_ = _serialize(self.failed)
        errors_ = _serialize(self.errors)
        return {
            'ids': ids_,
            'failed': failed_,
            'errors': errors_
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


class TestMonitorQueryProductsV2Request(RequestMessage):
    """
    TestMonitorQueryProductsV2Request JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorQueryProductsV2Request'

    def __init__(self,
                 filter_=None,
                 order_by_=None,
                 projection_=None,
                 skip_=None,
                 take_=None):
        """
        :param filter_: filter
        :type filter_: AdvancedQueryFilter
        :param order_by_: order_by
        :type order_by_: list(ProductSortDefinition)
        :param projection_: projection
        :type projection_: list(ProductField)
        :param skip_: skip
        :type skip_: int
        :param take_: take
        :type take_: int
        """
        self.filter = filter_
        self.order_by = order_by_
        self.projection = projection_
        self.skip = skip_
        self.take = take_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorQueryProductsV2Request, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryProductsV2Request` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryProductsV2Request`.
        :rtype: TestMonitorQueryProductsV2Request
        """
        filter_ = _deserialize(body_dict.get('filter'), 'AdvancedQueryFilter')
        order_by_ = _deserialize(body_dict.get('orderBy'), 'list(ProductSortDefinition)')
        projection_ = _deserialize(body_dict.get('projection'), 'list(ProductField)')
        skip_ = _deserialize(body_dict.get('skip'), 'int')
        take_ = _deserialize(body_dict.get('take'), 'int')
        return cls(
            filter_=filter_,
            order_by_=order_by_,
            projection_=projection_,
            skip_=skip_,
            take_=take_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryProductsV2Request` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryProductsV2Request`.
        :rtype: TestMonitorQueryProductsV2Request
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryProductsV2Request` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryProductsV2Request`.
        :rtype: TestMonitorQueryProductsV2Request
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryProductsV2Request` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryProductsV2Request`.
        :rtype: TestMonitorQueryProductsV2Request
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
        filter_ = _serialize(self.filter)
        order_by_ = _serialize(self.order_by)
        projection_ = _serialize(self.projection)
        skip_ = _serialize(self.skip)
        take_ = _serialize(self.take)
        return {
            'filter': filter_,
            'orderBy': order_by_,
            'projection': projection_,
            'skip': skip_,
            'take': take_
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


class TestMonitorQueryProductsV2Response(ResponseMessage):
    """
    TestMonitorQueryProductsV2Response JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorQueryProductsV2Response'

    def __init__(self,
                 request_message,
                 products_=None,
                 total_count_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param products_: products
        :type products_: list(ProductResponse)
        :param total_count_: total_count
        :type total_count_: long
        """
        self.products = products_
        self.total_count = total_count_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorQueryProductsV2Response, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryProductsV2Response` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryProductsV2Response`.
        :rtype: TestMonitorQueryProductsV2Response
        """
        products_ = _deserialize(body_dict.get('products'), 'list(ProductResponse)')
        total_count_ = _deserialize(body_dict.get('totalCount'), 'long')
        return cls(
            request_message,
            products_=products_,
            total_count_=total_count_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryProductsV2Response` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryProductsV2Response`.
        :rtype: TestMonitorQueryProductsV2Response
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryProductsV2Response` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryProductsV2Response`.
        :rtype: TestMonitorQueryProductsV2Response
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryProductsV2Response` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryProductsV2Response`.
        :rtype: TestMonitorQueryProductsV2Response
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
        products_ = _serialize(self.products)
        total_count_ = _serialize(self.total_count)
        return {
            'products': products_,
            'totalCount': total_count_
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


class TestMonitorCreateTestResultsRequest(RequestMessage):
    """
    TestMonitorCreateTestResultsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorCreateTestResultsRequest'

    def __init__(self,
                 results_=None):
        """
        :param results_: results
        :type results_: list(ResultCreateRequest)
        """
        self.results = results_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorCreateTestResultsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorCreateTestResultsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorCreateTestResultsRequest`.
        :rtype: TestMonitorCreateTestResultsRequest
        """
        results_ = _deserialize(body_dict.get('results'), 'list(ResultCreateRequest)')
        return cls(
            results_=results_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorCreateTestResultsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorCreateTestResultsRequest`.
        :rtype: TestMonitorCreateTestResultsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorCreateTestResultsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorCreateTestResultsRequest`.
        :rtype: TestMonitorCreateTestResultsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorCreateTestResultsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorCreateTestResultsRequest`.
        :rtype: TestMonitorCreateTestResultsRequest
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
        results_ = _serialize(self.results)
        return {
            'results': results_
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


class TestMonitorCreateTestResultsResponse(ResponseMessage):
    """
    TestMonitorCreateTestResultsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorCreateTestResultsResponse'

    def __init__(self,
                 request_message,
                 results_=None,
                 failed_=None,
                 errors_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param results_: results
        :type results_: list(ResultResponse)
        :param failed_: failed
        :type failed_: list(ResultCreateRequest)
        :param errors_: errors
        :type errors_: ErrorEntry
        """
        self.results = results_
        self.failed = failed_
        self.errors = errors_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorCreateTestResultsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorCreateTestResultsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorCreateTestResultsResponse`.
        :rtype: TestMonitorCreateTestResultsResponse
        """
        results_ = _deserialize(body_dict.get('results'), 'list(ResultResponse)')
        failed_ = _deserialize(body_dict.get('failed'), 'list(ResultCreateRequest)')
        errors_ = _deserialize(body_dict.get('errors'), 'ErrorEntry')
        return cls(
            request_message,
            results_=results_,
            failed_=failed_,
            errors_=errors_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorCreateTestResultsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorCreateTestResultsResponse`.
        :rtype: TestMonitorCreateTestResultsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorCreateTestResultsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorCreateTestResultsResponse`.
        :rtype: TestMonitorCreateTestResultsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorCreateTestResultsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorCreateTestResultsResponse`.
        :rtype: TestMonitorCreateTestResultsResponse
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
        results_ = _serialize(self.results)
        failed_ = _serialize(self.failed)
        errors_ = _serialize(self.errors)
        return {
            'results': results_,
            'failed': failed_,
            'errors': errors_
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


class TestMonitorUpdateTestResultsRequest(RequestMessage):
    """
    TestMonitorUpdateTestResultsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorUpdateTestResultsRequest'

    def __init__(self,
                 results_=None,
                 replace_=None,
                 determine_status_from_steps_=None):
        """
        :param results_: results
        :type results_: list(ResultUpdateRequest)
        :param replace_: replace
        :type replace_: bool
        :param determine_status_from_steps_: determine_status_from_steps
        :type determine_status_from_steps_: bool
        """
        self.results = results_
        self.replace = replace_
        self.determine_status_from_steps = determine_status_from_steps_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorUpdateTestResultsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorUpdateTestResultsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorUpdateTestResultsRequest`.
        :rtype: TestMonitorUpdateTestResultsRequest
        """
        results_ = _deserialize(body_dict.get('results'), 'list(ResultUpdateRequest)')
        replace_ = _deserialize(body_dict.get('replace'), 'bool')
        determine_status_from_steps_ = _deserialize(body_dict.get('determineStatusFromSteps'), 'bool')
        return cls(
            results_=results_,
            replace_=replace_,
            determine_status_from_steps_=determine_status_from_steps_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorUpdateTestResultsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorUpdateTestResultsRequest`.
        :rtype: TestMonitorUpdateTestResultsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorUpdateTestResultsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorUpdateTestResultsRequest`.
        :rtype: TestMonitorUpdateTestResultsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorUpdateTestResultsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorUpdateTestResultsRequest`.
        :rtype: TestMonitorUpdateTestResultsRequest
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
        results_ = _serialize(self.results)
        replace_ = _serialize(self.replace)
        determine_status_from_steps_ = _serialize(self.determine_status_from_steps)
        return {
            'results': results_,
            'replace': replace_,
            'determineStatusFromSteps': determine_status_from_steps_
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


class TestMonitorUpdateTestResultsResponse(ResponseMessage):
    """
    TestMonitorUpdateTestResultsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorUpdateTestResultsResponse'

    def __init__(self,
                 request_message,
                 results_=None,
                 failed_=None,
                 errors_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param results_: results
        :type results_: list(ResultResponse)
        :param failed_: failed
        :type failed_: list(ResultUpdateRequest)
        :param errors_: errors
        :type errors_: ErrorEntry
        """
        self.results = results_
        self.failed = failed_
        self.errors = errors_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorUpdateTestResultsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorUpdateTestResultsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorUpdateTestResultsResponse`.
        :rtype: TestMonitorUpdateTestResultsResponse
        """
        results_ = _deserialize(body_dict.get('results'), 'list(ResultResponse)')
        failed_ = _deserialize(body_dict.get('failed'), 'list(ResultUpdateRequest)')
        errors_ = _deserialize(body_dict.get('errors'), 'ErrorEntry')
        return cls(
            request_message,
            results_=results_,
            failed_=failed_,
            errors_=errors_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorUpdateTestResultsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorUpdateTestResultsResponse`.
        :rtype: TestMonitorUpdateTestResultsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorUpdateTestResultsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorUpdateTestResultsResponse`.
        :rtype: TestMonitorUpdateTestResultsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorUpdateTestResultsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorUpdateTestResultsResponse`.
        :rtype: TestMonitorUpdateTestResultsResponse
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
        results_ = _serialize(self.results)
        failed_ = _serialize(self.failed)
        errors_ = _serialize(self.errors)
        return {
            'results': results_,
            'failed': failed_,
            'errors': errors_
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


class TestMonitorDeleteResultsRequest(RequestMessage):
    """
    TestMonitorDeleteResultsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorDeleteResultsRequest'

    def __init__(self,
                 ids_=None,
                 delete_steps_=None):
        """
        :param ids_: ids
        :type ids_: list(str)
        :param delete_steps_: delete_steps
        :type delete_steps_: bool
        """
        self.ids = ids_
        self.delete_steps = delete_steps_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorDeleteResultsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorDeleteResultsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorDeleteResultsRequest`.
        :rtype: TestMonitorDeleteResultsRequest
        """
        ids_ = _deserialize(body_dict.get('ids'), 'list(str)')
        delete_steps_ = _deserialize(body_dict.get('deleteSteps'), 'bool')
        return cls(
            ids_=ids_,
            delete_steps_=delete_steps_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorDeleteResultsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorDeleteResultsRequest`.
        :rtype: TestMonitorDeleteResultsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorDeleteResultsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorDeleteResultsRequest`.
        :rtype: TestMonitorDeleteResultsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorDeleteResultsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorDeleteResultsRequest`.
        :rtype: TestMonitorDeleteResultsRequest
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
        ids_ = _serialize(self.ids)
        delete_steps_ = _serialize(self.delete_steps)
        return {
            'ids': ids_,
            'deleteSteps': delete_steps_
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


class TestMonitorDeleteResultsResponse(ResponseMessage):
    """
    TestMonitorDeleteResultsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorDeleteResultsResponse'

    def __init__(self,
                 request_message,
                 ids_=None,
                 failed_=None,
                 errors_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param ids_: ids
        :type ids_: list(str)
        :param failed_: failed
        :type failed_: list(str)
        :param errors_: errors
        :type errors_: ErrorEntry
        """
        self.ids = ids_
        self.failed = failed_
        self.errors = errors_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorDeleteResultsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorDeleteResultsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorDeleteResultsResponse`.
        :rtype: TestMonitorDeleteResultsResponse
        """
        ids_ = _deserialize(body_dict.get('ids'), 'list(str)')
        failed_ = _deserialize(body_dict.get('failed'), 'list(str)')
        errors_ = _deserialize(body_dict.get('errors'), 'ErrorEntry')
        return cls(
            request_message,
            ids_=ids_,
            failed_=failed_,
            errors_=errors_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorDeleteResultsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorDeleteResultsResponse`.
        :rtype: TestMonitorDeleteResultsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorDeleteResultsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorDeleteResultsResponse`.
        :rtype: TestMonitorDeleteResultsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorDeleteResultsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorDeleteResultsResponse`.
        :rtype: TestMonitorDeleteResultsResponse
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
        ids_ = _serialize(self.ids)
        failed_ = _serialize(self.failed)
        errors_ = _serialize(self.errors)
        return {
            'ids': ids_,
            'failed': failed_,
            'errors': errors_
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


class TestMonitorQueryResultsRequest(RequestMessage):
    """
    TestMonitorQueryResultsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorQueryResultsRequest'

    def __init__(self,
                 query_=None,
                 skip_=None,
                 take_=None):
        """
        :param query_: query
        :type query_: ResultQuery
        :param skip_: skip
        :type skip_: int
        :param take_: take
        :type take_: int
        """
        self.query = query_
        self.skip = skip_
        self.take = take_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorQueryResultsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryResultsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryResultsRequest`.
        :rtype: TestMonitorQueryResultsRequest
        """
        query_ = _deserialize(body_dict.get('query'), 'ResultQuery')
        skip_ = _deserialize(body_dict.get('skip'), 'int')
        take_ = _deserialize(body_dict.get('take'), 'int')
        return cls(
            query_=query_,
            skip_=skip_,
            take_=take_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryResultsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryResultsRequest`.
        :rtype: TestMonitorQueryResultsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryResultsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryResultsRequest`.
        :rtype: TestMonitorQueryResultsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryResultsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryResultsRequest`.
        :rtype: TestMonitorQueryResultsRequest
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
        query_ = _serialize(self.query)
        skip_ = _serialize(self.skip)
        take_ = _serialize(self.take)
        return {
            'query': query_,
            'skip': skip_,
            'take': take_
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


class TestMonitorQueryResultsResponse(ResponseMessage):
    """
    TestMonitorQueryResultsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorQueryResultsResponse'

    def __init__(self,
                 request_message,
                 results_=None,
                 total_count_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param results_: results
        :type results_: list(ResultResponse)
        :param total_count_: total_count
        :type total_count_: int
        """
        self.results = results_
        self.total_count = total_count_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorQueryResultsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryResultsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryResultsResponse`.
        :rtype: TestMonitorQueryResultsResponse
        """
        results_ = _deserialize(body_dict.get('results'), 'list(ResultResponse)')
        total_count_ = _deserialize(body_dict.get('totalCount'), 'int')
        return cls(
            request_message,
            results_=results_,
            total_count_=total_count_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryResultsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryResultsResponse`.
        :rtype: TestMonitorQueryResultsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryResultsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryResultsResponse`.
        :rtype: TestMonitorQueryResultsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryResultsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryResultsResponse`.
        :rtype: TestMonitorQueryResultsResponse
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
        results_ = _serialize(self.results)
        total_count_ = _serialize(self.total_count)
        return {
            'results': results_,
            'totalCount': total_count_
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


class TestMonitorQueryResultsV2Request(RequestMessage):
    """
    TestMonitorQueryResultsV2Request JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorQueryResultsV2Request'

    def __init__(self,
                 filter_=None,
                 order_by_=None,
                 projection_=None,
                 skip_=None,
                 take_=None):
        """
        :param filter_: filter
        :type filter_: AdvancedQueryFilter
        :param order_by_: order_by
        :type order_by_: list(ResultSortDefinition)
        :param projection_: projection
        :type projection_: list(ResultField)
        :param skip_: skip
        :type skip_: int
        :param take_: take
        :type take_: int
        """
        self.filter = filter_
        self.order_by = order_by_
        self.projection = projection_
        self.skip = skip_
        self.take = take_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorQueryResultsV2Request, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryResultsV2Request` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryResultsV2Request`.
        :rtype: TestMonitorQueryResultsV2Request
        """
        filter_ = _deserialize(body_dict.get('filter'), 'AdvancedQueryFilter')
        order_by_ = _deserialize(body_dict.get('orderBy'), 'list(ResultSortDefinition)')
        projection_ = _deserialize(body_dict.get('projection'), 'list(ResultField)')
        skip_ = _deserialize(body_dict.get('skip'), 'int')
        take_ = _deserialize(body_dict.get('take'), 'int')
        return cls(
            filter_=filter_,
            order_by_=order_by_,
            projection_=projection_,
            skip_=skip_,
            take_=take_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryResultsV2Request` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryResultsV2Request`.
        :rtype: TestMonitorQueryResultsV2Request
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryResultsV2Request` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryResultsV2Request`.
        :rtype: TestMonitorQueryResultsV2Request
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryResultsV2Request` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryResultsV2Request`.
        :rtype: TestMonitorQueryResultsV2Request
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
        filter_ = _serialize(self.filter)
        order_by_ = _serialize(self.order_by)
        projection_ = _serialize(self.projection)
        skip_ = _serialize(self.skip)
        take_ = _serialize(self.take)
        return {
            'filter': filter_,
            'orderBy': order_by_,
            'projection': projection_,
            'skip': skip_,
            'take': take_
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


class TestMonitorQueryResultsV2Response(ResponseMessage):
    """
    TestMonitorQueryResultsV2Response JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorQueryResultsV2Response'

    def __init__(self,
                 request_message,
                 results_=None,
                 total_count_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param results_: results
        :type results_: list(ResultResponse)
        :param total_count_: total_count
        :type total_count_: long
        """
        self.results = results_
        self.total_count = total_count_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorQueryResultsV2Response, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryResultsV2Response` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryResultsV2Response`.
        :rtype: TestMonitorQueryResultsV2Response
        """
        results_ = _deserialize(body_dict.get('results'), 'list(ResultResponse)')
        total_count_ = _deserialize(body_dict.get('totalCount'), 'long')
        return cls(
            request_message,
            results_=results_,
            total_count_=total_count_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryResultsV2Response` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryResultsV2Response`.
        :rtype: TestMonitorQueryResultsV2Response
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryResultsV2Response` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryResultsV2Response`.
        :rtype: TestMonitorQueryResultsV2Response
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryResultsV2Response` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryResultsV2Response`.
        :rtype: TestMonitorQueryResultsV2Response
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
        results_ = _serialize(self.results)
        total_count_ = _serialize(self.total_count)
        return {
            'results': results_,
            'totalCount': total_count_
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


class TestMonitorCreateTestStepsRequest(RequestMessage):
    """
    TestMonitorCreateTestStepsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorCreateTestStepsRequest'

    def __init__(self,
                 steps_=None,
                 update_result_total_time_=None):
        """
        :param steps_: steps
        :type steps_: list(StepCreateRequest)
        :param update_result_total_time_: update_result_total_time
        :type update_result_total_time_: bool
        """
        self.steps = steps_
        self.update_result_total_time = update_result_total_time_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorCreateTestStepsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorCreateTestStepsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorCreateTestStepsRequest`.
        :rtype: TestMonitorCreateTestStepsRequest
        """
        steps_ = _deserialize(body_dict.get('steps'), 'list(StepCreateRequest)')
        update_result_total_time_ = _deserialize(body_dict.get('updateResultTotalTime'), 'bool')
        return cls(
            steps_=steps_,
            update_result_total_time_=update_result_total_time_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorCreateTestStepsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorCreateTestStepsRequest`.
        :rtype: TestMonitorCreateTestStepsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorCreateTestStepsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorCreateTestStepsRequest`.
        :rtype: TestMonitorCreateTestStepsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorCreateTestStepsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorCreateTestStepsRequest`.
        :rtype: TestMonitorCreateTestStepsRequest
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
        steps_ = _serialize(self.steps)
        update_result_total_time_ = _serialize(self.update_result_total_time)
        return {
            'steps': steps_,
            'updateResultTotalTime': update_result_total_time_
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


class TestMonitorCreateTestStepsResponse(ResponseMessage):
    """
    TestMonitorCreateTestStepsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorCreateTestStepsResponse'

    def __init__(self,
                 request_message,
                 steps_=None,
                 failed_=None,
                 errors_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param steps_: steps
        :type steps_: list(StepResponse)
        :param failed_: failed
        :type failed_: list(StepCreateRequest)
        :param errors_: errors
        :type errors_: ErrorEntry
        """
        self.steps = steps_
        self.failed = failed_
        self.errors = errors_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorCreateTestStepsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorCreateTestStepsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorCreateTestStepsResponse`.
        :rtype: TestMonitorCreateTestStepsResponse
        """
        steps_ = _deserialize(body_dict.get('steps'), 'list(StepResponse)')
        failed_ = _deserialize(body_dict.get('failed'), 'list(StepCreateRequest)')
        errors_ = _deserialize(body_dict.get('errors'), 'ErrorEntry')
        return cls(
            request_message,
            steps_=steps_,
            failed_=failed_,
            errors_=errors_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorCreateTestStepsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorCreateTestStepsResponse`.
        :rtype: TestMonitorCreateTestStepsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorCreateTestStepsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorCreateTestStepsResponse`.
        :rtype: TestMonitorCreateTestStepsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorCreateTestStepsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorCreateTestStepsResponse`.
        :rtype: TestMonitorCreateTestStepsResponse
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
        steps_ = _serialize(self.steps)
        failed_ = _serialize(self.failed)
        errors_ = _serialize(self.errors)
        return {
            'steps': steps_,
            'failed': failed_,
            'errors': errors_
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


class TestMonitorUpdateTestStepsRequest(RequestMessage):
    """
    TestMonitorUpdateTestStepsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorUpdateTestStepsRequest'

    def __init__(self,
                 steps_=None,
                 update_result_total_time_=None):
        """
        :param steps_: steps
        :type steps_: list(StepUpdateRequest)
        :param update_result_total_time_: update_result_total_time
        :type update_result_total_time_: bool
        """
        self.steps = steps_
        self.update_result_total_time = update_result_total_time_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorUpdateTestStepsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorUpdateTestStepsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorUpdateTestStepsRequest`.
        :rtype: TestMonitorUpdateTestStepsRequest
        """
        steps_ = _deserialize(body_dict.get('steps'), 'list(StepUpdateRequest)')
        update_result_total_time_ = _deserialize(body_dict.get('updateResultTotalTime'), 'bool')
        return cls(
            steps_=steps_,
            update_result_total_time_=update_result_total_time_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorUpdateTestStepsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorUpdateTestStepsRequest`.
        :rtype: TestMonitorUpdateTestStepsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorUpdateTestStepsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorUpdateTestStepsRequest`.
        :rtype: TestMonitorUpdateTestStepsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorUpdateTestStepsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorUpdateTestStepsRequest`.
        :rtype: TestMonitorUpdateTestStepsRequest
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
        steps_ = _serialize(self.steps)
        update_result_total_time_ = _serialize(self.update_result_total_time)
        return {
            'steps': steps_,
            'updateResultTotalTime': update_result_total_time_
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


class TestMonitorUpdateTestStepsResponse(ResponseMessage):
    """
    TestMonitorUpdateTestStepsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorUpdateTestStepsResponse'

    def __init__(self,
                 request_message,
                 steps_=None,
                 failed_=None,
                 errors_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param steps_: steps
        :type steps_: list(StepResponse)
        :param failed_: failed
        :type failed_: list(StepUpdateRequest)
        :param errors_: errors
        :type errors_: ErrorEntry
        """
        self.steps = steps_
        self.failed = failed_
        self.errors = errors_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorUpdateTestStepsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorUpdateTestStepsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorUpdateTestStepsResponse`.
        :rtype: TestMonitorUpdateTestStepsResponse
        """
        steps_ = _deserialize(body_dict.get('steps'), 'list(StepResponse)')
        failed_ = _deserialize(body_dict.get('failed'), 'list(StepUpdateRequest)')
        errors_ = _deserialize(body_dict.get('errors'), 'ErrorEntry')
        return cls(
            request_message,
            steps_=steps_,
            failed_=failed_,
            errors_=errors_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorUpdateTestStepsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorUpdateTestStepsResponse`.
        :rtype: TestMonitorUpdateTestStepsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorUpdateTestStepsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorUpdateTestStepsResponse`.
        :rtype: TestMonitorUpdateTestStepsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorUpdateTestStepsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorUpdateTestStepsResponse`.
        :rtype: TestMonitorUpdateTestStepsResponse
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
        steps_ = _serialize(self.steps)
        failed_ = _serialize(self.failed)
        errors_ = _serialize(self.errors)
        return {
            'steps': steps_,
            'failed': failed_,
            'errors': errors_
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


class TestMonitorDeleteStepsRequest(RequestMessage):
    """
    TestMonitorDeleteStepsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorDeleteStepsRequest'

    def __init__(self,
                 steps_=None,
                 update_result_total_time_=None):
        """
        :param steps_: steps
        :type steps_: list(StepDeleteRequest)
        :param update_result_total_time_: update_result_total_time
        :type update_result_total_time_: bool
        """
        self.steps = steps_
        self.update_result_total_time = update_result_total_time_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorDeleteStepsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorDeleteStepsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorDeleteStepsRequest`.
        :rtype: TestMonitorDeleteStepsRequest
        """
        steps_ = _deserialize(body_dict.get('steps'), 'list(StepDeleteRequest)')
        update_result_total_time_ = _deserialize(body_dict.get('updateResultTotalTime'), 'bool')
        return cls(
            steps_=steps_,
            update_result_total_time_=update_result_total_time_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorDeleteStepsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorDeleteStepsRequest`.
        :rtype: TestMonitorDeleteStepsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorDeleteStepsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorDeleteStepsRequest`.
        :rtype: TestMonitorDeleteStepsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorDeleteStepsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorDeleteStepsRequest`.
        :rtype: TestMonitorDeleteStepsRequest
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
        steps_ = _serialize(self.steps)
        update_result_total_time_ = _serialize(self.update_result_total_time)
        return {
            'steps': steps_,
            'updateResultTotalTime': update_result_total_time_
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


class TestMonitorDeleteStepsResponse(ResponseMessage):
    """
    TestMonitorDeleteStepsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorDeleteStepsResponse'

    def __init__(self,
                 request_message,
                 steps_=None,
                 failed_=None,
                 errors_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param steps_: steps
        :type steps_: list(StepResponse)
        :param failed_: failed
        :type failed_: list(StepDeleteRequest)
        :param errors_: errors
        :type errors_: ErrorEntry
        """
        self.steps = steps_
        self.failed = failed_
        self.errors = errors_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorDeleteStepsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorDeleteStepsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorDeleteStepsResponse`.
        :rtype: TestMonitorDeleteStepsResponse
        """
        steps_ = _deserialize(body_dict.get('steps'), 'list(StepResponse)')
        failed_ = _deserialize(body_dict.get('failed'), 'list(StepDeleteRequest)')
        errors_ = _deserialize(body_dict.get('errors'), 'ErrorEntry')
        return cls(
            request_message,
            steps_=steps_,
            failed_=failed_,
            errors_=errors_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorDeleteStepsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorDeleteStepsResponse`.
        :rtype: TestMonitorDeleteStepsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorDeleteStepsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorDeleteStepsResponse`.
        :rtype: TestMonitorDeleteStepsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorDeleteStepsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorDeleteStepsResponse`.
        :rtype: TestMonitorDeleteStepsResponse
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
        steps_ = _serialize(self.steps)
        failed_ = _serialize(self.failed)
        errors_ = _serialize(self.errors)
        return {
            'steps': steps_,
            'failed': failed_,
            'errors': errors_
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


class TestMonitorQueryStepsRequest(RequestMessage):
    """
    TestMonitorQueryStepsRequest JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorQueryStepsRequest'

    def __init__(self,
                 query_=None,
                 skip_=None,
                 take_=None):
        """
        :param query_: query
        :type query_: StepQuery
        :param skip_: skip
        :type skip_: int
        :param take_: take
        :type take_: int
        """
        self.query = query_
        self.skip = skip_
        self.take = take_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorQueryStepsRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryStepsRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryStepsRequest`.
        :rtype: TestMonitorQueryStepsRequest
        """
        query_ = _deserialize(body_dict.get('query'), 'StepQuery')
        skip_ = _deserialize(body_dict.get('skip'), 'int')
        take_ = _deserialize(body_dict.get('take'), 'int')
        return cls(
            query_=query_,
            skip_=skip_,
            take_=take_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryStepsRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryStepsRequest`.
        :rtype: TestMonitorQueryStepsRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryStepsRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryStepsRequest`.
        :rtype: TestMonitorQueryStepsRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryStepsRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryStepsRequest`.
        :rtype: TestMonitorQueryStepsRequest
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
        query_ = _serialize(self.query)
        skip_ = _serialize(self.skip)
        take_ = _serialize(self.take)
        return {
            'query': query_,
            'skip': skip_,
            'take': take_
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


class TestMonitorQueryStepsResponse(ResponseMessage):
    """
    TestMonitorQueryStepsResponse JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorQueryStepsResponse'

    def __init__(self,
                 request_message,
                 steps_=None,
                 total_count_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param steps_: steps
        :type steps_: list(StepResponse)
        :param total_count_: total_count
        :type total_count_: int
        """
        self.steps = steps_
        self.total_count = total_count_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorQueryStepsResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryStepsResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryStepsResponse`.
        :rtype: TestMonitorQueryStepsResponse
        """
        steps_ = _deserialize(body_dict.get('steps'), 'list(StepResponse)')
        total_count_ = _deserialize(body_dict.get('totalCount'), 'int')
        return cls(
            request_message,
            steps_=steps_,
            total_count_=total_count_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryStepsResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryStepsResponse`.
        :rtype: TestMonitorQueryStepsResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryStepsResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryStepsResponse`.
        :rtype: TestMonitorQueryStepsResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryStepsResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryStepsResponse`.
        :rtype: TestMonitorQueryStepsResponse
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
        steps_ = _serialize(self.steps)
        total_count_ = _serialize(self.total_count)
        return {
            'steps': steps_,
            'totalCount': total_count_
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


class TestMonitorQueryStepsV2Request(RequestMessage):
    """
    TestMonitorQueryStepsV2Request JSON request message.
    """
    MESSAGE_NAME = 'TestMonitorQueryStepsV2Request'

    def __init__(self,
                 filter_=None,
                 order_by_=None,
                 projection_=None,
                 skip_=None,
                 take_=None):
        """
        :param filter_: filter
        :type filter_: AdvancedQueryFilter
        :param order_by_: order_by
        :type order_by_: list(StepSortDefinition)
        :param projection_: projection
        :type projection_: list(StepField)
        :param skip_: skip
        :type skip_: int
        :param take_: take
        :type take_: int
        """
        self.filter = filter_
        self.order_by = order_by_
        self.projection = projection_
        self.skip = skip_
        self.take = take_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorQueryStepsV2Request, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryStepsV2Request` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryStepsV2Request`.
        :rtype: TestMonitorQueryStepsV2Request
        """
        filter_ = _deserialize(body_dict.get('filter'), 'AdvancedQueryFilter')
        order_by_ = _deserialize(body_dict.get('orderBy'), 'list(StepSortDefinition)')
        projection_ = _deserialize(body_dict.get('projection'), 'list(StepField)')
        skip_ = _deserialize(body_dict.get('skip'), 'int')
        take_ = _deserialize(body_dict.get('take'), 'int')
        return cls(
            filter_=filter_,
            order_by_=order_by_,
            projection_=projection_,
            skip_=skip_,
            take_=take_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryStepsV2Request` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryStepsV2Request`.
        :rtype: TestMonitorQueryStepsV2Request
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryStepsV2Request` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryStepsV2Request`.
        :rtype: TestMonitorQueryStepsV2Request
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryStepsV2Request` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryStepsV2Request`.
        :rtype: TestMonitorQueryStepsV2Request
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
        filter_ = _serialize(self.filter)
        order_by_ = _serialize(self.order_by)
        projection_ = _serialize(self.projection)
        skip_ = _serialize(self.skip)
        take_ = _serialize(self.take)
        return {
            'filter': filter_,
            'orderBy': order_by_,
            'projection': projection_,
            'skip': skip_,
            'take': take_
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


class TestMonitorQueryStepsV2Response(ResponseMessage):
    """
    TestMonitorQueryStepsV2Response JSON response message.
    """
    MESSAGE_NAME = 'TestMonitorQueryStepsV2Response'

    def __init__(self,
                 request_message,
                 steps_=None,
                 total_count_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param steps_: steps
        :type steps_: list(StepResponse)
        :param total_count_: total_count
        :type total_count_: long
        """
        self.steps = steps_
        self.total_count = total_count_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(TestMonitorQueryStepsV2Response, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`TestMonitorQueryStepsV2Response` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorQueryStepsV2Response`.
        :rtype: TestMonitorQueryStepsV2Response
        """
        steps_ = _deserialize(body_dict.get('steps'), 'list(StepResponse)')
        total_count_ = _deserialize(body_dict.get('totalCount'), 'long')
        return cls(
            request_message,
            steps_=steps_,
            total_count_=total_count_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`TestMonitorQueryStepsV2Response` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorQueryStepsV2Response`.
        :rtype: TestMonitorQueryStepsV2Response
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`TestMonitorQueryStepsV2Response` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorQueryStepsV2Response`.
        :rtype: TestMonitorQueryStepsV2Response
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorQueryStepsV2Response` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorQueryStepsV2Response`.
        :rtype: TestMonitorQueryStepsV2Response
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
        steps_ = _serialize(self.steps)
        total_count_ = _serialize(self.total_count)
        return {
            'steps': steps_,
            'totalCount': total_count_
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


class TestMonitorSendResultEmailRoutedMessage(RoutedMessage):
    """
    TestMonitorSendResultEmailRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'TestMonitorSendResultEmailRoutedMessage'

    def __init__(self,
                 result_id_=None,
                 to_addresses_=None,
                 template_name_=None,
                 template_id_=None,
                 address_group_id_=None):
        """
        :param result_id_: result_id
        :type result_id_: str
        :param to_addresses_: to_addresses
        :type to_addresses_: list(str)
        :param template_name_: template_name
        :type template_name_: str
        :param template_id_: template_id
        :type template_id_: str
        :param address_group_id_: address_group_id
        :type address_group_id_: str
        """
        self.result_id = result_id_
        self.to_addresses = to_addresses_
        self.template_name = template_name_
        self.template_id = template_id_
        self.address_group_id = address_group_id_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('TestMonitor', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorSendResultEmailRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorSendResultEmailRoutedMessage` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorSendResultEmailRoutedMessage`.
        :rtype: TestMonitorSendResultEmailRoutedMessage
        """
        result_id_ = _deserialize(body_dict.get('resultId'), 'str')
        to_addresses_ = _deserialize(body_dict.get('toAddresses'), 'list(str)')
        template_name_ = _deserialize(body_dict.get('templateName'), 'str')
        template_id_ = _deserialize(body_dict.get('templateId'), 'str')
        address_group_id_ = _deserialize(body_dict.get('addressGroupId'), 'str')
        return cls(
            result_id_=result_id_,
            to_addresses_=to_addresses_,
            template_name_=template_name_,
            template_id_=template_id_,
            address_group_id_=address_group_id_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorSendResultEmailRoutedMessage` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorSendResultEmailRoutedMessage`.
        :rtype: TestMonitorSendResultEmailRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorSendResultEmailRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorSendResultEmailRoutedMessage`.
        :rtype: TestMonitorSendResultEmailRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorSendResultEmailRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorSendResultEmailRoutedMessage`.
        :rtype: TestMonitorSendResultEmailRoutedMessage
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
        result_id_ = _serialize(self.result_id)
        to_addresses_ = _serialize(self.to_addresses)
        template_name_ = _serialize(self.template_name)
        template_id_ = _serialize(self.template_id)
        address_group_id_ = _serialize(self.address_group_id)
        return {
            'resultId': result_id_,
            'toAddresses': to_addresses_,
            'templateName': template_name_,
            'templateId': template_id_,
            'addressGroupId': address_group_id_
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


class TestMonitorResultsCreatedBroadcast(BroadcastMessage):
    """
    TestMonitorResultsCreatedBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'TestMonitorResultsCreatedBroadcast'

    def __init__(self,
                 results_=None):
        """
        :param results_: results
        :type results_: list(ResultResponse)
        """
        self.results = results_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorResultsCreatedBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorResultsCreatedBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorResultsCreatedBroadcast`.
        :rtype: TestMonitorResultsCreatedBroadcast
        """
        results_ = _deserialize(body_dict.get('results'), 'list(ResultResponse)')
        return cls(
            results_=results_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorResultsCreatedBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorResultsCreatedBroadcast`.
        :rtype: TestMonitorResultsCreatedBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorResultsCreatedBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorResultsCreatedBroadcast`.
        :rtype: TestMonitorResultsCreatedBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorResultsCreatedBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorResultsCreatedBroadcast`.
        :rtype: TestMonitorResultsCreatedBroadcast
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
        results_ = _serialize(self.results)
        return {
            'results': results_
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


class TestMonitorResultsUpdatedBroadcast(BroadcastMessage):
    """
    TestMonitorResultsUpdatedBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'TestMonitorResultsUpdatedBroadcast'

    def __init__(self,
                 results_=None):
        """
        :param results_: results
        :type results_: list(ResultResponse)
        """
        self.results = results_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorResultsUpdatedBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorResultsUpdatedBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorResultsUpdatedBroadcast`.
        :rtype: TestMonitorResultsUpdatedBroadcast
        """
        results_ = _deserialize(body_dict.get('results'), 'list(ResultResponse)')
        return cls(
            results_=results_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorResultsUpdatedBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorResultsUpdatedBroadcast`.
        :rtype: TestMonitorResultsUpdatedBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorResultsUpdatedBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorResultsUpdatedBroadcast`.
        :rtype: TestMonitorResultsUpdatedBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorResultsUpdatedBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorResultsUpdatedBroadcast`.
        :rtype: TestMonitorResultsUpdatedBroadcast
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
        results_ = _serialize(self.results)
        return {
            'results': results_
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


class TestMonitorResultsDeletedBroadcast(BroadcastMessage):
    """
    TestMonitorResultsDeletedBroadcast JSON broadcast message.
    """
    MESSAGE_NAME = 'TestMonitorResultsDeletedBroadcast'

    def __init__(self,
                 results_=None):
        """
        :param results_: results
        :type results_: list(ResultResponse)
        """
        self.results = results_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key(None, self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(TestMonitorResultsDeletedBroadcast, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`TestMonitorResultsDeletedBroadcast` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`TestMonitorResultsDeletedBroadcast`.
        :rtype: TestMonitorResultsDeletedBroadcast
        """
        results_ = _deserialize(body_dict.get('results'), 'list(ResultResponse)')
        return cls(
            results_=results_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`TestMonitorResultsDeletedBroadcast` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`TestMonitorResultsDeletedBroadcast`.
        :rtype: TestMonitorResultsDeletedBroadcast
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`TestMonitorResultsDeletedBroadcast` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`TestMonitorResultsDeletedBroadcast`.
        :rtype: TestMonitorResultsDeletedBroadcast
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`TestMonitorResultsDeletedBroadcast` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`TestMonitorResultsDeletedBroadcast`.
        :rtype: TestMonitorResultsDeletedBroadcast
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
        results_ = _serialize(self.results)
        return {
            'results': results_
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
