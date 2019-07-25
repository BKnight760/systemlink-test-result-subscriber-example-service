# -*- coding: utf-8 -*-
"""
Command line actions for the Test Result Subscriber Example.
"""
from __future__ import absolute_import, print_function

# Import python libs
import argparse
import logging
import sys
import time

# Import local libs
# pylint: disable=import-error
from systemlink.testresultsubscriberexampleservice.managed_service import TestResultSubscriberExampleService
# pylint: enable=import-error


LOG_LEVELS = {
    'all': logging.NOTSET,
    'debug': logging.DEBUG,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
    'info': logging.INFO,
    'warning': logging.WARNING
}

SORTED_LEVEL_NAMES = [
    log_item[0] for log_item in sorted(LOG_LEVELS.items(), key=lambda x: x[1])
]

DEFAULT_LOG_LEVEL = 'warning'

SERVICE_NAME = 'TestResultSubscriberExample'


def parse_args():
    """
    This will parse the command-line arguments passed in.
    Returns a Namespace object of the parsed command-line arguments.

    :return: A Namespace object of the parsed command-line arguments.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--log-level',
        dest='log_level',
        choices=SORTED_LEVEL_NAMES,
        default=DEFAULT_LOG_LEVEL,
        help='Console logging log level. One of {0}. Default: \'{1}\'.'.format(
            ', '.join([repr(l) for l in SORTED_LEVEL_NAMES]),
            DEFAULT_LOG_LEVEL)
    )
    parser.add_argument(
        '--logfile',
        dest='logfile',
        default='',
        help='Log file path to log messages to.'
    )
    parser.add_argument(
        '-s', '--silent',
        dest='silent',
        action='store_true',
        help='Silent mode'
    )
    parser.add_argument(
        '--standalone',
        dest='standalone',
        action='store_true',
        help='Run service in \"standalone\" mode. This is the mode where the '
             'service is not registered with the NI SystemLink Service Manager.'
    )
    args = parser.parse_args()
    return args


def setup_logging(args):
    """
    This will set up logging at the desired log level.

    :param args: A Namespace object of the parsed command-line arguments.
    :type args: argparse.Namespace
    """
    log_level = LOG_LEVELS[args.log_level]
    log = logging.getLogger()
    log.setLevel(log_level)

    # Create console handler and set level to debug
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to stream_handler
    stream_handler.setFormatter(formatter)

    # Add handler to logger
    log.addHandler(stream_handler)

    # Log to file if enabled
    if args.logfile:
        file_handler = logging.FileHandler(args.logfile)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)


def run_service(standalone, silent=False):
    """
    This will run the service.

    :param standalone: If ``True``, run in standalone mode. If ``False``,
        must be launched from within the Service Manager.
    :type standalone: bool
    :param silent: If ``False``, will print status to stdout/stderr.
        If ``True``, will not print status.
    :type silent: bool
    :return: The return code. ``0`` on success. Non-zero on failure.
    :rtype: int
    """
    try:
        with TestResultSubscriberExampleService(service_name=SERVICE_NAME, standalone=standalone) as service:
            shutdown_event = service.shutdown_event
            if silent:
                shutdown_event.acquire(True)
            else:
                print('Waiting for messages...', end='')
                while True:
                    time.sleep(1)
                    print('.', end='', flush=True)
                    if shutdown_event.acquire(False):
                        break
    except (KeyboardInterrupt, SystemExit):
        if not silent:
            print('Test Result Subscriber Example has stopped.')
    return 0


def main():
    """
    This is the main entry point for this script.
    """
    args = parse_args()
    setup_logging(args)

    retcode = 0
    # parse_args() will ensure that the command is a valid option.
    try:
        retcode = run_service(args.standalone, silent=args.silent)
    except Exception:  # pylint: disable=broad-except
        retcode = 2
        if not args.silent:
            # Raising the exception here will print exception info to
            # the console.
            raise

    if retcode != 0:
        sys.exit(retcode)


if __name__ == '__main__':
    main()
