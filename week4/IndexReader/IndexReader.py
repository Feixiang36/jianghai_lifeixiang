# coding=utf8
__author__ = 'Li Feixiang'

import numpy as np
import pandas as pd


'''
此函数用以获取 给定日期的指数成分股
传入参数为：indexconstituent.pickle表的路径，待查询指数，待查询时间
返回: 待查询时间的 指数成分股的 股票代码list
'''
def index_constituent_list(path,index,date):   #index=30,300,500    path  date
    #读入indexconstituent.pickle文件
    index_constituent = pd.read_pickle(path)
    #日期处理：只保留天，去掉分钟
    date=str(date)[:10]
    #从indexconstituent.pickle文件中查询股票代码
    constituent_stock = index_constituent[index][date]['code'].tolist()

    #股票代码处理：去掉后面的字母，只保留前六位数字
    constituent_stock_update = []
    for code in constituent_stock:
        constituent_stock_update.append(code[:6])
    return constituent_stock_update


'''
说明：此程序需要和 indexconstituent.pickle 表配合使用
      但 indexconstituent.pickle 大小超出git限制，需从百度云下载 
'''


if __name__=='__main__':

    '''
    用以查询给定日期的某指数成分股，传入path，index，date三个参数，返回一个list
    path：indexconstituent.pickle表的路径   示例：'D:/index/indexconstituent.pickle.xlsx'
    index为待查询的指数：可接收参数（int型）：50 300 500， 分别代表上证50，沪深300，中证500
    date：查询日期，  示例：'20180710 093525' 或 '20180710'
    
    '''
    path = 'D:/index/indexconstituent/' + 'indexconstituent.pickle'   # indexconstituent.pickle表 的路径
    index=500  #待查询指数
    date= '20180710 093525'
    date = pd.to_datetime(date)
    constituent_stock = index_constituent_list(path=path,index=index,date=date)
    print(constituent_stock)