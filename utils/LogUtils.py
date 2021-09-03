#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Constant import Config


class Log:
    """Log util"""

    current = ""
    # Log info green
    @staticmethod
    def info(msg):
        if Log.current != "info":
            print('\033[32m')
            Log.current = "info"

        print(f'IFNO: {msg}')
        # print('\033[34m' + msg)

        # Log info blue

    # @staticmethod
    # def infoln(msg):
    #     # print('\033[34m')
    #     self.info('\n'+msg)

    # Log error red
    @staticmethod
    def error(msg):
        if Log.current != "error":
            print('\033[31m')
            Log.current = "error"
        print(f'ERROR: {msg}')
        # print('\033[31m' + msg)

    @staticmethod
    def warn(msg):
        if Log.current != "warn":
            print('\033[34m')
            Log.current = "warn"
        print(f'WARN: {msg}')
        # print('\033[31m' + msg)

    # Log debug white
    @staticmethod
    def debug(msg):
        if Config.isShowDebug:
            if Log.current != "debug":
                print('\033[37m')
                Log.current = "debug"
            print(f'DEBUG: {msg}')
            # print('\033[37m' + msg)


if __name__ == '__main__':
    Log.info("info")
    Log.debug("你好")
    Log.error("error")
    Log.warn("warn")
