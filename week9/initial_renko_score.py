#coding=utf8
__author__ = 'LiFeixiang'


import numpy as np
import pandas as pd
import os
import datetime
import scipy.signal as signal
import math

#输入一个ranko的csv 返回整理后的数据
def data_preprocessing(renko_csv):
    renko_data = pd.read_csv(brick_data + renko_csv,engine='python')
    #提取需要的数据 time 和close
    renko_useful = renko_data[['Close','Date Time']]
    #转换数据格式  便于计算时间
    #renko_data['Date Time'] = renko_data['Date Time'].apply(lambda x:datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    #重新设置索引
    renko_useful.index = renko_useful['Date Time']
    #去掉datetime列
    renko_useful.drop('Date Time',axis = 1,inplace = True)
    print(renko_useful)
    return renko_useful


#此函数用于产生一个观测窗口 输入当前的打分时间 输出一个frame刻画当前观测时间窗口下的ranko形态
def get_renko_shape(present_score_time):
    score_time = present_score_time
    #观测窗口设置为3.5小时 此参数可更改
    last_time =datetime.datetime.strptime(str(score_time),'%Y-%m-%d %H:%M:%S')-datetime.timedelta(days=0,hours=3,minutes=30)
    #从该截面向前取数据
    front_data = renko_frame.loc[pd.to_datetime(renko_frame.index) < datetime.datetime.strptime(str(score_time), '%Y-%m-%d %H:%M:%S')]
    print(front_data)
    #取出last_time 和 当前截面之间的数据
    present_renko_data = front_data.loc[front_data.index > str(last_time)]
    print(present_renko_data)
    # 描述一个时间区间内的ranko形态 ：上升一个ranko记作1 下降一个ranko记作 -1
    compare_position = (present_renko_data.diff()['Close'].values<0).tolist()  #下降  ture赋值为-1   false赋值为1
    renko_rela_position=[]
    for i in compare_position:
        if i==False:
            i=1
        else:
            i=-1
        renko_rela_position.append(i)
    #用收盘价刻画ranko的变化形态
    present_renko_data['Close'] = renko_rela_position
    #累积求和 即为该段区间内ranko的形态
    renko_shape = present_renko_data.cumsum()
    print(renko_shape)
    return renko_shape


# 该函数用于在一个截面下按规则打分  输入刻画renko形状的frame 输出分数
def get_renko_score(renko_shape_frame):
    renko_shape = renko_shape_frame
    # 极其简易打分规则 后续也在此部分细化
    # 和ranko的数目相关
    ranko_num = len(renko_shape)
    if ranko_num < 2:  # 0或1 个ranko没法看趋势
        score = 0
    else:
        # 先求极大值的位置  即为趋势的相对高点的位置
        greater_loc = signal.argrelextrema(renko_shape.values, np.greater)[0]
        if len(greater_loc) > 0:  # 如果不为空
            last_greater_loc = greater_loc[-1]  # 取出最后一个高点
            last_greater_value = int(renko_shape.values[last_greater_loc])
        else:  # 不存在极值 即为单调的ranko图
            last_greater_loc = np.where(renko_shape.values == renko_shape.values.max()[0])
            last_greater_value = int(renko_shape.values[last_greater_loc])

        # 极小值同上求法
        smaller_loc = signal.argrelextrema(-renko_shape.values, np.greater)[0]
        if len(smaller_loc) > 0:
            last_smaller_loc = smaller_loc[-1]
            last_smaller_value = int(renko_shape.values[last_smaller_loc])
        else:
            last_smaller_loc = np.where(renko_shape.values == renko_shape.values.min()[0])
            last_smaller_value = int(renko_shape.values[last_smaller_loc])

        # 由打分规则计算当前ranko形态的分数
        # 高低点计算第一个斜率
        present_value = renko_shape.values[-1]
        present_loc = ranko_num
        # 如果高点在后 即先由上涨趋势 后有下跌趋势
        if last_greater_loc > last_smaller_loc:
            # 则k1 为高点减低点计算
            slope1 = (last_greater_value - last_smaller_value) / (last_greater_loc - last_smaller_loc)
            # k2为末点减高点计算
            slope2 = (present_value - last_greater_value) / (present_loc - last_greater_loc)
        else:
            # 否则 k1为低点减高点计算
            slope1 = (last_smaller_value - last_greater_value) / (last_smaller_loc - last_greater_loc)
            # k2为末点减地点计算
            slope2 = (present_value - last_smaller_value) / (present_loc - last_smaller_loc)
        # 计算末点和高低点均线的距离
        distance = present_value - (last_greater_value + last_smaller_value) / 2
        # 此为打分表达式
        score = (0.5 * ranko_num + 0.5 * distance) * (2 - slope2 / slope1)
        # 映射到-1到1之间
        standard_score = 1/(1+np.exp(-score))
    return standard_score

#该函数用于对截面打分进行循环 生成字典 key为时间 value为分数
def get_score_dict(renko_frame):
    #取出此表的起始和终止日期 用于确定打分时间的范围
    start_time = renko_frame.index[5]  #可以考虑第六个开始 太靠前肯定取不到renko
    end_time = renko_frame.index[-1]
    #生成所有的需要打分的时间
    all_score_time = pd.date_range(start=str(start_time), end=str(end_time), freq='30T')
    #建立空字典用于存储renko分数 键为
    score_dict = {}
    for time in all_score_time:
        #获取当前时间的renko形态
        renko_shape = get_renko_shape(time)
        #获取当前截面的renko打分
        renko_score = get_renko_score(renko_shape)
        #键值对添加到字典中
        score_dict[time] = renko_score
    return  score_dict

'''
说明：改程序用于对renko形态打分
输入：510051的本地数据的路径 在brick_data处修改
输出：打分的字典 key为打分的时间 value为当前时间的分数
'''

if __name__=='__main__':
    # 510051的本地数据的路径
    brick_data = 'D:\\factor_combined_strategy\\砖宽\\'
    #有五张表  可以输入0-4  是不同砖宽的数据
    renko = os.listdir(brick_data)[0]
    #数据预处理 只保留有需要的数据
    renko_frame = data_preprocessing(renko)
    #生成打分字典
    score_dict = get_score_dict(renko_frame)
    print(score_dict)


