# -*- coding: utf-8 -*-
"""
Implementation of 'BroadcastMessage' class
"""
from __future__ import absolute_import

# Import python libs

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.message_base import MessageBase
# pylint: enable=import-error


class BroadcastMessage(MessageBase):  # pylint: disable=too-few-public-methods
    """
    Broadcast Message.

    Bundles a message that is to be broadcasted out
    to anyone who subscribes to the message.
    """
    def __init__(self, header, body):  # pylint: disable=useless-super-delegation
        """
        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The message body.
        :type body: bytes
        """
        super(BroadcastMessage, self).__init__(
            header,
            body
        )
