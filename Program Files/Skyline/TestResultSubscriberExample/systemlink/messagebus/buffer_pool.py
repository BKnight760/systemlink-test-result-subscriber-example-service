# -*- coding: utf-8 -*-
"""
Implementation of 'BufferPool' class
"""
from __future__ import absolute_import

# Import python libs
import sys

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.log_buffer import LogBuffer
if sys.version_info[0] < 3:
    from Queue import Queue, Empty
else:
    from queue import Queue, Empty
# pylint: enable=import-error


class BufferPool(object):  # pylint: disable=too-many-public-methods
    """
    Buffer Pool.

    A pool of buffers meant for Trace Logger logs.
    """
    def __init__(self):
        self._starting_buffer_pool_size = 10
        self._max_buffers_in_pool = 50
        self._pool = Queue(maxsize=self._max_buffers_in_pool)

        # Prime the pool with some buffers
        for _ in range(0, self._starting_buffer_pool_size):
            self._pool.put(LogBuffer())

    def return_buffer(self, buffer_):
        """
        Return a buffer to the pool.

        :param buffer_: The buffer that is no longer used to return to the
            buffer pool.
        :type buffer_: systemlink.messagebus.log_buffer.LogBuffer
        """
        buffer_.reset()
        if self._pool.qsize() < self._max_buffers_in_pool:
            self._pool.put(buffer_)

    def __len__(self):
        """
        Get the current size of the buffer pool.

        :return: The current size of the buffer pool.
        :rtype: int
        """
        return self._pool.qsize()

    def __bool__(self):
        """
        Get whether the buffer pool is not empty.

        :return: ``True`` if the buffer pool is not empty. ``False``
            otherwise.
        :rtype: bool
        """
        return not self._pool.empty()

    # Python 2 compatibilty.
    __nonzero__ = __bool__

    def get_buffer(self):
        """
        Get a buffer from the buffer pool. This will
        create a new buffer if the buffer pool is empty.

        :return: A free buffer from the buffer pool or a
                 new buffer if the buffer pool is empty.
        :rtype: systemlink.messagebus.log_buffer.LogBuffer
        """
        try:
            return self._pool.get_nowait()
        except Empty:
            return LogBuffer()
