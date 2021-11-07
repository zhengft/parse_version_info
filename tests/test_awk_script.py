#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import subprocess
from subprocess import PIPE, STDOUT
from typing import Tuple


def check_compat(version: str, require: str) -> Tuple:
    """执行check_compat.awk。"""
    result = subprocess.run(
        [
            'awk', '-f', 'strip.awk',
            '-f', 'check_compat.awk',
            '-v', 'version={0}'.format(version),
            '-v', 'all_require={0}'.format(require)
        ],
        stdout=PIPE,
        stderr=STDOUT
    )
    ret = result.returncode
    stdout = result.stdout.decode()
    return ret, stdout


def test_check_compat_01():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='3.14')
    expected = 0, 'T'
    assert expected == result

def test_check_compat_02():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_03():
    """测试检查兼容性。"""
    result = check_compat('3.15', require='3.14')
    expected = 0, 'F'
    assert expected == result


def test_check_compat_06():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='3.14,3.15')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_07():
    """测试检查兼容性。"""
    result = check_compat('3.15', require='3.14,3.15')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_08():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='3.14, 3.15')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_09():
    """测试检查兼容性。"""
    result = check_compat('3.15', require='3.14, 3.15')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_10():
    """测试检查兼容性。"""
    result = check_compat('3.16', require='3.14, 3.15, 3.16')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_11():
    """测试检查兼容性。"""
    result = check_compat('3.14', require=' ')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_12():
    """测试检查兼容性。"""
    result = check_compat('3.14', require=',')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_13():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='.,.')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_14():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='., .')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_15():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='>=3.14')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_16():
    """测试检查兼容性。"""
    result = check_compat('3.15', require='>=3.14')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_17():
    """测试检查兼容性。"""
    result = check_compat('3.13', require='>=3.14')
    expected = 0, 'F'
    assert expected == result


def test_check_compat_18():
    """测试检查兼容性。"""
    result = check_compat('3.13', require='>=3.14, 3.13')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_19():
    """测试检查兼容性。"""
    result = check_compat('3.13', require='>=3.14, >=3.13')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_20():
    """测试检查兼容性。"""
    result = check_compat('3.14.1', require='>=3.14')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_21():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='>=3.14.1')
    expected = 0, 'F'
    assert expected == result


def test_check_compat_ge_10():
    """测试检查兼容性。"""
    result = check_compat('3.15.1', require='>=3.14')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_ge_11():
    """测试检查兼容性。"""
    result = check_compat('3.15', require='>=3.14.1')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_ge_12():
    """测试检查兼容性。"""
    # 代码中没有强转数字，也可以通过。
    # 字符串比较，"2">="14"
    # 怀疑split时被系统自动转化为int类型了。
    result = check_compat('3.2', require='>=3.14')
    expected = 0, 'F'
    assert expected == result


def test_check_compat_le_01():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='<=3.14')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_le_02():
    """测试检查兼容性。"""
    result = check_compat('3.15', require='<=3.14')
    expected = 0, 'F'
    assert expected == result


def test_check_compat_le_03():
    """测试检查兼容性。"""
    result = check_compat('3.13', require='<=3.14')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_le_04():
    """测试检查兼容性。"""
    result = check_compat('3.13', require='<=3.14')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_le_05():
    """测试检查兼容性。"""
    result = check_compat('3.14.1', require='<=3.14')
    expected = 0, 'F'
    assert expected == result


def test_check_compat_le_06():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='<=3.14.1')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_le_07():
    """测试检查兼容性。"""
    result = check_compat('3.13.1', require='<=3.14')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_le_08():
    """测试检查兼容性。"""
    result = check_compat('3.13', require='<=3.14.1')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_gt_01():
    """测试检查兼容性。"""
    result = check_compat('3.14', require='>3.14')
    expected = 0, 'F'
    assert expected == result


def test_check_compat_gt_02():
    """测试检查兼容性。"""
    result = check_compat('3.15', require='>3.14')
    expected = 0, 'T'
    assert expected == result


def test_check_compat_gt_03():
    """测试检查兼容性。"""
    result = check_compat('3.13', require='>3.14')
    expected = 0, 'F'
    assert expected == result