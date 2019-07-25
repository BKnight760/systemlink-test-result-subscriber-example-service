# -*- coding: utf-8 -*-
"""
Implementation of 'AmqpConfigurationManager' class
"""
from __future__ import absolute_import

# Import python libs
import codecs
import os
import os.path
import json

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.amqp_configuration import (
    AmqpConfiguration, SKYLINE_LOCALHOST_CONFIGURATION_ID,
    SKYLINE_MASTER_CONFIGURATION_ID
)
from systemlink.messagebus.constants import Environment
from systemlink.messagebus.exceptions import SystemLinkException
from systemlink.messagebus.paths import get_skyline_configurations_directory
from systemlink.messagebus.utils import is_windows
# pylint: enable=import-error

_TEMP_CERT_PATH = '/run/systemlink/certs/amqp.crt'


class AmqpConfigurationManager(object):
    """
    Factory for AMQPConfiguration objects.
    """
    _instance = None

    def __init__(self, id_=None, enable_fallbacks=True):
        """
        :param id_: The configuration ID to use or ``None`` to use
            the default configuration.
        :type id_: str or None
        :param enable_fallbacks: If ``True`` and the desired configuration
            ID is not found, will fall back to the default configuration.
            If ``False`` and the desired configuration is not found, will
            raise a :class:`systemlink.messagebus.exceptions.SystemLinkException`.
        :type enable_fallbacks: bool
        """
        self._closing = False
        self._configurations = {}
        self._read_file_set = set()
        self._configurations = self._read_configurations()
        self._default_configuration = self._get_configuration_helper(
            id_, enable_fallbacks, False
        )

    def __del__(self):
        self.close()

    def close(self):
        """
        Close this instance of :class:`AmqpConfigurationManager`.
        """
        if self._closing:
            return
        self._closing = True
        cls = self.__class__
        if cls._instance == self:  # pylint: disable=protected-access
            cls._instance = None  # pylint: disable=protected-access

    @classmethod
    def shutdown(cls):
        """
        If a singleton instance of :class:`AmqpConfigurationManager` exists,
        close and remove it.
        """
        if cls._instance:
            cls._instance.close()
            cls._instance = None

    @classmethod
    def get_instance(cls):
        """
        Obtain a singleton instance of :class:`AmqpConfigurationManager`.
        """
        if cls._instance is None:
            cls._instance = cls(None, True)
        return cls._instance

    @classmethod
    def get_configuration(cls, id_=None, enable_fallbacks=True, refresh=True):
        """
        Obtain an instance of
        :class:`systemlink.messagebus.amqp_configuration.AmqpConfiguration`
        from the singleton instance of :class:`AmqpConfigurationManager`.

        :param id_: The configuration ID to use or ``None`` to use
            the default configuration.
        :type id_: str or None
        :param enable_fallbacks: If ``True`` and the desired configuration
            ID is not found, will fall back to the default configuration.
            If ``False`` and the desired configuration is not found, will
            raise a :class:`systemlink.messagebus.exceptions.SystemLinkException`.
        :type enable_fallbacks: bool
        :param refresh: If ``True``, will refresh the selected configuration
            if it has changed since it was last loaded. If ``False``, will not
            refresh and could potentially use stale data.
        :type refresh: bool
        """
        instance = cls.get_instance()
        if id_ is None:
            if refresh:
                instance._default_configuration.refresh()  # pylint: disable=protected-access
            return instance._default_configuration  # pylint: disable=protected-access
        return instance._get_configuration_helper(id_, enable_fallbacks, refresh)  # pylint: disable=protected-access

    def _get_configuration_helper(self, id_, enable_fallbacks, refresh):
        """
        Helper function to obtain an instance of
        :class:`systemlink.messagebus.amqp_configuration.AmqpConfiguration`.

        :param id_: The configuration ID to use or ``None`` to use
            the default configuration.
        :type id_: str or None
        :param enable_fallbacks: If ``True`` and the desired configuration
            ID is not found, will fall back to the default configuration.
            If ``False`` and the desired configuration is not found, will
            raise a :class:`systemlink.messagebus.exceptions.SystemLinkException`.
        :type enable_fallbacks: bool
        :param refresh: If ``True``, will refresh the selected configuration
            if it has changed since it was last loaded. If ``False``, will not
            refresh and could potentially use stale data.
        :type refresh: bool
        """
        if refresh:
            # Check for new files
            self._configurations.update(
                self._read_configurations(only_new_files=True)
            )

        selected_amqp_configuration = None
        if not id_:
            selected_amqp_configuration = self._fallback()
            if selected_amqp_configuration is None:
                raise SystemLinkException.from_name('Skyline.NoSkylineConfigurations')
        else:
            selected_amqp_configuration = self._configurations.get(id_)
            if selected_amqp_configuration is None:
                if enable_fallbacks:
                    selected_amqp_configuration = self._fallback()
                    if selected_amqp_configuration is None:
                        raise SystemLinkException.from_name('Skyline.NoSkylineConfigurations')
                else:
                    raise SystemLinkException.from_name('Skyline.NoSkylineConfigurations')
        if refresh:
            selected_amqp_configuration.refresh()
        return selected_amqp_configuration

    def _read_config_file(self, file_path):
        """
        Read the configuration file.

        :param file_path: Path to the configuration file.
        :type file_path: str
        :return: A tuple containging the configuration ID and a
             :class:`systemlink.messagebus.amqp_configuration.AmqpConfiguration`
             object containing the configuration information.
        :rtype: tuple(str, systemlink.messagebus.amqp_configuration.AmqpConfiguration)
            or tuple(None, None)
        """
        last_modifed_time = os.path.getmtime(file_path)
        with codecs.open(file_path, 'r', encoding='utf-8-sig') as fp_:
            configuration = json.loads(fp_.read())

        if 'Id' in configuration:
            configuration_id = configuration['Id'].lower()
            if configuration_id in self._configurations:
                raise SystemLinkException.from_name('Skyline.DuplicateConfigurationId')
            amqp_config = AmqpConfiguration(
                file_path, configuration, last_modifed_time
            )
            return configuration_id, amqp_config
        return None, None

    @staticmethod
    def _read_configurations_from_env():  # pylint: disable=too-many-locals
        """
        Attempt to read a configuration by reading the environment variables.

        :return: A dictionary with key of the configuration ID and value
             an instance of
             :class:`systemlink.messagebus.amqp_configuration.AmqpConfiguration`.
             Will return an empty dictionary if there is no
             configuration in the environment variables.
        :rtype: dict(str, systemlink.messagebus.amqp_configuration.AmqpConfiguration)
        """
        configurations = {}
        host = os.environ.get(Environment.HOST)
        if not host:
            return configurations
        port = os.environ.get(Environment.PORT)
        exchange = os.environ.get(Environment.EXCHANGE)
        user = os.environ.get(Environment.USER)
        password = os.environ.get(Environment.PASSWORD)
        cert = os.environ.get(Environment.CERTIFICATE)
        cert_path = os.environ.get(Environment.CERTIFICATE_PATH)

        # The certificate is optional.
        if not port or not exchange or not user or password is None:
            return configurations

        actual_cert_path = None
        if cert_path:
            actual_cert_path = cert_path
        elif cert:
            if is_windows():
                raise NotImplementedError(
                    'Passing a TLS certificate via the environment is not supported on Windows'
                )
            temp_cert_dir = os.path.dirname(_TEMP_CERT_PATH)
            if not os.path.isdir(temp_cert_dir):
                os.makedirs(temp_cert_dir)
            with open(_TEMP_CERT_PATH, 'w') as fp_:
                fp_.write(cert)
            actual_cert_path = _TEMP_CERT_PATH

        try:
            port_num = int(port)
        except (TypeError, ValueError):
            raise SystemLinkException.from_name('Skyline.FailedToParse')

        configuration = {
            'Id': 'skyline_localhost',
            'DisplayName': 'Local',
            'ConnectionType': 'Local',
            'ExchangeName': exchange,
            'Host': host,
            'Port': port_num,
            'User': user,
            'Password': password,
            'UseTls' : actual_cert_path is not None,
            'TlsServerName': host if actual_cert_path is not None else None,
            'CertPath': actual_cert_path
        }

        amqp_config = AmqpConfiguration(None, configuration)
        configurations[SKYLINE_LOCALHOST_CONFIGURATION_ID] = amqp_config
        return configurations

    def _read_configurations(self, only_new_files=False):
        """
        Read configurations by reading all '.json' files in the
        configuration directory as well as the environment variables.

        :param only_new_files: If ``True``, read only files not read since
            last scan.
        :type only_new_files: bool
        :return: A dictionary with key of the configuration ID and value
             an instance of
             :class:`systemlink.messagebus.amqp_configuration.AmqpConfiguration`.
        :rtype: dict(str, systemlink.messagebus.amqp_configuration.AmqpConfiguration)
        """
        configurations = self._read_configurations_from_env()
        path = get_skyline_configurations_directory()
        if not os.path.exists(path):
            if configurations:
                return configurations
            raise SystemLinkException.from_name('Skyline.NoSkylineConfigurations')

        only_files = [file_name for file_name in os.listdir(path)
                      if os.path.isfile(os.path.join(path, file_name))]
        for file_name in only_files:
            file_path = os.path.join(
                path,
                file_name
            )
            if file_name.endswith('.json'):
                if not only_new_files or file_path not in self._read_file_set:
                    # Read .json configuration file
                    configuration_id, amqp_config = self._read_config_file(file_path)
                    if configuration_id is not None:
                        configurations[configuration_id] = amqp_config
                        self._read_file_set.add(file_path)

        return configurations

    def _fallback(self):
        """
        Helper function to facilitate falling back on the default configuration
        ID when the desired ID is not available.
        """
        if SKYLINE_LOCALHOST_CONFIGURATION_ID in self._configurations:
            return self._configurations[SKYLINE_LOCALHOST_CONFIGURATION_ID]
        return self._configurations.get(
            SKYLINE_MASTER_CONFIGURATION_ID,
            None
        )
