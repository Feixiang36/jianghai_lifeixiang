#coding=utf8
__author__ = 'LiFeixiang'

import numpy as np
import pandas as pd
import os

#该函数用于数据预处理 将分钟数据变为日线数据
def data_preprocessing(future):
    # 读入期货品种的csv
    net_value_frame = pd.read_csv(future_path + future,engine='python')
    #数据预处理：分钟数据只保留日数据
    net_value_frame.index = np.array([time[0:10] for time in net_value_frame['Date Time'].values])
    net_value_frame = net_value_frame[~net_value_frame.index.duplicated(keep='last')]
    #去掉时间那一列后返回
    net_value_frame.drop(['Date Time'], axis=1, inplace=True)
    return net_value_frame

#该函数用于将30张csv拼接成一个csv
def get_combined_frame(future_path):
    #获取文件夹下的所有csv的目录
    futures = os.listdir(future_path)
    #创建空frame 用于存储所有合成的frame
    combined_frame = pd.DataFrame()
    for future in futures:
        #对一个csv处理
        one_net_value_frame = data_preprocessing(future)
        #不同的frame拼接
        combined_frame = pd.concat([combined_frame, one_net_value_frame], axis=1)
    return combined_frame


#该函数用于计算某一截面下的净值总和
def oneday_net_value(date):
    #从date开始往前取30天 不包含今日
    day30_frame = combined_frame[combined_frame.index < date].iloc[-window_width:,:]
    #计算30日的相关矩阵
    day30_corr = day30_frame.corr()
    #获取最小的100个相关系数的行列索引  由于相关矩阵的对称性 相当于找出50个不同的相关性系数
    row_index,col_index = np.unravel_index(np.argpartition(day30_corr.values.ravel(),num*2)[:num*2],day30_corr.values.shape)
    #通过索引 取出相关矩阵中的列名
    select_columns = day30_corr.columns[row_index]
    #用列名在净值矩阵中访问 求出今日的五个列名对应的净值数据的均值
    today_net_value = combined_frame[select_columns].loc[date].mean()
    return today_net_value

#该函数用于对截面循环 输出字典
def future_net_value_dict(net_value_frame):
    #每隔十天需要计算一次 取出这些日期
    need_cal_date = net_value_frame.index.tolist()[::time_interval]
    #空字典用于存储 日期：净值 键值对
    all_net_value = {}
    #初试时数据不足 故从第n个时间开始开始
    for date in need_cal_date[round((window_width/time_interval))+1:]:
        #计算date这一日的 净值
        date_net_value = oneday_net_value(date)
        #添加到字典中 key为date，value为净值
        all_net_value[date] = date_net_value
    return all_net_value

'''
该函数用于将30个品种的期货合并得到1w多组参数之后 利用低相关系数 在截面下计算净值，并输出一个时间序列的净值字典
输入：期货数据的存储路径
输出：期货的净值字典 key为日期（十日间隔），value为净值的均值
说明：1.需要结合期货的数据使用
      2.数据量过大 需要十几分钟的计算时间，请耐心等待。。。
'''

if __name__=='__main__':
    # 30个期货品种解压后的文件路径 需要根据本地路径修改
    future_path = 'D:\\factor_combined_strategy\\future_data\\'

    #可调参数设置
    window_width = 30  #用30天的数据 计算相关系数
    time_interval = 10  #m每隔十天计算一次
    num = 50  #每个截面下选取的净值数目

    combined_frame = get_combined_frame(future_path)
    net_value_dict = future_net_value_dict(combined_frame)
    print(net_value_dict)
    #画净值图
    #net_value_frame = pd.DataFrame.from_dict(net_value_dict, orient='index')
    #net_value_frame.plot()




