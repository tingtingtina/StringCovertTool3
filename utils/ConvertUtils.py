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


def convert_str(base_str):
    """
    转换字符串
    :param base_str: 源字符串
    :return: 转换后的字符串
    """
    # 用正则匹配出%1$s格式的字符串，并替换
    pattern = re.compile(r'%\d\$[a-zA-Z]')
    replace_list = pattern.findall(base_str)
    temp_result = base_str
    for replace in replace_list:
        temp_result = replace_str(temp_result, replace)

    # 用正则匹配出%s格式的字符串，并替换
    pattern2 = re.compile(r'%[a-zA-Z]')
    replace_list2 = pattern2.findall(temp_result)
    new_result = temp_result
    for replace in replace_list2:
        new_result = replace_str(new_result, replace)
    return new_result


def reverse_convert_str(base_str) -> str:
    """
    转换字符串
    :param base_str: 源字符串
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
    %1$s的车价值%2$d元,购买人数 %3$d, 占了%%4$d  ==> $$1s的车价值$$2d元,购买人数 $$3d, 占了%$$4d
    %1$s的车价值%2$d元,购买人数 %3$d, %3$dD 占了%90 ==> $$1s的车价值$$2d元,购买人数 $$3d, 占了%90
    %s的车价值%d ==> $$s的车价值$$d
    """

    STR1 = '%1$s的车价值%2$d元,购买人数 %3$d, 占了%%4$d'
    STR2 = '%2$s的车价值%1$d元,购买人数 %3$d, 占了%90'
    STR3 = '%s的车价值%d'
    print(f'{STR1} 转换后结果 ===>\n{convert_str(STR1)}')
    print('-' * 50)
    print(f'{STR2} 转换后结果 ===>\n{convert_str(STR2)}')
    print('-' * 50)
    print(f'{STR3} 转换后结果 ===>\n{convert_str(STR3)}')
    print('-' * 50)

    REVERSE_STR1 = '$$1s的车价值$$2d元,购买人数 $$3d, 占了%$$4d'
    REVERSE_STR2 = '$$1s的车价值$$2d元,购买人数 $$3d, 占了%90'
    REVERSE_STR3 = '$$s的车价值$$d'
    print(f'{REVERSE_STR1} 反向转换后结果 ===>\n{reverse_convert_str(REVERSE_STR1)}')
    print('-' * 50)
    print(f'{REVERSE_STR2} 反向转换后结果 ===>\n{reverse_convert_str(REVERSE_STR2)}')
    print('-' * 50)
    print(f'{REVERSE_STR3} 反向转换后结果 ===>\n{reverse_convert_str(REVERSE_STR3)}')
