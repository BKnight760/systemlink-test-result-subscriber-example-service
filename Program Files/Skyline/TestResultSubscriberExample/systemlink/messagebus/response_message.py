# -*- coding: utf-8 -*-
"""
Implementation of 'ResponseMessage' class
"""
from __future__ import absolute_import

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.message_base import MessageBase
# pylint: enable=import-error

# pylint: disable=missing-docstring


class ResponseMessage(MessageBase):  # pylint: disable=too-few-public-methods
    """
    Response Message

    A message meant to be sent as a response to
    a RequestMessage.
    """
    def __init__(self, header, body):  # pylint: disable=useless-super-delegation
        """
        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The raw message body.
        :type body: bytes
        """
        super(ResponseMessage, self).__init__(
            header,
            body
        )
