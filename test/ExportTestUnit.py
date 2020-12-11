# -*- coding:utf-8 -*-
from Export import ExportUtils


def main():
    exportUtils = ExportUtils()
    xls_dir = "StringCovertTool3/test"
    input_dir = xls_dir
    file_path = "StringCovertTool3/test/strings_me.xml"

    exportUtils.xml2xls(xls_dir, input_dir)
    # exportUtils.xml2xls_single(xls_dir, file_path)


# 读取 xls
main()
