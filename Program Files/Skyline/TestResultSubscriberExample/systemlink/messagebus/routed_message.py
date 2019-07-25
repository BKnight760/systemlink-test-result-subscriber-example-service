# -*- coding: utf-8 -*-
"""
Implementation of 'RoutedMessage' class
"""
from __future__ import absolute_import

# Import python libs

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.message_base import MessageBase
# pylint: enable=import-error


class RoutedMessage(MessageBase):  # pylint: disable=too-few-public-methods
    """
    Routed Message

    A message meant to be routed by the given header.
    Defaults to ignore responses.
    """
    def __init__(self, header, body):  # pylint: disable=useless-super-delegation
        """
        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The raw message body.
        :type body: bytes
        """
        if header:
            header.ignore_response = True
        super(RoutedMessage, self).__init__(
            header,
            body
        )
