# -*- coding:utf-8 -*-
from Export import ExportUtils
import Constant


def exportTestFile():
    # test 文件
    file_path = "../test/values-zh/strings_test.xml"
    xls_dir = "../test"
    ExportUtils().xml2xls_single(xls_dir, file_path)
    pass


def exportTestDir():
    # test 文件夹
    xls_dir = "../test"
    dirPath = "../test"
    ExportUtils().xml2xls(xls_dir, dirPath)
    pass


def exportNinebot():
    Constant.Config.export_excel_name = "Android_Output_1123.xls"
    xls_dir = "../test"
    dirPath = "/Users/liting/Documents/ninebotProject/ninebot-6(1)/commonres/src/main/res"
    ExportUtils().xml2xls(xls_dir, dirPath)
    pass


def main():

    # 仅导出中文
    Constant.Config.export_only_zh = False
    Constant.Config.export_base_title = "en"
    Constant.Config.export_base_dir = "values"
    Constant.Config.export_apply_translatable = True
    Constant.Config.export_excel_name = "Output_debug.xls"
    Constant.Config.support_custom_ph_rule = True
    Constant.Config.isShowInfo = False

    # exportTestDir()
    # exportTestFile()
    exportNinebot()
    

main()
