#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Log:
    """Log util"""

    current = ""
    # Log info green
    @staticmethod
    def info(msg):
        if Log.current != "info":
            print('\033[32m')
            Log.current = "info"

        print(msg)
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
        print(msg)
        # print('\033[31m' + msg)

    # Log debug white
    @staticmethod
    def debug(msg):
        if Log.current != "debug":
            print('\033[37m')
            Log.current = "debug"
        print(msg)
        # print('\033[37m' + msg)


if __name__ == '__main__':
    Log.infoln("info")
    Log.debug("你好")
    Log.debug("nihao")
    Log.info("info")