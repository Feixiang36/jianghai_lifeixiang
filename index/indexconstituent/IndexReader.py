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
    #返回
    return index_constituent[index][date]['code'].tolist()




if __name__=='__main__':

    '''
    用以查询给定日期的某指数成分股，传入path，index，date三个参数，返回一个list
    path：indexconstituent.pickle表的路径   示例：'D:/index/indexconstituent.pickle.xlsx'
    index为待查询的指数：可接收参数（int型）：50 300 500， 分别代表上证50，沪深300，中证500
    date：查询日期，  示例：'2013-06-01'
    
    '''
    path = 'D:/index/indexconstituent/' + 'indexconstituent.pickle'   # indexconstituent.pickle表 的路径
    index=500                                   #待查询指数
    date = '2018-07-10'                        #date为待查询日期
    constituent_stock = index_constituent_list(path=path,index=index,date=date)
    print(constituent_stock)