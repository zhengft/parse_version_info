#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import subprocess
from subprocess import PIPE, STDOUT
from typing import Tuple


def run_join(input: str, sep: str) -> Tuple:
    """执行run_join.awk。"""
    result = subprocess.run(
        [
            'awk', '-f', 'join.awk',
            '-f', os.path.join('tests', 'run_join.awk'),
            '-v', 'input={0}'.format(input),
            '-v', 'sep={0}'.format(sep)
        ],
        stdout=PIPE,
        stderr=STDOUT
    )
    ret = result.returncode
    stdout = result.stdout.decode()
    return ret, stdout


def test_join_01():
    """测试join函数。"""
    ret, stdout = run_join('aaa', '_')
    assert 0 == ret
    assert 'aaa' == stdout


def test_join_02():
    """测试join函数。"""
    ret, stdout = run_join('aaa bbb', '_')
    assert 0 == ret
    assert 'aaa_bbb' == stdout


def test_join_03():
    """测试join函数。切换sep。"""
    ret, stdout = run_join('aaa bbb', '-')
    assert 0 == ret
    assert 'aaa-bbb' == stdout


def test_join_04():
    """测试join函数。"""
    ret, stdout = run_join('aaa bbb ccc ddd', '_')
    assert 0 == ret
    assert 'aaa_bbb_ccc_ddd' == stdout


def test_join_ex_01():
    """测试join函数。入参为空"""
    ret, stdout = run_join('', '_')
    assert 0 == ret
    assert '' == stdout


def run_strip(input: str) -> Tuple:
    """执行run_strip.awk。"""
    result = subprocess.run(
        [
            'awk', '-f', 'strip.awk',
            '-f', os.path.join('tests', 'run_strip.awk'),
            '-v', 'input={0}'.format(input)
        ],
        stdout=PIPE,
        stderr=STDOUT
    )
    ret = result.returncode
    stdout = result.stdout.decode()
    return ret, stdout


def test_strip_01():
    """测试strip函数。"""
    ret, stdout = run_strip(' aaa')
    assert 0 == ret
    assert 'aaa' == stdout


def test_strip_02():
    """测试strip函数。"""
    ret, stdout = run_strip(' bbb')
    assert 0 == ret
    assert 'bbb' == stdout


def test_strip_03():
    """测试strip函数。"""
    ret, stdout = run_strip('  aaa')
    assert 0 == ret
    assert 'aaa' == stdout


def test_strip_04():
    """测试strip函数。"""
    ret, stdout = run_strip('aaa')
    assert 0 == ret
    assert 'aaa' == stdout


def test_strip_05():
    """测试strip函数。"""
    ret, stdout = run_strip('aaa ')
    assert 0 == ret
    assert 'aaa' == stdout


def test_strip_06():
    """测试strip函数。"""
    ret, stdout = run_strip('bbb ')
    assert 0 == ret
    assert 'bbb' == stdout


def test_strip_07():
    """测试strip函数。"""
    ret, stdout = run_strip('aaa  ')
    assert 0 == ret
    assert 'aaa' == stdout


def test_strip_08():
    """测试strip函数。"""
    ret, stdout = run_strip('  aaa  ')
    assert 0 == ret
    assert 'aaa' == stdout


def test_strip_09():
    """测试strip函数。"""
    ret, stdout = run_strip('  3.14  ')
    assert 0 == ret
    assert '3.14' == stdout