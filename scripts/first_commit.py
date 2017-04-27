# -*- coding:utf-8 -*-
# @FileName  : first_commit.py
# @Author    : Wang Hongqing
# @Date      : 2017-04-22 19:23
#
# --------------------------------------------------------

import os
import sys
import argparse
import logging
import datetime
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

"""
第一次提交结果练手
假定用户购买过这个商品，那么用户一定会再次购买，简单出一个结果。提交一下
"""
#
# parser = argparse.ArgumentParser()
# parser.add_argument()
# parser.parse_args()

logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%a, %d %b %Y %H:%M:%S'
)

HOME_DIR = os.getcwd()
DATA_DIR = os.path.join(HOME_DIR, "data")
RESULT_DIR = os.path.join(HOME_DIR, "result")


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


mkdir(DATA_DIR)
mkdir(RESULT_DIR)

user_list_file = os.path.join(DATA_DIR, "JData_User.csv")
product_list_file = os.path.join(DATA_DIR, "JData_Product.csv")
action_02 = os.path.join(DATA_DIR, "JData_Action_201602.csv")
action_03 = os.path.join(DATA_DIR, "JData_Action_201603.csv")
action_04 = os.path.join(DATA_DIR, "JData_Action_201604.csv")
result_file = os.path.join(RESULT_DIR, datetime.datetime.now().strftime("%Y%m%d") + ".csv")


def get_purchase_user_item_pair(action_file, chunk_size=100000):
    reader = pd.read_csv(action_file, header=0, iterator=True)
    chunks = []
    while True:
        try:
            logging.info("%d" % len(chunks))
            chunk = reader.get_chunk(chunk_size)[["user_id", "sku_id", "type"]]
            chunks.append(chunk)
        except StopIteration:
            logging.info("Iteration stopped by user")
            break
    df = pd.concat(chunks, ignore_index=True)
    df_purchase = df[df["type"] == 4]
    df_purchase["user_id"] = df_purchase["user_id"].astype('int')
    result = pd.DataFrame({"user_id": df_purchase["user_id"].as_matrix(), "sku_id": df_purchase["sku_id"].as_matrix()})
    result.to_csv("result.csv", index=False)


get_purchase_user_item_pair(action_04, chunk_size=1000000)
