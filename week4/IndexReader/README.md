# IndexReader
#### _@author:李飞翔_
### Read Data Module
- ``` index_constituent_list(path,index,date)```
- 输入
    - path:存储指数成分股的pickle文件的路径
    - index:格式为int,50代表查询上证50；300代表查询沪深300；500代表查询中证500
    - date:查询的日期，格式可以为datetime 或 '%Y-%M-%d'
- 输出
    - 相应的成分股股票代码列表

