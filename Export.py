# -*- coding:utf-8 -*-
import re

from utils.ParseUtils import *
import pyexcelerate


# 单个文件：获取文件 key - value 分别存放在 excel表格指定列


class ExportUtils:

    def __init__(self):
        pass

    def xml2xls(self, xls_dir, input_dir):
        """
        xml 转换成 xls
        :param xls_dir: 表格所在目录，会主动在改目录下创建个 xls
        :param input_dir: xml 所在目录
        :return: 输出状态 Constant.Error
        """
        if not xls_dir or not os.path.exists(xls_dir):
            # 表格目录不存在
            Log.error(Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "excel dir").get_desc_en())
            return Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "excel dir")

        if not input_dir or not os.path.exists(input_dir):
            # xml 目录不存在
            Log.error(Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "xml dir").get_desc_en())
            return Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "xml dir")

        xlsPath = os.path.join(xls_dir, Constant.Config.export_excel_name)
        workbook = pyexcelerate.Workbook()
        ws = workbook.new_sheet('Sheet1')
        # row col content
        # write title: module key lan, begin from 1
        ws[1][1] = Constant.Config.moduleTitle
        ws[1][2] = Constant.Config.keyTitle
        ws[1][3] = Constant.Config.export_base_title

        # 获取某个文件夹的所有文件，作为标准 这里是 value-zh
        base_dir = os.path.join(input_dir, Constant.Config.export_base_dir)
        if not os.path.exists(base_dir):
            # 标准文件夹不存在
            Log.error(Constant.Error(Constant.ERROR_DIR_NOT_EXIST,
                                     "base_dir\nU can change base dir in Constant-->Config").get_desc_en())
            return Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "base_dir\nU can change base dir in Constant-->Config")
        #  os.walk(path)返回三个值：
        #  parent, 表示path的路径、
        #  dirnames, path路径下的文件夹的名字
        #  filenames path路径下文件夹以外的其他文件。
        Log.debug("input_dir ---> " + input_dir)
        sub_dir_names = []
        for _, dir_names, _ in os.walk(input_dir):
            if dir_names:
                sub_dir_names = dir_names
                break
        Log.debug("sub_dir_names-->")
        Log.debug(sub_dir_names)

        # 标题下一行写入数据
        row = 2
        # 标准文件夹下所有文件
        files = os.listdir(base_dir)
        Log.debug("标准文件夹下所有文件：")
        Log.debug(files)
        for filename in files:
            module_name = getModuleName(filename)
            if not module_name:
                continue
            Log.debug(f"{'-' * 30}")
            file_path = os.path.join(base_dir, filename)  # 文件路径
            base_dict = XMLParse.get_value_and_key(file_path)

            col = 4  # base_dic 去掉前三列
            # 开始找其他文件语言下的对应 module
            for dir_name in sub_dir_names:
                cur_dir_path = os.path.join(input_dir, dir_name)
                if cur_dir_path == base_dir:
                    continue  # 标准文件夹不处理

                # 当前文件夹的语言
                lan = getDirLan(input_dir, cur_dir_path)
                if not lan:  # 文件夹不符合规范不处理（values-lan 或 values）
                    continue
                else:
                    Log.debug(f"module_name:{module_name} lan:{lan}")

                # 获取其他按文件夹下的该文件路径
                cur_file = os.path.join(cur_dir_path, filename)
                if not os.path.exists(cur_file):
                    # 路径不存在，不处理，跳过
                    continue

                # 写标题(语言）
                ws[1][col] = lan
                cur_dict = XMLParse.get_value_and_key(cur_file)
                (base_dict, cur_dict) = sortDic(base_dict, cur_dict)
                writeDict(ws, cur_dict, row, col, None, False)  # 仅写 非标注value, base_dict 会被一直被更新，
                col += 1  # 写完非标准文件的内容，坐标右移（列+1）

            # 最后写 标准文件的 key（0）-values（1）
            writeDict(ws, base_dict, row, 1, module_name, True)

            row += len(base_dict)
            Log.debug("row = %s" % row)

        workbook.save(xlsPath)
        return Constant.Error(Constant.SUCCESS)

    def xml2xls_single(self, xls_dir, input_file_path):
        # type: (str, str) -> object
        if not xls_dir or not os.path.exists(xls_dir):
            Log.error(Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "excel dir").get_desc_en())
            return Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "excel dir")
        if not input_file_path or not os.path.exists(input_file_path):
            Log.error(Constant.Error(Constant.ERROR_XML_FILE_NOT_EXIST).get_desc_en())
            return Constant.Error(Constant.ERROR_XML_FILE_NOT_EXIST)

        xlsPath = os.path.join(xls_dir, Constant.Config.export_excel_name)
        workbook = pyexcelerate.Workbook()
        ws = workbook.new_sheet('Sheet1')
        # row col content
        ws[1][1] = Constant.Config.keyTitle
        dic = XMLParse.get_value_and_key(input_file_path)
        writeDict(ws, dic, 2, 1, None, True)
        workbook.save(xlsPath)
        Log.debug(Constant.Error(Constant.SUCCESS).get_desc_en())
        return Constant.Error(Constant.SUCCESS)


def getModuleName(xml_file_name):
    """
    通过文件名获取 moduleName
    :param xml_file_name:文件名
    :return:去除 xml的文件名，比如 string.xml, 返回 strings
    """
    m = re.search('(.*?).xml', xml_file_name)
    module_name = ''
    if m:
        module_name = m.group(1)
        # print module_name
    return module_name


def getDirLan(input_dir, dir_path):
    """
    子文件夹为 values 时默认为 en
    :param input_dir: 目标文件夹（包含这 values等文件夹的路径）
    :param dir_path: 子文件夹路径 一般 是 path/values-zh 等
    :return str 文件夹表示的语言 比如 values-zh 语言为 zh
    """
    lan = ""
    if dir_path == os.path.join(input_dir, "values"):
        lan = "en"
    else:
        dirSplit = dir_path.split('values-')
        if len(dirSplit) > 1:
            lan = dirSplit[1]
        else:
            # cur_dir_path 文件夹不符合规则
            pass
    return lan


def writeDict(ws, dic, start_row, col, module, isKeepKey):
    """
    :param ws: workSheet
    :param dic:要写入的 dic 数据
    :param start_row:从哪一行开始写
    :param col: 从那一列开始写
    :param module:
    :param isKeepKey: 是否保留key，true：写key-value，false：写value
    """
    row = start_row
    for (key, value) in dic.items():
        if value == "ERROR":
            Log.warn(f"{key}:ERROR")
        else:
            Log.info(f"{key}:{value}")
        if isKeepKey:
            if module:
                ws[row][col] = module
                ws[row][col + 1] = key
                ws[row][col + 2] = value
            else:
                ws[row][col] = key
                ws[row][col + 1] = value
        else:
            ws[row][col] = value
        row += 1


def sortDic(base_dict, dict2):
    """
    dic2 根据 base_dict key 的顺序排序，如果 dict2 中的 key 不在 base_dict 中存在，则添加至 base_dict 最后
    :param base_dict: 目标 key 顺序
    :param dict2:
    :return:
    """
    result_dict = collections.OrderedDict()
    dict2_temp = dict2.copy()
    for (key, value) in base_dict.items():
        isMatch = False
        for (temp_key, temp_value) in dict2.items():
            if key == temp_key:
                isMatch = True
                result_dict[key] = temp_value
                del dict2_temp[key]
        if not isMatch:  # 循环结束，没有找到
            result_dict[key] = ""
    if len(dict2_temp) != 0:
        for (key, value) in dict2_temp.items():
            result_dict[key] = value
            base_dict[key] = ""
    return base_dict, result_dict
