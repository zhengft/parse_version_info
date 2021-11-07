#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import subprocess
from subprocess import PIPE, STDOUT
from typing import NamedTuple

import pytest


class RetOutvar(NamedTuple):
    ret: int
    outvar: str


def run_outvar(*args):
    """调用run_outvar.sh。"""
    result = subprocess.run(
        ['bash', os.path.join('tests', 'run_outvar.sh'), *args],
        stdout=PIPE,
        stderr=STDOUT
    )
    ret = result.returncode
    outvar = result.stdout.decode()
    return RetOutvar(ret, outvar)


def run_check(*args):
    """调用run_check.sh。"""
    result = subprocess.run(
        ['bash', os.path.join('tests', 'run_check.sh'), *args],
    )
    return result.returncode


class TestGetRequirePackages:

    def get_require_packages(self, version_info_path):
        """调用get_require_packages函数。"""
        return run_outvar('get_require_packages', version_info_path)

    def test_basic_01(self):
        """测试获取需要的包。"""
        ret_outvar = self.get_require_packages('version.01.info')

        expected = RetOutvar(0, 'driver')
        assert expected == ret_outvar

    def test_basic_02(self):
        """测试获取需要的包。"""
        ret_outvar = self.get_require_packages('version.02.info')

        expected = RetOutvar(0, 'driver operator')
        assert expected == ret_outvar

    def test_basic_03(self):
        """测试获取需要的包。"""
        ret_outvar = self.get_require_packages('version.03.info')

        expected = RetOutvar(0, 'driver cloud_component')
        assert expected == ret_outvar

    def test_basic_ex_01(self):
        """测试获取需要的包。version.info不存在。"""
        ret_outvar = self.get_require_packages('version.not_exists.info')

        expected = RetOutvar(1, '')
        assert expected == ret_outvar


class TestGetRequirePackageInfo:

    def get_require_package_info(self, version_info_path, pkg_name):
        """调用get_require_package_info函数。"""
        return run_outvar('get_require_package_info', version_info_path, pkg_name)

    def test_basic_01(self):
        """测试获取包依赖信息。"""
        ret_outvar = self.get_require_package_info('version.01.info', 'driver')
        expected = RetOutvar(0, '>=3.13, <=3.15, 3.19')
        assert expected == ret_outvar

    def test_basic_02(self):
        """测试获取包依赖信息。"""
        ret_outvar = self.get_require_package_info('version.02.info', 'operator')
        expected = RetOutvar(0, '3.14')
        assert expected == ret_outvar

    def test_basic_03(self):
        """测试获取包依赖信息。"""
        ret_outvar = self.get_require_package_info('version.03.info', 'cloud_component')
        expected = RetOutvar(0, '3.14')
        assert expected == ret_outvar

    def test_basic_04(self):
        """测试获取包依赖信息。包信息不存在"""
        ret_outvar = self.get_require_package_info('version.01.info', 'operator')
        expected = RetOutvar(0, '')
        assert expected == ret_outvar

    def test_basic_ex_01(self):
        """测试获取包依赖信息。version.info不存在。"""
        ret_outvar = self.get_require_package_info('version.not_exists.info', 'driver')

        expected = RetOutvar(1, '')
        assert expected == ret_outvar


class TestGetPackageVersion:

    def get_package_version(self, version_info_path):
        """调用get_package_version函数。"""
        return run_outvar('get_package_version', version_info_path)

    def test_basic_01(self):
        """测试获取包版本。"""
        ret_outvar = self.get_package_version('version.01.info')
        expected = RetOutvar(0, '3.14.V100')
        assert expected == ret_outvar

    def test_basic_02(self):
        """测试获取包版本。"""
        ret_outvar = self.get_package_version('version.03.info')
        expected = RetOutvar(0, '3.14.V200')
        assert expected == ret_outvar

    def test_basic_ex_01(self):
        """测试获取包版本。version.info不存在。"""
        ret_outvar = self.get_package_version('version.not_exists.info')
        expected = RetOutvar(1, '')
        assert expected == ret_outvar


class TestCheckVersionCompat:

    def check_version_compat(self, version, require):
        """调用check_version_compat函数。"""
        return run_check('check_version_compat', version, require)

    def test_basic_01(self):
        """测试版本兼容检查。"""
        ret = self.check_version_compat('3.14', require='3.14')
        assert 0 == ret

    def test_basic_02(self):
        """测试版本兼容检查。"""
        ret = self.check_version_compat('3.14', require='')
        assert 0 == ret

    def test_basic_03(self):
        """测试版本兼容检查。"""
        ret = self.check_version_compat('3.15', require='3.14')
        assert 1 == ret

    def test_basic_04(self):
        """测试版本兼容检查。"""
        ret = self.check_version_compat('3.14.V100', require='3.14')
        assert 0 == ret

    def test_basic_05(self):
        """测试版本兼容检查。"""
        ret = self.check_version_compat('3.14', require='3.14.V100')
        assert 1 == ret

    def test_basic_06(self):
        """测试版本兼容检查。"""
        ret = self.check_version_compat('3.14', require='3.14,3.15')
        assert 0 == ret

    def test_basic_07(self):
        """测试版本兼容检查。"""
        ret = self.check_version_compat('3.15', require='3.14,3.15')
        assert 0 == ret