# -*- coding:utf-8 -*-
import Constant
from Import import ImportUtils


def importTest():
    importUtils = ImportUtils()
    xlsPath = "../test/Output_Test.xls"
    filePath = "../test/values/strings_test.xml"
    importUtils.xls2xml(xlsPath, filePath, "en", None)


def main():
    Constant.Config.import_start_col = 5
    Constant.Config.import_base_xml = False
    Constant.Config.support_custom_ph_rule = True

    importTest()


main()
