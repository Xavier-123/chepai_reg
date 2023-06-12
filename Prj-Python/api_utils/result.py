#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file         :  result.py
@introduction :  
"""

"""状态码枚举类

author: Jill

usage：
    结构为：错误枚举名-错误码code-错误说明message
    # 打印状态码信息
    code = Status.OK.get_code()
    print("code:", code)
    # 打印状态码说明信息
    msg = Status.OK.get_msg()
    print("msg:", msg)
    # 打印状态码
    value = Status.OK.get_value()
    print("value:", value)
    # 遍历枚举
    for status in Status:
        print(status.name, "---", status.value)
"""
from enum import Enum, unique


class Code(object):
    OK = 0
    InternalError = 1  # 内部错误
    InvalidParameter = 2  # 无效参数，请检查参数是否正确
    Recognition_Error = 3  # 模型识别失败


@unique
class Status(Enum):
    OK = {Code.OK: "成功"}
    INVALID_PARAM = {Code.InvalidParameter: "无效参数，请检查参数是否正确"}
    INTERNALERROR = {Code.InternalError: "异常"}
    RECOGNITION_ERROR = {Code.Recognition_Error: "模型识别识别"}

    def get_code(self):
        """
        根据枚举名称取状态码code
        :return: 状态码code
        """
        return list(self.value.keys())[0]

    def get_msg(self):
        """
        根据枚举名称取状态说明message
        :return: 状态说明message
        """
        return list(self.value.values())[0]

    def get_value(self):
        """
        根据枚举名称取状态值
        :return: 状态值
        """

        return str(self.value)


class result(object):
    def __init__(self, isSuc, msg, res, code):
        self.isSuc = isSuc
        self.code = code
        self.msg = msg
        self.res = res
