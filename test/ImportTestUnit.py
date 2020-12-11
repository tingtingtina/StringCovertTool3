# -*- coding:utf-8 -*-
from Import import ImportUtils


def main():
    importUtils = ImportUtils()
    # options = addParser()
    # importUtils.xls2xml_options(options)

    xlsPath = "StringCovertTool3/test/Output.xls"
    filePath ="StringCovertTool3/test/strings_me.xml"
    dirPath = "StringCovertTool3/test"
    importUtils.xls2xml(xlsPath, None, None, dirPath)
    # importUtils.xls2xml(xlsPath, filePath, "en", dirPath)


# 读取 xls
main()
