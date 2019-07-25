# -*- coding: utf-8 -*-
"""
Constants related to the SystemLink environment.
"""

NODE_NAME = 'SKYLINE_NODENAME'
SERVICE_GUID = 'SKYLINE_SERVICEGUID'
SERVICE_GROUP_NAME = 'SKYLINE_SERVICE_GROUP_NAME'

DEFAULT_SERVICE_GROUP_NAME = 'Default'


class Environment(object):  # pylint: disable=too-few-public-methods
    """
    SystemLink environment variables.
    """
    HOST = 'SYSTEMLINK_AMQP_HOST'
    PORT = 'SYSTEMLINK_AMQP_PORT'
    EXCHANGE = 'SYSTEMLINK_AMQP_EXCHANGE'
    USER = 'SYSTEMLINK_AMQP_USER'
    PASSWORD = 'SYSTEMLINK_AMQP_PASSWORD'
    CERTIFICATE = 'SYSTEMLINK_AMQP_CERT'
    CERTIFICATE_PATH = 'SYSTEMLINK_AMQP_CERT_PATH'
