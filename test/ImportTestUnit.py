# -*- coding:utf-8 -*-
import Constant
from Import import ImportUtils


def importTest():
    importUtils = ImportUtils()
    xlsPath = "../test/Output_Test.xls"
    filePath = "../test/values/strings_test.xml"
    importUtils.xls2xml(xlsPath, filePath, "en", None)


def importNinebot():
    Constant.isShowInfo = True
    Constant.Config.import_base_xml = True
    Constant.Config.import_start_col = 4
    Constant.import_allow_none = False

    importUtils = ImportUtils()
    xlsPath = "/Users/liting/Downloads/Android_0601.xlsx"
    target_dir_path = "/Users/liting/Documents/ninebotProject/ninebot-6(1)/commonres/src/main/res"
    importUtils.xls2xml(xlsPath, None, None, target_dir_path)


def main():
    Constant.Config.import_start_col = 5
    Constant.Config.import_base_xml = False
    Constant.Config.support_custom_ph_rule = True

    # importTest()

    importNinebot()


main()
