# -*- coding:utf-8 -*-
# @FileName  : first_commit.py
# @Author    : Wang Hongqing
# @Date      : 2017-04-22 19:23
# --------------------------------------------------------

import os
import sys
import argparse
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

"""
第一次提交结果练手
假定用户购买过这个商品，那么用户一定会再次购买，简单出一个结果。提交一下
"""

parser = argparse.ArgumentParser()
parser.add_argument()
parser.parse_args()

logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%a, %d %b %Y %H:%M:%S'
)

