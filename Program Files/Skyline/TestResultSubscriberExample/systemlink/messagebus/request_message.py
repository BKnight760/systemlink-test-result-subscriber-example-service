# -*- coding: utf-8 -*-
"""
Implementation of 'RequestMessage' class
"""
from __future__ import absolute_import

# Import python libs
import logging

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.message_base import MessageBase
# pylint: enable=import-error

# Set up logging
LOGGER = logging.getLogger(__name__)


class RequestMessage(MessageBase):  # pylint: disable=too-few-public-methods
    """
    Request Message

    A message meant to make a request so that a response may
    be returned.
    """
    def __init__(self, header, body):
        """
        :param header: The message header.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The raw message body.
        :type body: bytes
        """
        LOGGER.debug('RequestMessage __init__')
        super(RequestMessage, self).__init__(
            header,
            body
        )
