# -*- coding: utf-8 -*-
"""
Implementation of 'SerializationMixin'.
"""
from __future__ import absolute_import

# Import python libs
import functools
import json
from datetime import datetime
from typing import Any, Dict, List, Tuple, Union

# Import local libs
from systemlink.messagebus.datetime import from_datetime, to_datetime
from systemlink.messagebus.exceptions import SystemLinkException

# Special token signifying that the attribute is required and therefore
# does not have a default value.
_Required = object()  # pylint: disable=invalid-name


class SerializationMixin():
    """
    A mixin to add standard serialization and deserialization
    functionality to a client class.
    """

    # Client class that uses this mixin must define the following attributes:
    #   ATTRIBUTE_MAP (Dict[str, Tuple[str, type, Any]]):
    #       The key is the attribute name and the value is a 3-tuple
    #       containing the JSON key name, the Python type, and the
    #       default value (or ``_Required`` if the attribute is a
    #       required attribute).
    ATTRIBUTE_MAP = {}

    @classmethod
    def _get_real_type(cls, type_: type) -> Tuple[type, bool]:
        """
        Gets the real type from a type that may be :class:`Optional`,
        which means that it may also allow for ``None``.

        :param type_: The source type.
        :type type_: type
        :return: A 2-tuple where the first element is the real type
            and the second element is a :class:`bool` where if it
            is ``True``, it means that the type is optional (``None``
            is permitted).
        :rtype: tuple(type, bool)
        """
        # The :class:`typing.Optional` type automatically gets converted to
        # :class:`Union`.
        if hasattr(type_, '__origin__') and type_.__origin__ == Union:
            type_list = type_.__args__
            if len(type_list) == 2:
                if type_list[0] == type(None):
                    return type_list[1], True
                if type_list[1] == type(None):
                    return type_list[0], True
        return type_, False

    @classmethod
    def _from_embedded_list(  # pylint: disable=too-many-branches
            cls,
            lst: List[Any],
            item_type: type) -> List[Any]:
        """
        Performs deserialization of an embedded list.

        :param lst: The embedded list.
        :type lst: list
        :param item_type: The type of each list element.
        :type item_type: type
        :return: A list of deserialized objects meant to be used as
            constructor arguments for the parent class.
        :rtype: list
        :raises SystemLinkException: if an error occurs.
        """
        ret_lst = []

        item_type, optional = cls._get_real_type(item_type)

        embedded_list = False
        embedded_dict = False
        if hasattr(item_type, '__origin__') and item_type.__origin__ in (List, list):
            item_type = item_type.__args__[0]
            embedded_list = True
        elif hasattr(item_type, '__origin__') and item_type.__origin__ in (Dict, dict):
            key_type, val_type = item_type.__args__
            embedded_dict = True

        for value in lst:
            if value is None:
                if optional or item_type is Any:
                    ret_lst.append(None)
                else:
                    raise SystemLinkException.from_name(
                        'SkylineWebServices.InvalidJsonDataTypeForKey', args=[cls.__name__]
                    )
            elif embedded_list:
                ret_lst.append(cls._from_embedded_list(value, item_type))  # pylint: disable=protected-access
            elif embedded_dict:
                ret_lst.append(cls._from_embedded_dict(value, key_type, val_type))  # pylint: disable=protected-access
            elif item_type is Any:
                ret_lst.append(value)
            elif item_type is datetime:
                ret_lst.append(to_datetime(value))
            elif hasattr(item_type, 'from_dict'):
                ret_lst.append(item_type.from_dict(value))
            else:
                ret_lst.append(item_type(value))
        return ret_lst

    @classmethod
    def _from_embedded_dict(
            cls,
            dct: Dict[Any, Any],
            key_type: type,
            val_type: type) -> Dict[Any, Any]:  # pylint: disable=too-many-branches
        """
        Performs deserialization of an embedded dictionary.

        :param dct: The embedded dictionary.
        :type dct: dict
        :param key_type: The type of each dictionary key.
        :type key_type: type
        :param val_type: The type of each dictionary value.
        :type val_type: type
        :return: A dictionary of deserialized objects meant to be used as
            constructor arguments for the parent class.
        :rtype: dict
        :raises SystemLinkException: if an error occurs.
        """
        ret_dct = {}

        val_type, optional = cls._get_real_type(val_type)

        embedded_list = False
        embedded_dict = False
        if hasattr(val_type, '__origin__') and val_type.__origin__ in (List, list):
            item_type = val_type.__args__[0]
            embedded_list = True
        elif hasattr(val_type, '__origin__') and val_type.__origin__ in (Dict, dict):
            key_type, val_type = val_type.__args__
            embedded_dict = True

        for key, value in dct.items():
            if value is None:
                if optional or val_type is Any:
                    ret_dct[key] = None
                else:
                    raise SystemLinkException.from_name(
                        'SkylineWebServices.InvalidJsonDataTypeForKey', args=[key]
                    )
            elif embedded_list:
                ret_dct[key] = cls._from_embedded_list(value, item_type)  # pylint: disable=protected-access
            elif embedded_dict:
                ret_dct[key] = cls._from_embedded_dict(value, key_type, val_type)  # pylint: disable=protected-access
            elif val_type is Any:
                ret_dct[key] = value
            elif val_type is datetime:
                ret_dct[key] = to_datetime(value)
            elif hasattr(val_type, 'from_dict'):
                ret_dct[key] = val_type.from_dict(value)
            else:
                ret_dct[key] = val_type(value)
        return ret_dct

    @classmethod
    def deserialize_value(cls, value: Any, type_: type, name=None) -> Any:  # pylint: disable=too-many-return-statements
        """
        Deserialize a single value.

        :param value: The value to deserialize.
        :type value: Any
        :param type_: The type of the value to deserialize.
        :type type_: Any
        :param name: The name of the value. Used in exception messages.
        :type name: str or None
        :return: An instance of the class of the deserialized value.
        :rtype: Any
        :raises SystemLinkException: if an error occurs.
        """
        if value is _Required:
            raise SystemLinkException.from_name(
                'SkylineWebServices.MissingRequiredJsonKey', args=[name]
            )
        real_type, optional = cls._get_real_type(type_)
        if value is None:
            if optional or real_type is Any:
                return None
            raise SystemLinkException.from_name(
                'SkylineWebServices.InvalidJsonDataTypeForKey', args=[name]
            )
        if hasattr(real_type, '__origin__') and real_type.__origin__ in (List, list):
            item_type = real_type.__args__[0]
            return cls._from_embedded_list(value, item_type)  # pylint: disable=protected-access
        if hasattr(real_type, '__origin__') and real_type.__origin__ in (Dict, dict):
            key_type, val_type = real_type.__args__
            return cls._from_embedded_dict(value, key_type, val_type)  # pylint: disable=protected-access
        if real_type is Any:
            return value
        if real_type is datetime:
            return to_datetime(value)
        if hasattr(real_type, 'from_dict'):
            return real_type.from_dict(value)
        return real_type(value)

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]) -> Any:
        """
        Creates an instance of the mixin client class from
        a serialized dictionary.

        :param dct: The serialized dictionary.
        :type dct: dict
        :return: An instance of the mixin client class.
        :rtype: object
        :raises SystemLinkException: if an error occurs.
        """
        args = []

        for base_name, attr_type, default in cls.ATTRIBUTE_MAP.values():
            value = dct.get(base_name, default)
            args.append(cls.deserialize_value(value, attr_type, name=base_name))

        return cls(*args)

    @classmethod
    def from_json(cls, json_str: str) -> Any:
        """
        Creates an instance of the mixin client class from
        a JSON serialized string.

        :param json_str: The JSON serialized string.
        :type json_str: str
        :return: An instance of the mixin client class.
        :rtype: object
        """
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def _map_to_embedded_list(
            cls,
            item: Any,
            convert_datetime: bool) -> Any:
        """
        Map function for use on an embedded list.

        :param item: The list item to be mapped.
        :type item: Any
        :param convert_datetime: When ``True``, will convert a
            :class:`datetime` object to a :class:`str`. When ``False``,
            no such conversion will occur.
        :return: The mapped item.
        :rtype: Any
        """
        if isinstance(item, list):
            return list(map(
                functools.partial(cls._map_to_embedded_list, convert_datetime=convert_datetime),
                item))
        if isinstance(item, dict):
            return dict(map(
                functools.partial(cls._map_to_embedded_dict, convert_datetime=convert_datetime),
                item.items()))
        if isinstance(item, datetime):
            if convert_datetime:
                return from_datetime(item)
            return item
        if hasattr(item, 'to_dict'):
            return item.to_dict()
        return item

    @classmethod
    def _map_to_embedded_dict(
            cls,
            key_val: Tuple[Any, Any],
            convert_datetime: bool) -> Tuple[Any, Any]:
        """
        Map function for use on an embedded dict.

        :param key_val: The dict key/value pair to be mapped.
        :type key_val: Tuple[Any, Any]
        :param convert_datetime: When ``True``, will convert a
            :class:`datetime` object to a :class:`str`. When ``False``,
            no such conversion will occur.
        :type convert_datetime: bool
        :return: The mapped key/value pair.
        :rtype: Tuple[Any, Any]
        """
        key, value = key_val
        if isinstance(value, list):
            return key, list(map(
                functools.partial(cls._map_to_embedded_list, convert_datetime=convert_datetime),
                value))
        if isinstance(value, dict):
            return key, dict(map(
                functools.partial(cls._map_to_embedded_dict, convert_datetime=convert_datetime),
                value.items()))
        if isinstance(value, datetime):
            if convert_datetime:
                return key, from_datetime(value)
            return key, value
        if hasattr(value, 'to_dict'):
            return key, value.to_dict()
        return key, value

    @classmethod
    def serialize_value(  # pylint: disable=too-many-return-statements
            cls,
            value: Any,
            convert_datetime: bool = True) -> Any:
        """
        Serialize a single value to Python structures.

        :param value: The value to serialize.
        :type value: Any
        :param convert_datetime: When ``True``, will convert a
            :class:`datetime` object to a :class:`str`. When ``False``,
            no such conversion will occur.
        :type convert_datetime: bool
        :return: An instance of the class of the deserialized value.
        :rtype: Any
        :raises SystemLinkException: if an error occurs.
        """
        if value is None:
            return None
        if isinstance(value, list):
            return list(map(
                functools.partial(
                    cls._map_to_embedded_list, convert_datetime=convert_datetime
                ), value))
        if isinstance(value, dict):
            return dict(map(
                functools.partial(
                    cls._map_to_embedded_dict, convert_datetime=convert_datetime
                ), value.items()))
        if isinstance(value, datetime):
            if convert_datetime:
                return from_datetime(value)
            return value
        if hasattr(value, 'to_dict'):
            return value.to_dict()
        return value

    def to_dict(self, convert_datetime: bool = True) -> Dict[str, Any]:
        """
        Serializes the mixin client class to a dictionary.

        :param convert_datetime: When ``True``, will convert a
            :class:`datetime` object to a :class:`str`. When ``False``,
            no such conversion will occur.
        :type convert_datetime: bool
        :return: The serialized dictionary.
        :rtype: dict
        """
        result = {}

        for attr, (base_name, attr_type, default) in self.ATTRIBUTE_MAP.items():
            value = getattr(self, attr)
            if value is None:
                # If the value is None, omit it if it isn't a required
                # attribute.
                if default is _Required:
                    # Ensure that None is valid for this required attribute.
                    attr_type, optional = self._get_real_type(attr_type)
                    if optional is False and attr_type is not Any:
                        raise SystemLinkException.from_name(
                            'SkylineWebServices.InvalidJsonDataTypeForKey', args=[base_name]
                        )
                    result[base_name] = None
            else:
                result[base_name] = self.serialize_value(value, convert_datetime=convert_datetime)

        return result

    def to_json(self) -> str:
        """
        Serializes the mixin client class to a JSON string.

        :return: The serialized JSON string.
        :rtype: str
        """
        return json.dumps(self.to_dict(), separators=(',', ':'))
