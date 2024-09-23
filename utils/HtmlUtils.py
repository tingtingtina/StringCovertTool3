import re


def change_str(base_str):
    """
    %1$s ==> $$1s
    %s ==> $$s
    :param base_str: format: %1$s or %s
    :return: format: $$1s or $$s
    """
    new_str = '$$'
    new_str += base_str[1]
    if len(base_str) == 4:
        new_str += base_str[3]
    return new_str


def reverse_change_str(base_str):
    """
    $$1s ==> %1$s
    $$s ==> %s
    :param base_str: format: $$1s or $$s
    :return: format: %1$s or %s
    """
    new_str = '%'
    new_str += base_str[2]
    if len(base_str) == 4:
        new_str += '$' + base_str[3]
    return new_str


def replace_str(base_str, change_word):
    """
    将base_str中需要替代的字符（change_word）替换成需要的格式
    :param base_str: 源字符串
    :param change_word: 需要替换的字符
    :return: 转换后的字符串
    """
    new_str = ''
    if len(change_word) == 4:
        while change_word in base_str:
            start = base_str.find(change_word)
            new_str += base_str[:start] + change_str(base_str[start:start + 4])
            base_str = base_str[start + 4:]
    elif len(change_word) == 2:
        while change_word in base_str:
            start = base_str.find(change_word)
            new_str += base_str[:start] + change_str(base_str[start:start + 2])
            base_str = base_str[start + 2:]
    new_str += base_str
    return new_str


def reverse_replace_str(base_str, change_word):
    """
    将base_str中需要替代的字符（change_word）替换成需要的格式
    :param base_str: 源字符串
    :param change_word: 需要替换的字符
    :return: 转换后的字符串
    """
    new_str = ''
    if len(change_word) == 4:
        while change_word in base_str:
            start = base_str.find(change_word)
            new_str += base_str[:start] + reverse_change_str(base_str[start:start + 4])
            base_str = base_str[start + 4:]
    elif len(change_word) == 3:
        while change_word in base_str:
            start = base_str.find(change_word)
            new_str += base_str[:start] + reverse_change_str(base_str[start:start + 3])
            base_str = base_str[start + 3:]
    new_str += base_str
    return new_str


def convert_str(str):
    """
    转换字符串
    :param str: 源字符串
    :return: 转换后的字符串
    """
    # str = '<a helf="www.baidu.com">你好</a>啊，<font>中国</font>'

    # 用正则匹配出<></>格式的字符串，添加新标签更新到原来位置上
    # 找到标签内内容
    pattern = re.compile(r'<[^/].*?>(.*?)</')
    res = pattern.findall(str)

    # 去标签
    pattern2 = re.compile(r'<[^>]+>')
    res2 = pattern2.sub('', str)
    # print(res)
    # print(res2)

    result = res2
    for content in res:
        # print(content)
        result = result.replace(content, '<HH>'+content+'</HH>')
        # print(result)

    return result


def reverse_convert_str(base_str, str) -> str:
    """
    转换字符串
    :param base_str: 基础参考字符串
    :param str: 源字符串
    :return: 转换后的字符串
    """


    # 用正则匹配出$$1s格式的字符串，并替换
    pattern = re.compile(r'\$\$\d[a-zA-Z]')
    replace_list = pattern.findall(base_str)
    temp_result = base_str
    for replace in replace_list:
        temp_result = reverse_replace_str(temp_result, replace)

    # 用正则匹配出$$s格式的字符串，并替换
    pattern2 = re.compile(r'\$\$[a-zA-Z]')
    replace_list2 = pattern2.findall(temp_result)
    new_result = temp_result
    for replace in replace_list2:
        new_result = reverse_replace_str(new_result, replace)
    return new_result


if __name__ == "__main__":
    """
    回复 <font color="#4C4C4C">我：</font> ==> 回复 <HH>我：</HH>
    
    重点关注<b>这个功能</b> ==> 重点关注<HH>这个功能</HH>
    
    """

    STR1 = '回复 <font color="#4C4C4C">我：</font>'
    STR2 = '重点关注<b>这个功能</b>'
    STR3 = '<a helf="www.baidu.com">你好</a>啊，<font>中国</font>'
    print(f'{STR1} 转换后结果 ===>\n{convert_str(STR1)}')
    print('-' * 50)
    print(f'{STR2} 转换后结果 ===>\n{convert_str(STR2)}')
    print('-' * 50)
    print(f'{STR3} 转换后结果 ===>\n{convert_str(STR3)}')
    print('-' * 50)

    REVERSE_STR1 = '<HH>我：</HH>'
    REVERSE_BASE_STR1 = '<HH>我：</HH>'
    # REVERSE_STR2 = '$$1s的车价值$$2d元,购买人数 $$3d, 占了%90'
    # REVERSE_STR3 = '$$s的车价值$$d'
    # print(f'{REVERSE_STR1} 反向转换后结果 ===>\n{reverse_convert_str(REVERSE_STR1)}')
    # print('-' * 50)
    # print(f'{REVERSE_STR2} 反向转换后结果 ===>\n{reverse_convert_str(REVERSE_STR2)}')
    # print('-' * 50)
    # print(f'{REVERSE_STR3} 反向转换后结果 ===>\n{reverse_convert_str(REVERSE_STR3)}')
