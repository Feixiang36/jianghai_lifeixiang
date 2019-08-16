#coding=utf8
__author__ = 'LiFeixiang'

import numpy as np
import pandas as pd
from scipy import linalg


#用于计算截面的 因子tbdf10 的函数
def cal_tbdf10(x):
    #对股票的收益序列 按降序排序并去空
    x=x.sort_values(ascending=False).dropna()
    #求出该收益序列10%的长度并取整
    length = round(len(x) * 0.1)
    #对前10%求和
    top10percent = x.iloc[0:length].sum()
    #对后10%求和
    bottom10percent = x.iloc[-length:].sum()
    #返回股票收益的tbdf10
    return top10percent - bottom10percent


#计算因子收益的相关矩阵
def cal_alpha_profit_matrix(factor_list):
    alpha_profit_matrix=pd.DataFrame()
    for factor in factor_list:
        #读入因子收益的dataframe： index为时间序列 column为标的代码 value为标的收益
        factor_profit_frame = pd.read_hdf(path + factor +'.h5')
        #计算每一个时间股票的tbdf10，即为该因子收益， 返回一个Series，为因子的收益序列
        alpha_series = factor_profit_frame.apply(cal_tbdf10,axis=1)
        #将factor list 中 每一个因子的收益序列合并为一个dataframe
        alpha_profit_matrix = alpha_profit_matrix.append(alpha_series.T ,ignore_index=True)
    #构造新的dataframe index为时间 column为因子 value为因子收益值
    alpha_profit_matrix = alpha_profit_matrix.T
    alpha_profit_matrix.columns = factor_list
    return alpha_profit_matrix


#矩阵求逆的正则化方法 用于对协方差矩阵求逆
def regularization_cal_inv(matrix):
    #判断矩阵是否奇异
    if np.linalg.det(matrix):
        #如果非奇异，直接求逆
        inv_matrix = linalg.inv(matrix)
    else:
        #奇异矩阵使用paper给出的正则化方法
        p = np.arange(0,1,0.02)
        for q in p:
            nonsingular_matrix= q * np.diag(np.diag(matrix))+ (1-q) * matrix
            if not np.linalg.det(nonsingular_matrix):  #非0为真 即行列式不为0了，则矩阵可逆
                inv_matrix = linalg.inv(matrix)
                break
            else:
                continue
    #返回相关矩阵的逆矩阵 用于计算因子权重
    return inv_matrix


def get_inv_dict(factor_list):
    #设定协方差矩阵估计的窗宽，该参数根据估计需要可以调整，此处为10天
    window_width=10
    #获取因子列表的长度 即协方差阵的维度
    covmat_dim=len(factor_list)
    #获取因子收益的dataframe
    alpha_profit_matrix = cal_alpha_profit_matrix(factor_list)
    #rolling 求出协方差的dataframe
    cov_frame = pd.DataFrame(alpha_profit_matrix).rolling(window=window_width).cov().dropna()
    #取出双索引中的时间索引作为字典的键
    keys = cov_frame.index.levels[0][(window_width-1):]
    #创建空列表存储每日权重
    daily_weight=[]
    for i in range(0,int(len(cov_frame)/covmat_dim)):
        #获取因子收益的相关矩阵
        cov_matrix = cov_frame.iloc[covmat_dim*i:covmat_dim*(i+1)].values
        #利用正则化方法求逆
        inv_matrix = regularization_cal_inv(cov_matrix)
        daily_weight.append(inv_matrix)
    #返回字典: 键为时间 值为逆矩阵（array类型）
    return dict(zip(keys,daily_weight))


def opt_factor_weight(factor_list):
    #获取逆矩阵字典
    cov_inv_dict = get_inv_dict(factor_list)
    #获取alpha收益矩阵
    alpha_profit_matrix = cal_alpha_profit_matrix(factor_list)
    #建立空字典，用以存储 日期：权重向量
    weight_dict={}
    for date in cov_inv_dict:
        #paper方法计算权重向量
        initial_weight = cov_inv_dict[date].dot(alpha_profit_matrix.T[date].values)
        #paper的约束归一化
        standard_weight = initial_weight/ np.sum(np.abs(initial_weight))
        #循环添加到字典中
        weight_dict[date] = standard_weight
    return weight_dict


'''
    代码说明：
    此代码根据paper提供的方法，给定若干个alpha，通过优化alpha的权重，使得投资组合的sharp ratio 最大，
    输入：alpha stream 
    输出：dict，key为日期，values为该日期下给定alpha stream 的投资权重
    注：需要先下载因子收益的文件，已传到百度云，下载本地后路径存为path
'''



if __name__=='__main__':
    # 因子收益文件的路径，需要从百度云下载
    path = 'D:\\factor_combined_strategy\\factor_profit\\'
    #alpha stream 长度不限，需要是factor_profit中的因子
    factor_list = ['factor1', 'factor28', 'factor3','factor8']
    print(opt_factor_weight(factor_list))
