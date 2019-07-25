# -*- coding: utf-8 -*-
"""
Implementation of 'GenericResponse' class
"""
from __future__ import absolute_import

# Import python libs
import sys

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.response_message import ResponseMessage
from systemlink.messagebus.message_header import JSON_MESSAGE_CONTENT_TYPE
# pylint: enable=import-error


class GenericResponse(ResponseMessage):
    """
    Generic Response.

    A response message that is genericized so that the body is represented as
    bytes.
    """
    def __init__(self, header, body):
        """
        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The raw message body.
        :type body: bytes or bytearray
        """
        self._request_name = body['RequestName']
        super(GenericResponse, self).__init__(header, body)

    @classmethod
    def from_routing_source(cls, routing_source, error=None):
        """
        Create a GenericResponse object based on routing source.

        :param routing_source: A message to use to identify
            the routing information for this response message.
        :type routing_source: systemlink.messagebus.message_base.MessageBase
        :param error: Optional error information to transfer to this response
            message.
        :type error: systemlink.messagebus.error.Error or None
        :return: A :class:`GenericResponse` object with the routing
            information and optionally error information set.
        :rtype: GenericResponse
        """
        instance = super(GenericResponse, cls).from_message_name_content_type_routing_param(
            cls.__name__,
            JSON_MESSAGE_CONTENT_TYPE,
            routing_source.reply_to
        )
        instance._request_name = routing_source.message_name  # pylint: disable=protected-access
        instance.error = error
        instance.correlation_id = routing_source.correlation_id
        return instance

    @property
    def request_name(self):
        """
        Get the request name.

        :return: The request name.
        :rtype: str
        """
        return self._request_name

    @property
    def message_body_as_bytes(self):
        """
        Get the message body in a raw bytes form.

        :return: The message body as bytes.
        :rtype: bytes
        """
        body = '{\"RequestName\":\"' + self._request_name + '\"}'
        if sys.version_info[0] < 3:
            # Python 2 does not support 'bytes'.
            return bytearray(body, 'utf-8')
        return bytes(body, 'utf-8')
