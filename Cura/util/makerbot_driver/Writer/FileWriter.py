#-*- coding: utf-8 -*-
"""An implementation of s3g that writes s3g packets to a file.

Due to the nature of building to file, we cannot handle ANY Query commands.  Thus,
if a user tries to write a query command to file, we throw a AttemptedQueryCommand error.
"""
from __future__ import absolute_import
import logging

from . import AbstractWriter
import makerbot_driver


class FileWriter(AbstractWriter): #继承AbstractWriter类
    """ A file writer can be used to export an s3g payload stream to a file
    """
    def __init__(self, file, condition): #file 是文件对象
        """ Initialize a new file writer

        @param string file File object to write to.
        """
        super(FileWriter, self).__init__(file, condition)
        self.check_binary_mode()
        self._log = logging.getLogger(self.__class__.__name__)

    def close(self):
        with self._condition:
            if not self.file.closed: #判断是否关闭 
                self.file.close()

    def is_open(self):
        return not self.file.closed #是否open

    def check_binary_mode(self):# check file 是否 'wb' mode 打开
        mode = str(self.file.mode)
        if 'b' not in mode:
            raise makerbot_driver.Writer.NonBinaryModeFileError

    def send_action_payload(self, payload): #
        if self.external_stop:
            self._log.error('{"event":"external_stop"}')
            raise makerbot_driver.ExternalStopError
        self.check_binary_mode()
        with self._condition:
            self.file.write(bytes(payload))
