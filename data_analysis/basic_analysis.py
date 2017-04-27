# -*- coding:utf-8 -*-
# =======================================================
# 
# @FileName  : basic_analysis.py
# @Author    : Wang Hongqing
# @Date      : 2017-04-27 08:58
# 
# =======================================================

import os
import sys
import argparse
import logging
import matplotlib
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')

# parser = argparse.ArgumentParser()
# parser.add_argument()
# args = parser.parse_args()

# output = args.output
logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%a, %d %b %Y %H:%M:%S'
)

"""
主要分析下列内容
星期几对是否购买产品是否造成影响
"""

# 文件夹定义
current_dir = os.getcwd()
home_dir = os.path.dirname(current_dir)
download_data_dir = os.path.join(home_dir, "data", "original_data")
transform_data_dir = os.path.join(home_dir, "data", "transform_data")

# 文件定义
action_02 = os.path.join(download_data_dir, "JData_Action_201602.csv")
action_03 = os.path.join(download_data_dir, "JData_Action_201603.csv")
action_04 = os.path.join(download_data_dir, "JData_Action_201604.csv")
comment_file = os.path.join(download_data_dir, "JData_Comment.csv")
product_file = os.path.join(download_data_dir, "JData_Product.csv")
user_file = os.path.join(download_data_dir, "JData_User.csv")
transform_user_file = os.path.join(transform_data_dir, "user.csv")


def get_info_from_action_data(file_name=None, chunk_size=100000):
    reader = pd.read_csv(file_name, header=0, iterator=True)
    chunks = []
    while True:
        try:
            chunk = reader.get_chunk(chunk_size)[["user_id", "sku_id", "type", "time"]]
            chunks.append(chunk)
        except StopIteration:
            logging.info("Iteration mannually stopped!")
            break
    df_concat = pd.concat(chunks, ignore_index=True)
    df_concat = df_concat[df_concat["type"] == 4]
    df_concat["time"] = pd.to_datetime(df_concat['time'])
    # 周一为 1 周日为7
    df_concat["time"] = df_concat.apply(lambda x: x.weekday() + 1)
    return df_concat[["user_id", "sku_id", "time"]]


df_list = []
for index in range(2, 5):
    df_concat = get_info_from_action_data(file_name="action_0%d" % index)
    df_list.append(df_concat)

df_concat_all = pd.concat(df_list, ignore_index=True)

df_user = df_concat.groupby("time")["user_id"].nunique()
df_user = df_user.to_frame().reset_index()
df_user.columns = ["weekday", "user_num"]

df_item = df_concat.groupby("time")["sku_id"].nunique()
df_item = df_item.to_frame().reset_index()
df_item.columns = ["weekday", "item_num"]

# 周一到周日每天购买记录个数
df_ui = df_concat.groupby('time', as_index=False).size()
df_ui = df_ui.to_frame().reset_index()
df_ui.columns = ['weekday', 'user_item_num']

# 条形宽度
bar_width = 0.2
# 透明度
opacity = 0.4

plt.bar(df_user['weekday'], df_user['user_num'], bar_width,
        alpha=opacity, color='c', label='user')
plt.bar(df_item['weekday']+bar_width, df_item['item_num'],
        bar_width, alpha=opacity, color='g', label='item')
plt.bar(df_ui['weekday']+bar_width*2, df_ui['user_item_num'],
        bar_width, alpha=opacity, color='m', label='user_item')

plt.xlabel('weekday')
plt.ylabel('number')
plt.title('A Week Purchase Table')
plt.xticks(df_user['weekday'] + bar_width * 3 / 2., (1,2,3,4,5,6,7))
plt.tight_layout()
plt.legend(prop={'size':9})
