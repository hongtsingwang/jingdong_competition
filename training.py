# -*- coding:utf-8 -*-
# =======================================================
#
# @FileName  : training.py
# @Author    : Wang Hongqing
# @Date      : 2017-05-03 16:17
#
# =======================================================

import os
import sys
import argparse
import logging
import pandas as pd
from itertools import product

# import xgboost

reload(sys)
sys.setdefaultencoding('utf-8')

# 输入参数定义
parser = argparse.ArgumentParser()
parser.add_argument("--train_start_date", default="2016-03-10", help="训练集开始选定的日期")
parser.add_argument("--train_end_date", default="2016-04-11", help="训练集截止的日期")
parser.add_argument("--test_start_date", default="2016-04-12", help="测试集开始的日期")
parser.add_argument("--test_end_date", default="2016-04-15", help="测试集截止的日期")

# 文件夹定义
home_dir = os.getcwd()
download_data_dir = os.path.join(home_dir, "data", "original_data")
transform_data_dir = os.path.join(home_dir, "data", "transform_data")
submission_data_dir = os.path.join(home_dir, "submission")

# 文件定义
action_02 = os.path.join(download_data_dir, "JData_Action_201602.csv")
action_03 = os.path.join(download_data_dir, "JData_Action_201603.csv")
action_04 = os.path.join(download_data_dir, "JData_Action_201604.csv")
comment_file = os.path.join(download_data_dir, "JData_Comment.csv")
product_file = os.path.join(download_data_dir, "JData_Product.csv")
user_file = os.path.join(download_data_dir, "JData_User.csv")
transform_user_file = os.path.join(transform_data_dir, "user.csv")
result_file = os.path.join(submission_data_dir, "submission.csv")

args = parser.parse_args()

# output = args.output
logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%a, %d %b %Y %H:%M:%S'
)


def get_ratio_feature(user_df):
    time_list = ["02", "03", "04", "2016-01-31_2016-04-11", "2016-03-13_2016-04-11", "2016-03-22_2016-04-11",
                 "2016-03-28_2016-04-11", "2016-04-02_2016-04-11", "2016-04-05_2016-04-11", "2016-04-07_2016-04-11",
                 "2016-04-09_2016-04-11", "2016-04-10_2016-04-11", "2016-04-11_2016-04-11"]
    action_list = ["view", "add_cart", "cancel_add_cart", "follow", "click"]
    feature_list = []
    for times, action in product(time_list, action_list):
        purchase_key = times + "_" + "purchase"
        other_key = times + "_" + action
        result_key = "_".join([times, "purchase", action, "ratio"])
        user_df[result_key] = user_df[other_key] / user_df[purchase_key]
        feature_list.append(result_key)
    return user_df, feature_list


def get_basic_user_feature():
    user = pd.read_csv(user_file, encoding='gbk', header=0)
    age_df = pd.get_dummies(user["age_convert_id"], prefix="age")
    sex_df = pd.get_dummies(user["sex"], prefix="sex")
    user_level_df = pd.get_dummies(user["user_lv_cd"], prefix="user_level")
    user_ratio_feature, ratio_feature = get_ratio_feature(user)
    actions = user_ratio_feature[ratio_feature]
    user_df = pd.concat([user["user_id"], age_df, sex_df, user_level_df,actions], axis=1)
    return user_df


def train_set_making(train_start_date, train_end_date, test_start_date, test_end_date):
    """
    
    :param train_start_date: 
    :param train_end_date: 
    :param test_start_date: 
    :param test_end_date: 
    :return: 
    """
    user_basic_feature = get_basic_user_feature()


def make_submission():
    train_start_date = args.train_start_date
    train_end_date = args.train_end_date
    test_start_date = args.test_start_date
    test_end_date = args.test_end_date
    user_index, training_data, label = train_set_making(train_start_date, train_end_date, test_start_date,
                                                        test_end_date)

    # 结果输出成csv文件,
    # TODO index，index_label 分别代表什么含义
    pred.to_csv(result_file, index=False, index_label=False)


if __name__ == "__main__":
    make_submission()
