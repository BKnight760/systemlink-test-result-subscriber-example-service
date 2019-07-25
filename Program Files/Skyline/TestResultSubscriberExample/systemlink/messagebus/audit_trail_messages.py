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
# AuditTrail service
#


class AuditTypeEntry(object):
    """
    AuditTypeEntry custom data type.
    """
    def __init__(self,
                 short_name_=None,
                 description_=None):
        """
        :param short_name_: short_name
        :type short_name_: str
        :param description_: description
        :type description_: str
        """
        self.short_name = short_name_
        self.description = description_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`AuditTypeEntry` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`AuditTypeEntry`.
        :rtype: AuditTypeEntry
        """
        short_name_ = _deserialize(body_dict.get('shortName'), 'str')
        description_ = _deserialize(body_dict.get('description'), 'str')
        return cls(
            short_name_=short_name_,
            description_=description_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AuditTypeEntry` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditTypeEntry`.
        :rtype: AuditTypeEntry
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AuditTypeEntry` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditTypeEntry`.
        :rtype: AuditTypeEntry
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        short_name_ = _serialize(self.short_name)
        description_ = _serialize(self.description)
        return {
            'shortName': short_name_,
            'description': description_
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


class AuditEntry(object):
    """
    AuditEntry custom data type.
    """
    def __init__(self,
                 timestamp_=None,
                 subtype_=None,
                 originator_=None,
                 user_name_=None,
                 record_type_=None,
                 device_=None,
                 detail_=None,
                 int1_=None,
                 int2_=None,
                 int3_=None,
                 int4_=None,
                 str1_=None,
                 str2_=None,
                 str3_=None,
                 str4_=None):
        """
        :param timestamp_: timestamp
        :type timestamp_: datetime
        :param subtype_: subtype
        :type subtype_: str
        :param originator_: originator
        :type originator_: str
        :param user_name_: user_name
        :type user_name_: str
        :param record_type_: record_type
        :type record_type_: str
        :param device_: device
        :type device_: str
        :param detail_: detail
        :type detail_: str
        :param int1_: int1
        :type int1_: int
        :param int2_: int2
        :type int2_: int
        :param int3_: int3
        :type int3_: int
        :param int4_: int4
        :type int4_: int
        :param str1_: str1
        :type str1_: str
        :param str2_: str2
        :type str2_: str
        :param str3_: str3
        :type str3_: str
        :param str4_: str4
        :type str4_: str
        """
        self.timestamp = timestamp_
        self.subtype = subtype_
        self.originator = originator_
        self.user_name = user_name_
        self.record_type = record_type_
        self.device = device_
        self.detail = detail_
        self.int1 = int1_
        self.int2 = int2_
        self.int3 = int3_
        self.int4 = int4_
        self.str1 = str1_
        self.str2 = str2_
        self.str3 = str3_
        self.str4 = str4_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`AuditEntry` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`AuditEntry`.
        :rtype: AuditEntry
        """
        timestamp_ = _deserialize(body_dict.get('timestamp'), 'datetime')
        subtype_ = _deserialize(body_dict.get('subtype'), 'str')
        originator_ = _deserialize(body_dict.get('originator'), 'str')
        user_name_ = _deserialize(body_dict.get('userName'), 'str')
        record_type_ = _deserialize(body_dict.get('recordType'), 'str')
        device_ = _deserialize(body_dict.get('device'), 'str')
        detail_ = _deserialize(body_dict.get('detail'), 'str')
        int1_ = _deserialize(body_dict.get('int1'), 'int')
        int2_ = _deserialize(body_dict.get('int2'), 'int')
        int3_ = _deserialize(body_dict.get('int3'), 'int')
        int4_ = _deserialize(body_dict.get('int4'), 'int')
        str1_ = _deserialize(body_dict.get('str1'), 'str')
        str2_ = _deserialize(body_dict.get('str2'), 'str')
        str3_ = _deserialize(body_dict.get('str3'), 'str')
        str4_ = _deserialize(body_dict.get('str4'), 'str')
        return cls(
            timestamp_=timestamp_,
            subtype_=subtype_,
            originator_=originator_,
            user_name_=user_name_,
            record_type_=record_type_,
            device_=device_,
            detail_=detail_,
            int1_=int1_,
            int2_=int2_,
            int3_=int3_,
            int4_=int4_,
            str1_=str1_,
            str2_=str2_,
            str3_=str3_,
            str4_=str4_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AuditEntry` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditEntry`.
        :rtype: AuditEntry
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AuditEntry` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditEntry`.
        :rtype: AuditEntry
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        timestamp_ = _serialize(self.timestamp)
        subtype_ = _serialize(self.subtype)
        originator_ = _serialize(self.originator)
        user_name_ = _serialize(self.user_name)
        record_type_ = _serialize(self.record_type)
        device_ = _serialize(self.device)
        detail_ = _serialize(self.detail)
        int1_ = _serialize(self.int1)
        int2_ = _serialize(self.int2)
        int3_ = _serialize(self.int3)
        int4_ = _serialize(self.int4)
        str1_ = _serialize(self.str1)
        str2_ = _serialize(self.str2)
        str3_ = _serialize(self.str3)
        str4_ = _serialize(self.str4)
        return {
            'timestamp': timestamp_,
            'subtype': subtype_,
            'originator': originator_,
            'userName': user_name_,
            'recordType': record_type_,
            'device': device_,
            'detail': detail_,
            'int1': int1_,
            'int2': int2_,
            'int3': int3_,
            'int4': int4_,
            'str1': str1_,
            'str2': str2_,
            'str3': str3_,
            'str4': str4_
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


class AuditQueryParameters(object):
    """
    AuditQueryParameters custom data type.
    """
    def __init__(self,
                 timestamp_from_=None,
                 timestamp_to_=None,
                 originator_=None,
                 record_type_=None,
                 subtype_=None,
                 device_=None,
                 detail_=None,
                 int1_=None,
                 int2_=None,
                 int3_=None,
                 int4_=None,
                 str1_=None,
                 str2_=None,
                 str3_=None,
                 str4_=None,
                 query_using_timestamps_=None,
                 query_using_ints_=None,
                 skip_count_=None,
                 max_records_=None,
                 order_by_=None,
                 order_by_descending_=None):
        """
        :param timestamp_from_: timestamp_from
        :type timestamp_from_: datetime
        :param timestamp_to_: timestamp_to
        :type timestamp_to_: datetime
        :param originator_: originator
        :type originator_: str
        :param record_type_: record_type
        :type record_type_: str
        :param subtype_: subtype
        :type subtype_: str
        :param device_: device
        :type device_: str
        :param detail_: detail
        :type detail_: str
        :param int1_: int1
        :type int1_: int
        :param int2_: int2
        :type int2_: int
        :param int3_: int3
        :type int3_: int
        :param int4_: int4
        :type int4_: int
        :param str1_: str1
        :type str1_: str
        :param str2_: str2
        :type str2_: str
        :param str3_: str3
        :type str3_: str
        :param str4_: str4
        :type str4_: str
        :param query_using_timestamps_: query_using_timestamps
        :type query_using_timestamps_: bool
        :param query_using_ints_: query_using_ints
        :type query_using_ints_: list(int)
        :param skip_count_: skip_count
        :type skip_count_: int
        :param max_records_: max_records
        :type max_records_: int
        :param order_by_: order_by
        :type order_by_: str
        :param order_by_descending_: order_by_descending
        :type order_by_descending_: str
        """
        self.timestamp_from = timestamp_from_
        self.timestamp_to = timestamp_to_
        self.originator = originator_
        self.record_type = record_type_
        self.subtype = subtype_
        self.device = device_
        self.detail = detail_
        self.int1 = int1_
        self.int2 = int2_
        self.int3 = int3_
        self.int4 = int4_
        self.str1 = str1_
        self.str2 = str2_
        self.str3 = str3_
        self.str4 = str4_
        self.query_using_timestamps = query_using_timestamps_
        self.query_using_ints = query_using_ints_
        self.skip_count = skip_count_
        self.max_records = max_records_
        self.order_by = order_by_
        self.order_by_descending = order_by_descending_

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`AuditQueryParameters` using a dictionary.

        :param body_dict: A dictionary representing the body.
        :type body_dict: dict
        :return: A new instance of :class:`AuditQueryParameters`.
        :rtype: AuditQueryParameters
        """
        timestamp_from_ = _deserialize(body_dict.get('timestampFrom'), 'datetime')
        timestamp_to_ = _deserialize(body_dict.get('timestampTo'), 'datetime')
        originator_ = _deserialize(body_dict.get('originator'), 'str')
        record_type_ = _deserialize(body_dict.get('recordType'), 'str')
        subtype_ = _deserialize(body_dict.get('subtype'), 'str')
        device_ = _deserialize(body_dict.get('device'), 'str')
        detail_ = _deserialize(body_dict.get('detail'), 'str')
        int1_ = _deserialize(body_dict.get('int1'), 'int')
        int2_ = _deserialize(body_dict.get('int2'), 'int')
        int3_ = _deserialize(body_dict.get('int3'), 'int')
        int4_ = _deserialize(body_dict.get('int4'), 'int')
        str1_ = _deserialize(body_dict.get('str1'), 'str')
        str2_ = _deserialize(body_dict.get('str2'), 'str')
        str3_ = _deserialize(body_dict.get('str3'), 'str')
        str4_ = _deserialize(body_dict.get('str4'), 'str')
        query_using_timestamps_ = _deserialize(body_dict.get('queryUsingTimestamps'), 'bool')
        query_using_ints_ = _deserialize(body_dict.get('queryUsingInts'), 'list(int)')
        skip_count_ = _deserialize(body_dict.get('skipCount'), 'int')
        max_records_ = _deserialize(body_dict.get('maxRecords'), 'int')
        order_by_ = _deserialize(body_dict.get('orderBy'), 'str')
        order_by_descending_ = _deserialize(body_dict.get('orderByDescending'), 'str')
        return cls(
            timestamp_from_=timestamp_from_,
            timestamp_to_=timestamp_to_,
            originator_=originator_,
            record_type_=record_type_,
            subtype_=subtype_,
            device_=device_,
            detail_=detail_,
            int1_=int1_,
            int2_=int2_,
            int3_=int3_,
            int4_=int4_,
            str1_=str1_,
            str2_=str2_,
            str3_=str3_,
            str4_=str4_,
            query_using_timestamps_=query_using_timestamps_,
            query_using_ints_=query_using_ints_,
            skip_count_=skip_count_,
            max_records_=max_records_,
            order_by_=order_by_,
            order_by_descending_=order_by_descending_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AuditQueryParameters` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditQueryParameters`.
        :rtype: AuditQueryParameters
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AuditQueryParameters` using a body
        of type :class:`bytes` or :class:`bytearray`.

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditQueryParameters`.
        :rtype: AuditQueryParameters
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    def to_dict(self):
        """
        Returns a dictionary representing the data in this object.

        :return: A dictionary representing the data in this object.
        :rtype: dict
        """
        timestamp_from_ = _serialize(self.timestamp_from)
        timestamp_to_ = _serialize(self.timestamp_to)
        originator_ = _serialize(self.originator)
        record_type_ = _serialize(self.record_type)
        subtype_ = _serialize(self.subtype)
        device_ = _serialize(self.device)
        detail_ = _serialize(self.detail)
        int1_ = _serialize(self.int1)
        int2_ = _serialize(self.int2)
        int3_ = _serialize(self.int3)
        int4_ = _serialize(self.int4)
        str1_ = _serialize(self.str1)
        str2_ = _serialize(self.str2)
        str3_ = _serialize(self.str3)
        str4_ = _serialize(self.str4)
        query_using_timestamps_ = _serialize(self.query_using_timestamps)
        query_using_ints_ = _serialize(self.query_using_ints)
        skip_count_ = _serialize(self.skip_count)
        max_records_ = _serialize(self.max_records)
        order_by_ = _serialize(self.order_by)
        order_by_descending_ = _serialize(self.order_by_descending)
        return {
            'timestampFrom': timestamp_from_,
            'timestampTo': timestamp_to_,
            'originator': originator_,
            'recordType': record_type_,
            'subtype': subtype_,
            'device': device_,
            'detail': detail_,
            'int1': int1_,
            'int2': int2_,
            'int3': int3_,
            'int4': int4_,
            'str1': str1_,
            'str2': str2_,
            'str3': str3_,
            'str4': str4_,
            'queryUsingTimestamps': query_using_timestamps_,
            'queryUsingInts': query_using_ints_,
            'skipCount': skip_count_,
            'maxRecords': max_records_,
            'orderBy': order_by_,
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


class AuditTypeListRequest(RequestMessage):
    """
    AuditTypeListRequest JSON request message.
    """
    MESSAGE_NAME = 'AuditTypeListRequest'

    def __init__(self):
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('AuditTrail', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(AuditTypeListRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`AuditTypeListRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`AuditTypeListRequest`.
        :rtype: AuditTypeListRequest
        """
        return cls(
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AuditTypeListRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditTypeListRequest`.
        :rtype: AuditTypeListRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AuditTypeListRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditTypeListRequest`.
        :rtype: AuditTypeListRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`AuditTypeListRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`AuditTypeListRequest`.
        :rtype: AuditTypeListRequest
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


class AuditTypeListResponse(ResponseMessage):
    """
    AuditTypeListResponse JSON response message.
    """
    MESSAGE_NAME = 'AuditTypeListResponse'

    def __init__(self,
                 request_message,
                 entries_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param entries_: entries
        :type entries_: list(AuditTypeEntry)
        """
        self.entries = entries_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(AuditTypeListResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`AuditTypeListResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`AuditTypeListResponse`.
        :rtype: AuditTypeListResponse
        """
        entries_ = _deserialize(body_dict.get('entries'), 'list(AuditTypeEntry)')
        return cls(
            request_message,
            entries_=entries_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`AuditTypeListResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditTypeListResponse`.
        :rtype: AuditTypeListResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`AuditTypeListResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditTypeListResponse`.
        :rtype: AuditTypeListResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`AuditTypeListResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`AuditTypeListResponse`.
        :rtype: AuditTypeListResponse
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


class AuditTypeAddRoutedMessage(RoutedMessage):
    """
    AuditTypeAddRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'AuditTypeAddRoutedMessage'

    def __init__(self,
                 entry_=None):
        """
        :param entry_: entry
        :type entry_: AuditTypeEntry
        """
        self.entry = entry_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('AuditTrail', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(AuditTypeAddRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`AuditTypeAddRoutedMessage` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`AuditTypeAddRoutedMessage`.
        :rtype: AuditTypeAddRoutedMessage
        """
        entry_ = _deserialize(body_dict.get('entry'), 'AuditTypeEntry')
        return cls(
            entry_=entry_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AuditTypeAddRoutedMessage` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditTypeAddRoutedMessage`.
        :rtype: AuditTypeAddRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AuditTypeAddRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditTypeAddRoutedMessage`.
        :rtype: AuditTypeAddRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`AuditTypeAddRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`AuditTypeAddRoutedMessage`.
        :rtype: AuditTypeAddRoutedMessage
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
        entry_ = _serialize(self.entry)
        return {
            'entry': entry_
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


class AuditTypeDeleteRequest(RequestMessage):
    """
    AuditTypeDeleteRequest JSON request message.
    """
    MESSAGE_NAME = 'AuditTypeDeleteRequest'

    def __init__(self,
                 id_=None):
        """
        :param id_: id
        :type id_: str
        """
        self.id = id_  # pylint: disable=invalid-name
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('AuditTrail', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(AuditTypeDeleteRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`AuditTypeDeleteRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`AuditTypeDeleteRequest`.
        :rtype: AuditTypeDeleteRequest
        """
        id_ = _deserialize(body_dict.get('id'), 'str')  # pylint: disable=invalid-name
        return cls(
            id_=id_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AuditTypeDeleteRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditTypeDeleteRequest`.
        :rtype: AuditTypeDeleteRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AuditTypeDeleteRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditTypeDeleteRequest`.
        :rtype: AuditTypeDeleteRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`AuditTypeDeleteRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`AuditTypeDeleteRequest`.
        :rtype: AuditTypeDeleteRequest
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
        id_ = _serialize(self.id)  # pylint: disable=invalid-name
        return {
            'id': id_
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


class AuditTypeDeleteResponse(ResponseMessage):
    """
    AuditTypeDeleteResponse JSON response message.
    """
    MESSAGE_NAME = 'AuditTypeDeleteResponse'

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
        super(AuditTypeDeleteResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):  # pylint: disable=unused-argument
        """
        Create a new instance of :class:`AuditTypeDeleteResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`AuditTypeDeleteResponse`.
        :rtype: AuditTypeDeleteResponse
        """
        return cls(
            request_message
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`AuditTypeDeleteResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditTypeDeleteResponse`.
        :rtype: AuditTypeDeleteResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`AuditTypeDeleteResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditTypeDeleteResponse`.
        :rtype: AuditTypeDeleteResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`AuditTypeDeleteResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`AuditTypeDeleteResponse`.
        :rtype: AuditTypeDeleteResponse
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


class AuditQueryRequest(RequestMessage):
    """
    AuditQueryRequest JSON request message.
    """
    MESSAGE_NAME = 'AuditQueryRequest'

    def __init__(self,
                 parameters_=None,
                 take_count_=None,
                 skip_count_=None):
        """
        :param parameters_: parameters
        :type parameters_: AuditQueryParameters
        :param take_count_: take_count
        :type take_count_: int
        :param skip_count_: skip_count
        :type skip_count_: int
        """
        self.parameters = parameters_
        self.take_count = take_count_
        self.skip_count = skip_count_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('AuditTrail', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(AuditQueryRequest, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`AuditQueryRequest` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`AuditQueryRequest`.
        :rtype: AuditQueryRequest
        """
        parameters_ = _deserialize(body_dict.get('parameters'), 'AuditQueryParameters')
        take_count_ = _deserialize(body_dict.get('takeCount'), 'int')
        skip_count_ = _deserialize(body_dict.get('skipCount'), 'int')
        return cls(
            parameters_=parameters_,
            take_count_=take_count_,
            skip_count_=skip_count_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AuditQueryRequest` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditQueryRequest`.
        :rtype: AuditQueryRequest
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AuditQueryRequest` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditQueryRequest`.
        :rtype: AuditQueryRequest
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`AuditQueryRequest` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`AuditQueryRequest`.
        :rtype: AuditQueryRequest
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
        parameters_ = _serialize(self.parameters)
        take_count_ = _serialize(self.take_count)
        skip_count_ = _serialize(self.skip_count)
        return {
            'parameters': parameters_,
            'takeCount': take_count_,
            'skipCount': skip_count_
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


class AuditQueryResponse(ResponseMessage):
    """
    AuditQueryResponse JSON response message.
    """
    MESSAGE_NAME = 'AuditQueryResponse'

    def __init__(self,
                 request_message,
                 entries_=None,
                 full_count_=None):
        """
        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param entries_: entries
        :type entries_: list(AuditEntry)
        :param full_count_: full_count
        :type full_count_: int
        """
        self.entries = entries_
        self.full_count = full_count_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        # If request_message is None, routing key needs to be set outside this constructor.
        if request_message:
            header.correlation_id = request_message.correlation_id
            routing_key = MessageHeader.generate_routing_key(request_message.reply_to, self.MESSAGE_NAME)
            header.routing_key = routing_key
        super(AuditQueryResponse, self).__init__(header, None)

    @classmethod
    def from_dict(cls, request_message, body_dict):
        """
        Create a new instance of :class:`AuditQueryResponse` using a dictionary.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`AuditQueryResponse`.
        :rtype: AuditQueryResponse
        """
        entries_ = _deserialize(body_dict.get('entries'), 'list(AuditEntry)')
        full_count_ = _deserialize(body_dict.get('fullCount'), 'int')
        return cls(
            request_message,
            entries_=entries_,
            full_count_=full_count_
        )

    @classmethod
    def from_json(cls, request_message, body_json):
        """
        Create a new instance of :class:`AuditQueryResponse` using a JSON string.

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditQueryResponse`.
        :rtype: AuditQueryResponse
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(request_message, body_dict)

    @classmethod
    def from_body_bytes(cls, request_message, body_bytes):
        """
        Create a new instance of :class:`AuditQueryResponse` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param request_message: The request_message to use for reply information. May be None.
        :type request_message: systemlink.messagebus.message_base.MessageBase or None
        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditQueryResponse`.
        :rtype: AuditQueryResponse
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(request_message, body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`AuditQueryResponse` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`AuditQueryResponse`.
        :rtype: AuditQueryResponse
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
        entries_ = _serialize(self.entries)
        full_count_ = _serialize(self.full_count)
        return {
            'entries': entries_,
            'fullCount': full_count_
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


class AuditAddRoutedMessage(RoutedMessage):
    """
    AuditAddRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'AuditAddRoutedMessage'

    def __init__(self,
                 entries_=None):
        """
        :param entries_: entries
        :type entries_: list(AuditEntry)
        """
        self.entries = entries_
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('AuditTrail', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(AuditAddRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`AuditAddRoutedMessage` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`AuditAddRoutedMessage`.
        :rtype: AuditAddRoutedMessage
        """
        entries_ = _deserialize(body_dict.get('entries'), 'list(AuditEntry)')
        return cls(
            entries_=entries_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AuditAddRoutedMessage` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditAddRoutedMessage`.
        :rtype: AuditAddRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AuditAddRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditAddRoutedMessage`.
        :rtype: AuditAddRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`AuditAddRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`AuditAddRoutedMessage`.
        :rtype: AuditAddRoutedMessage
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


class AuditDeleteRoutedMessage(RoutedMessage):
    """
    AuditDeleteRoutedMessage JSON routed message.
    """
    MESSAGE_NAME = 'AuditDeleteRoutedMessage'

    def __init__(self,
                 id_=None):
        """
        :param id_: id
        :type id_: str
        """
        self.id = id_  # pylint: disable=invalid-name
        header = MessageHeader()
        header.message_name = self.MESSAGE_NAME
        header.content_type = JSON_MESSAGE_CONTENT_TYPE
        routing_key = MessageHeader.generate_routing_key('AuditTrail', self.MESSAGE_NAME)
        header.routing_key = routing_key
        super(AuditDeleteRoutedMessage, self).__init__(header, None)

    @classmethod
    def from_dict(cls, body_dict):
        """
        Create a new instance of :class:`AuditDeleteRoutedMessage` using a dictionary.

        :param body_dict: The body as a dictionary.
        :type body_dict: dict
        :return: A new instance of :class:`AuditDeleteRoutedMessage`.
        :rtype: AuditDeleteRoutedMessage
        """
        id_ = _deserialize(body_dict.get('id'), 'str')  # pylint: disable=invalid-name
        return cls(
            id_=id_
        )

    @classmethod
    def from_json(cls, body_json):
        """
        Create a new instance of :class:`AuditDeleteRoutedMessage` using a JSON string.

        :param body_json: A string in JSON format representing the body.
        :type body_json: str
        :return: A new instance of :class:`AuditDeleteRoutedMessage`.
        :rtype: AuditDeleteRoutedMessage
        """
        body_dict = json.loads(body_json)
        return cls.from_dict(body_dict)

    @classmethod
    def from_body_bytes(cls, body_bytes):
        """
        Create a new instance of :class:`AuditDeleteRoutedMessage` using a body
        of type :class:`bytes` or :class:`bytearray`,

        :param body_bytes: The body to use.
        :type body_bytes: bytes or bytearray
        :return: A new instance of :class:`AuditDeleteRoutedMessage`.
        :rtype: AuditDeleteRoutedMessage
        """
        body_json = str(body_bytes, 'utf-8')
        return cls.from_json(body_json)

    @classmethod
    def from_message(cls, message):
        """
        Create a new instance of :class`AuditDeleteRoutedMessage` using a
        :class:`systemlink.messagebus.message_base.MessageBase` derived message.

        :param message: The message to use as the basis for this class instance.
        :type message: systemlink.messagebus.message_base.MessageBase
        :return: A new instance of :class`AuditDeleteRoutedMessage`.
        :rtype: AuditDeleteRoutedMessage
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
        id_ = _serialize(self.id)  # pylint: disable=invalid-name
        return {
            'id': id_
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
