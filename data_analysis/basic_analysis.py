# -*- coding:utf-8 -*-
# =======================================================
# 
# @FileName  : basic_analysis.py
# @Author    : Wang Hongqing
# @Date      : 2017-04-27 08:58
# 
# =======================================================

import logging
import os
import sys

import pandas as pd
from matplotlib.pyplot import bar, ylabel, tight_layout, figure, legend, xticks, xlabel, title

reload(sys)
sys.setdefaultencoding('utf-8')

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


def get_chunks(reader, chunk_size, field_list=[]):
    chunks = []
    while True:
        try:
            chunk = reader.get_chunk(chunk_size)[field_list]
            chunks.append(chunk)
        except StopIteration:
            logging.info("Iteration manually stopped!")
            break
    return chunks


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

    return df_concat[["user_id", "sku_id", "time"]]


df_list = []
for index in range(2, 5):
    df_concat = get_info_from_action_data(file_name="action_0%d" % index)
    df_list.append(df_concat)

df_concat_all = pd.concat(df_list, ignore_index=True)
# 周一为 1 周日为7
df_concat_all["time"] = df_concat_all.apply(lambda x: x.weekday() + 1)

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

bar(df_user['weekday'], df_user['user_num'], bar_width,
    alpha=opacity, color='c', label='user')
bar(df_item['weekday'] + bar_width, df_item['item_num'],
    bar_width, alpha=opacity, color='g', label='item')
bar(df_ui['weekday'] + bar_width * 2, df_ui['user_item_num'],
    bar_width, alpha=opacity, color='m', label='user_item')

xlabel('weekday')
ylabel('number')
title('A Week Purchase Table')
xticks(df_user['weekday'] + bar_width * 3 / 2., (1, 2, 3, 4, 5, 6, 7))
tight_layout()
legend(prop={'size': 9})


def purchase_statistics_each_day():
    df = get_info_from_action_data(fname=action_02)
    df['time'] = pd.to_datetime(df['time']).apply(lambda x: x.day)

    df_user = df.groupby("time")["user_id"].nunique()
    df_user = df_user.to_frame().reset_index()
    df_item = df.groupby('time')['sku_id'].nunique()
    df_item = df_item.to_frame().reset_index()
    df_item.columns = ['day', 'item_num']
    df_ui = df.groupby('time', as_index=False).size()
    df_ui = df_ui.to_frame().reset_index()
    df_ui.columns = ['day', 'user_item_num']

    # 条形宽度
    bar_width = 0.2
    # 透明度
    opacity = 0.4
    # 天数
    day_range = range(1, len(df_user['day']) + 1, 1)
    # 设置图片大小
    figure(figsize=(14, 10))

    bar(df_user['day'], df_user['user_num'], bar_width,
        alpha=opacity, color='c', label='user')
    bar(df_item['day'] + bar_width, df_item['item_num'],
        bar_width, alpha=opacity, color='g', label='item')
    bar(df_ui['day'] + bar_width * 2, df_ui['user_item_num'],
        bar_width, alpha=opacity, color='m', label='user_item')

    xlabel('day')
    ylabel('number')
    title('February Purchase Table')
    xticks(df_user['day'] + bar_width * 3 / 2., day_range)
    tight_layout()
    legend(prop={'size': 9})


def spec_ui_action_data(fname, user_id, item_id, chunk_size=100000):
    """
    查看特定用户对特定商品的活动轨迹
    :param fname: 
    :param user_id: 
    :param item_id: 
    :param chunk_size: 
    :return: 
    """
    reader = pd.read_csv(fname, header=0, iterator=True)
    chunks = get_chunks(reader, chunk_size)
    df_concat = pd.concat(chunks, ignore_index=True)
    df_concat = df_concat[(df_concat['user_id'] == user_id) & (df_concat['sku_id'] == item_id)]
    return df_concat


def explore_user_item_via_time():
    """
    指定user_id, item_id 获取其活动轨迹
    :return: 
    """
    user_id = 62969
    item_id = 62655
    df_ac = [spec_ui_action_data(action_02, user_id, item_id), spec_ui_action_data(action_03, user_id, item_id),
             spec_ui_action_data(action_04, user_id, item_id)]

    df_ac = pd.concat(df_ac, ignore_index=False)
    print(df_ac.sort_values(by='time'))


explore_user_item_via_time()
