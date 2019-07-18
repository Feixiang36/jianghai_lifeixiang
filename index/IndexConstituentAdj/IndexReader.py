import numpy as np
import pandas as pd


'''
此函数用以获取 给定日期的指数成分股
传入参数为：成分股调整表的路径，要查询的时间
返回: list 为待查询日期的成分股
'''
def given_date_constituent(path,date):    #path为IndexConstituentAdj表的路径 示例：'D:/index/IndexConstituentAdj.xlsx'
                                         #date为待查询日期 示例 '2018-07-10'
    #读入ndexConstituentAdj表
    adjindex=pd.read_excel(path)
    # 筛选早于给定日期的状态
    adj_index=adjindex[adjindex['日期']< date]
    # 将已剔除股票的纳入状态删除
    adj_index=adj_index.drop_duplicates(['品种代码'],keep='last')
    # 去除剔除状态 返回given date 的成分股
    return adj_index[adj_index['操作']=='纳入']

'''
说明：此函数根据给定的 IndexConstituentAdj.xlsx 样表编写
      但由于给定的表本身数据不完整 故返回的结果可能并非真实结果
      如果有完整数据，结构与 IndexConstituentAdj.xlsx 相同，则可使用此程序返回正确的指数成分股
'''

if __name__=='__main__':
    path = 'D:/index/IndexConstituentAdj/'+'IndexConstituentAdj.xlsx'  #path为IndexConstituentAdj表的路径 示例：'D:/index/IndexConstituentAdj.xlsx'
    date = '2018-01-03'                         #date为待查询日期  示例 '2018-01-03'
    constituent_stock = given_date_constituent(path=path,date=date)['品种代码'].tolist()
    print(constituent_stock)