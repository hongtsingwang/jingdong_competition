#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================================
# 
# Copyright (c) 2017 Letv.com, Inc. All Rights Reserved
# @Time     : 2017/4/10 9:21
# @Author   : Wang Hongqing
# @File     : first_explore_data.py
#
# ===============================================================================
import os
import sys
import logging
import argparse
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

current_time = datetime.datetime.today().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%a, %d %b %Y %H:%M:%S'
)
logger = logging.getLogger(__name__)
logger.info("running %s", " ".join(sys.argv))

import pandas as pd
import numpy as np


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        pass
    assert os.path.exists(path)


# 文件夹定义
home_dir = os.getcwd()
download_data_dir = os.path.join(home_dir, "data", "original_data")
transform_data_dir = os.path.join(home_dir, "data", "transform_data")

# 文件定义
action_02 = os.path.join(download_data_dir, "JData_Action_201602.csv")
action_03 = os.path.join(download_data_dir, "JData_Action_201603.csv")
action_04 = os.path.exists(download_data_dir, "JData_Action_201604.csv")
comment_file = os.path.exists(download_data_dir, "JData_Comment.csv")
product_file = os.path.join(download_data_dir, "JData_Product.csv")
user_file = os.path.exists(download_data_dir, "JData_User.csv")
transform_user_file = os.path.exists(transform_data_dir, "user.csv")

# mkdir(data_dir)
assert os.path.exists(download_data_dir)
mkdir(transform_data_dir)


def age_convert(age):
    """
    将中文age转换成数字序列可表示的方式。 方便feature处理
    :param age: 输入年龄形式。example："15岁以下"
    :return: 数字化的年龄形式结果
    """
    age_map = {
        u'-1': -1,
        u"15岁以下": 0,
        u"16-25岁": 1,
        u"26-35岁": 2,
        u"36-45岁": 3,
        u"46-55岁": 4,
        u"56岁以上": 5,
    }
    return age_map.get(age, -1)


def user_file_transform():
    """
    :return:无返回结果，直接将新的user_文件保存
    """
    df = pd.read_csv(user_file, header=0, encoding="gbk")
    df['age'] = df['age'].map(age_convert)
    df["user_reg_tm"] = pd.to_datetime(df["user_reg_tm"])
    start_date = df["user_reg_tm"].min()  # 求最早的注册日期
    df["user_register_diff"] = (df['user_reg_tm'] - start_date).dt.days
    df.to_csv(transform_user_file, index=False)


if __name__ == "__main__":
    user_file_transform()
