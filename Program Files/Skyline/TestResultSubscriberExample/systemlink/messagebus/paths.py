# -*- coding: utf-8 -*-
"""
Collection of path-related functions.
"""
from __future__ import absolute_import

# Import python libs
import codecs
import os.path
import sys

# Import local libs
# pylint: disable=import-error
try:
    from systemlink.messagebus.utils import is_windows
except ImportError:
    # Import as relative libs (for relocatability)
    # Add the current directory to the search path.
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from utils import is_windows
    finally:
        # Remove the extra search path that we added to sys.path
        del sys.path[-1:]
# pylint: enable=import-error

_IS_LEGACY_LINUX = False

if is_windows():
    # pylint: disable=import-error
    import winreg
    # pylint: enable=import-error

    NI_INSTALLERS_REG_PATH = 'SOFTWARE\\National Instruments\\Common\\Installer'
    NI_INSTALLERS_REG_KEY_APP_DATA = 'NIPUBAPPDATADIR'
    NI_INSTALLERS_REG_KEY_SHARED = 'NISHAREDDIR64'

    def _get_ni_shared_dir():
        """
        Return the National Instruments Shared Application Directory.
        This looks like: 'C:\\Program Files\\National Instruments\\Shared'

        :return: The National Instruments Shared Application Directory.
        :rtype: str
        """
        with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                NI_INSTALLERS_REG_PATH,
                0,
                winreg.KEY_READ) as hkey:
            (shared_dir, _) = winreg.QueryValueEx(hkey, NI_INSTALLERS_REG_KEY_SHARED)
            return shared_dir

    def _get_ni_common_appdata_dir():
        """
        Return the National Instruments Common Application Data Directory.
        This looks like: 'C:\\ProgramData\\National Instruments'

        :return: The National Instruments Common Application Data Directory.
        :rtype: str
        """
        with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                NI_INSTALLERS_REG_PATH,
                0,
                winreg.KEY_READ) as hkey:
            (appdata_dir, _) = winreg.QueryValueEx(hkey, NI_INSTALLERS_REG_KEY_APP_DATA)
            return appdata_dir
else:
    # Linux
    _IS_LEGACY_LINUX = os.path.isdir('/etc/natinst/niskyline')


def get_application_directory():
    """
    Returns the directory where the Skyline binaries may be found.

    :return: Path to the Skyline application directory.
    :rtype: str
    """
    if is_windows():
        # Get Program Files directory
        ni_shared_path = _get_ni_shared_dir()
        path = os.path.join(
            ni_shared_path,
            'Skyline'
        )
        return path
    return '/usr/local/bin'


def get_application_data_directory():
    """
    Returns the directory where the Skyline data files may be found.

    :return: Path to the Skyline date file directory.
    :rtype: str
    """
    if is_windows():
        # Get APPDATA directory
        ni_appdata_path = _get_ni_common_appdata_dir()
        path = os.path.join(
            ni_appdata_path,
            'Skyline'
        )
        return path
    if _IS_LEGACY_LINUX:
        return '/etc/natinst/niskyline'
    return '/var/lib/systemlink'


def get_base_configuration_directory():
    """
    Returns the directory where the Skyline configuration files may be found.

    :return: Path to the Skyline configuration directory.
    :rtype: str
    """
    if is_windows():
        return get_application_data_directory()
    if _IS_LEGACY_LINUX:
        return '/etc/natinst/niskyline'
    return '/etc/systemlink'


def get_configuration_directory():
    """
    Returns the directory where the Skyline configuration files may be found.

    :return: Path to the Skyline configuration directory.
    :rtype: str
    """
    if is_windows():
        return os.path.join(get_base_configuration_directory(), 'Config')
    return os.path.join(get_base_configuration_directory(), 'config')


def get_log_directory():
    """
    Returns the directory where the Skyline log files may be found.

    :return: Path to the Skyline log directory.
    :rtype: str
    """
    if is_windows():
        return os.path.join(get_application_data_directory(), 'Logs')
    return '/var/log/systemlink'


def get_service_descriptor_install_directory():  # pylint: disable=invalid-name
    """
    Returns the directory where the service descriptors
    are added and removed during install time.

    :return: Path to the service descriptor install directory.
    :rtype: str
    """
    if is_windows():
        return os.path.join(
            get_base_configuration_directory(),
            'Install', 'Services', 'Descriptors'
        )
    return os.path.join(
        get_base_configuration_directory(),
        'install', 'services', 'descs'
    )


def get_skyline_configurations_directory():  # pylint: disable=invalid-name
    """
    Return path to the Skyline AMQP configurations directory.

    :return: Path to Skyline AMQP configurations directory.
    :rtype: str
    """
    if is_windows() or _IS_LEGACY_LINUX:
        return os.path.join(
            get_base_configuration_directory(),
            'SkylineConfigurations',
        )
    return os.path.join(
        get_base_configuration_directory(),
        'amqp_config',
    )


def get_skyline_localhost_file():
    """
    Return path to the Skyline Localhost AMQP credentials file.

    :return: Path to Skyline Localhost AMQP credentials file.
    :rtype: str
    """
    path = os.path.join(
        get_skyline_configurations_directory(),
        'skyline_localhost.json'
    )
    return path


def get_skyline_master_file():
    """
    Return path to the Skyline Master AMQP credentials file on the minion.

    :return: Path to Skyline Master AMQP credentials file.
    :rtype: str
    """
    path = os.path.join(
        get_skyline_configurations_directory(),
        'skyline_master.json'
    )
    return path


def load_utf8_file_to_string(filename):
    """
    Read the contents of a utf-8 based file and
    return that data as a string.

    :param filename: The input file path.
    :type filename: str
    :return: Contents of utf-8 based file.
    :rtype: str
    """
    with codecs.open(filename, 'r', encoding='utf-8-sig') as fp_:
        data = fp_.read()
    return data
