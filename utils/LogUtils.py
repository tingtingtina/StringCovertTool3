#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

from loguru import logger

from Constant import Config


class Log:
    """Log util"""

    current = ""
    # Log info green
    @staticmethod
    def debug(msg):
        # if Log.current != "info":
        #     print('\033[32m')
        #     Log.current = "info"
        #
        # print(f'DEBUG: {msg}')
        logger.debug(msg)

    # Log error red
    @staticmethod
    def error(msg):
        # if Log.current != "error":
        #     print('\033[31m')
        #     Log.current = "error"
        # print(f'ERROR: {msg}')
        logger.error(msg)

    @staticmethod
    def warn(msg):
        # if Log.current != "warn":
        #     print('\033[34m')
        #     Log.current = "warn"
        # print(f'WARN: {msg}')
        logger.warning(msg)

    # Log info white
    @staticmethod
    def info(msg):
        if Config.isShowInfo:
            logger.info(msg)
        #     if Log.current != "debug":
        #         print('\033[37m')
        #         Log.current = "debug"
        #     print(f'INFO: {msg}')


if __name__ == '__main__':
    Log.info("你好")
    Log.debug("debug")
    Log.warn("warn")
    Log.error("error")