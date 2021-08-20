# -*- coding: UTF-8 -*-

import xlrd
import sys
import xml.dom.minidom
import os.path

import Constant
from utils.LogUtils import Log
import collections


class XLSParse:

    # 打开Excel
    def open_excel(self, filePath):
        self.data = xlrd.open_workbook(filePath)

    # 根据sheet索引获取sheet内容,sheet索引从0开始
    def sheet_by_index(self, index):
        return self.data.sheet_by_index(index)

    # 根据sheet名称获取sheet内容
    def sheet_by_name(self, name):
        return self.data.sheet_by_name(name)


class XMLParse:

    def __init__(self):
        pass

    @staticmethod
    def get_text_node_value(string_node):
        """
        :param string_node: string 结点
        :return: data 类型结点 text
        """
        if string_node.firstChild.nodeType == string_node.TEXT_NODE:
            # 获取某个元素节点的文本内容，先获取子文本节点，然后通过“data”属性获取文本内容
            if len(string_node.firstChild.data) != 0:
                value = string_node.firstChild.data
        elif string_node.firstChild.nodeType == string_node.ELEMENT_NODE:  # 元素节点
            data_node = string_node.getElementsByTagName("Data")  # 字符串样式
            # 处理 # CDATA
            if len(data_node) != 0 and data_node[0].firstChild.nodeType == data_node[0].CDATA_SECTION_NODE:
                data_value = data_node[0].firstChild.data
                value = data_value
                # value = "<Data><![CDATA[" + data_value + "]]</>"
        return value

    @staticmethod
    def update_multi_xml_value(sub_dir_path, keys, values, modules):
        """
        遍历每个子目录下的文件，把每一种语言的对应 module 下 key 将value 导入进去
        :param sub_dir_path: 目标子目录，比如 value-zh
        :param keys: 集合，目标目录下所有 key
        :param values: 集合，目标子目录下所有 value
        :param modules: 集合，目标子目录下每个 xml 文件的名字（不含.xml)，三个集合元素一一对应
        """
        Log.info("\n" + sub_dir_path + "\n")
        if len(modules) == 0:
            return

        # 先排序，把 excel 中的统一 module 排到一起
        # 排序，分块处理
        # 当前正在处理的 module
        current_module = modules[0]
        # 每个 module 中文案的数目
        module_length_list = []
        # 当前遍历的 module中文案的数目
        current_module_len = 0

        # 新 modules 集合，分块处理
        modules_new = []
        values_new = []
        keys_new = []
        for mid, module in enumerate(modules):
            if module is None or module == "":
                continue
            if current_module != module:
                module_length_list.append(current_module_len)
                current_module = module
                current_module_len = 0

            modules_new.append(module)
            values_new.append(values[mid])
            keys_new.append(keys[mid])
            current_module_len += 1

        module_length_list.append(current_module_len)

        start = 0
        end = 0
        for module_len in module_length_list:
            end += module_len
            subKeys = keys_new[start:end]
            subValues = values_new[start:end]
            module = modules_new[start]
            start += module_len
            filePath = sub_dir_path + module + ".xml"

            XMLParse.update_xml_value(filePath, subKeys, subValues)

    @staticmethod
    def update_xml_value(file_path, keys, values):
        """
        替换 xml 中 value
        :param file_path: xml 文件路径
        :param keys: xml 键值对 - key
        :param values: xml 键值对 - value
        :return:
        """
        Log.info("--- updating xml... \n%s" % file_path)
        if not os.path.exists(file_path):
            return
        # Log.info ("--- string ---")
        # 读取文档
        xml_doc = xml.dom.minidom.parse(file_path)

        if Constant.Config.import_base_xml:
            update_xml_base_xml(xml_doc, keys, values)
        else:
            update_xml_base_xls(xml_doc, keys, values)

        Log.info("--- array end ---\n")
        writeFile = open(file_path, 'wb')
        writeFile.write(xml_doc.toxml('utf-8'))
        writeFile.close()

    @staticmethod
    def get_value_and_key(file_path):
        """
        获取 xml 文件的 key - value
        :param file_path: 文件路径
        :return: dic[key]-value
        """
        if not file_path or not os.path.exists(file_path):
            Log.error("xml 文件不存在")
            return
        if Constant.Config.export_only_zh:
            # 仅中文，排除 values-zh 和 ja 文件夹（日语有太多中文，容易被误导出，因此先忽略掉）
            if "values-zh" in file_path or "values-ja" in file_path:
                return collections.OrderedDict()
        xml_doc = xml.dom.minidom.parse(file_path)
        nodes = xml_doc.getElementsByTagName('string')
        dic = collections.OrderedDict()
        for index, node in enumerate(nodes):
            if node is None or node.firstChild is None:
                continue

            if Constant.Config.export_apply_translatable:
                # ignore translatable
                translatable = node.getAttribute('translatable')
                if translatable is not None and translatable == "false":
                    continue

            key = node.getAttribute("name")

            value = XMLParse.get_text_node_value(node)
            if not Constant.Config.export_only_zh:
                dic[key] = value
            else:
                # 仅导出中文，是中文，则保存
                if is_chinese(value):
                    dic[key] = value

            # Log.info("%s : %s" % (key, value))

        array_nodes = xml_doc.getElementsByTagName("string-array")
        for array_node in array_nodes:
            key = array_node.getAttribute('name')
            child_nodes = array_node.getElementsByTagName('item')
            for idx, child_node in enumerate(child_nodes):
                newKey = convertStringArrayName(key, str(idx))
                value = XMLParse.get_text_node_value(child_node)
                if not Constant.Config.export_only_zh:
                    dic[newKey] = value
                else:
                    if is_chinese(value):
                        dic[newKey] = value
        return dic


def update_xml_base_xml(xml_doc, keys, values):
    # filename
    nodes = xml_doc.getElementsByTagName('string')
    for node in nodes:
        xmlKey = node.getAttribute("name")
        xmlValue = ""  # 该变量仅用于输出
        if node.firstChild is None:
            continue
        xmlValue = XMLParse.get_text_node_value(node)

        for index, key in enumerate(keys):
            if key == xmlKey and len(values[index]) != 0:
                if node.firstChild.nodeType == node.ELEMENT_NODE:
                    # 处理 CDATA
                    data_node = node.getElementsByTagName("Data")
                    data_node[0].firstChild.data = values[index]
                else:
                    node.firstChild.data = values[index]
                Log.debug("%s : %s -- >%s " % (xmlKey, xmlValue, values[index]))
    Log.info("--- string end ---\n")

    # 数组
    Log.info("--- array ---")
    array_nodes = xml_doc.getElementsByTagName('string-array')
    for array_node in array_nodes:
        xmlKey = array_node.getAttribute('name')
        Log.debug("xmlKey name -- > " + xmlKey)
        child_nodes = array_node.getElementsByTagName('item')
        for idx, child_node in enumerate(child_nodes):
            newKey = convertStringArrayName(xmlKey, str(idx))
            xmlValue = child_node.firstChild.data
            Log.debug("newKey: %s value: %s" % (newKey, xmlValue))
            for index, key in enumerate(keys):
                if key == newKey and len(values[index]) != 0:
                    child_node.firstChild.data = values[index]
                    Log.debug("%s : %s --> %s" % (newKey, xmlValue, child_node.firstChild.data))
    Log.info("--- array end ---\n")


def update_xml_base_xls(xml_doc, keys, values):
    # 如果不存在 xls 中的 key，则 append
    nodes = xml_doc.getElementsByTagName('string')
    for index, key in enumerate(keys):
        if len(values[index]) == 0 or isStringArrayKey(key) is not None:
            continue
        Log.debug("--xml key--" + key)
        for nodeIndex, node in enumerate(nodes):
            if isCDATAKey(key):
                # TODO
                continue
            else:
                xmlKey = node.getAttribute("name")
                xmlValue = XMLParse.get_text_node_value(node)
                if xmlKey == key:
                    if node.firstChild.nodeType == node.ELEMENT_NODE:
                        # 处理 CDATA
                        data_node = node.getElementsByTagName("Data")
                        data_node[0].firstChild.data = values[index]
                    else:
                        node.firstChild.data = values[index]
                    Log.debug("%s : %s -- >%s " % (xmlKey, xmlValue, values[index]))
                    break

            if nodeIndex == (len(nodes) - 1):
                # xml 中找不到 xls 中的key，xml 添加元素
                if isCDATAKey(key):
                    # CDATA
                    Log.debug("")
                else:
                    # 一般文本
                    newel = xml_doc.createElement("string")
                    newText = xml_doc.createTextNode(values[index])
                    newel.setAttribute('name', key)
                    newel.appendChild(newText)
                    xml_doc.documentElement.appendChild(newel)

    # 数组
    # Log.info("--- array ---")
    array_nodes = xml_doc.getElementsByTagName('string-array')
    for index, key in enumerate(keys):
        if len(values[index]) == 0:
            continue
        if isStringArrayKey(key) is None:
            continue

        Log.debug("--xml array key--" + key)
        arrayKey = isStringArrayKey(key)[0]
        arrayIndex = isStringArrayKey(key)[1]
        for nodeIndex, array_node in enumerate(array_nodes):
            xmlKey = array_node.getAttribute('name')
            if xmlKey == arrayKey:
                child_nodes = array_node.getElementsByTagName('item')
                for idx, child_node in enumerate(child_nodes):
                    tempKey = convertStringArrayName(xmlKey, str(idx))
                    xmlValue = child_node.firstChild.data
                    if tempKey == key:
                        child_node.firstChild.data = values[index]
                        Log.debug("%s : %s --> %s" % (tempKey, xmlValue, child_node.firstChild.data))
                        break

            # # 没有数组，则需要添加
            # newel = xml_doc.createElement("string-array")
            # newel.createElement("item")
            # newText = xml_doc.createTextNode(values[index])
            # newel.appendChild(newText)
            # Log.debug("--convert key--" + arrayKey)


def convertStringArrayName(key, index):
    """
    :param key: 字符串数组的key
    :param index: 数组item 索引，从 0开始
    :return: 返回每一条数组item 新key
    比如 array1 --> array1-INDEX-0
    """
    return key + "-INDEX-" + index


def isStringArrayKey(key):
    index = key.find('-INDEX-')
    if index > 0:
        arrayKey = key[0:index]
        arrayIndex = key[index:len(key)]
        return arrayKey, arrayIndex
    return None


def isCDATAKey(key):
    return False


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
