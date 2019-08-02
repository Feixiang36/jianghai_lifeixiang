#-SMA(((CLOSE/DELAY(CLOSE,10))>0.8?TRADES_COUNT:(CLOSE/DELAY(CLOSE,10))<0.8?-TRADE_COUNT:0),30,17)
# coding=utf8
__author__ = 'lifx'

import time

import numpy as np
import pandas as pd
from FactorModule.FactorBase import FactorBase
from DataReaderModule.Constants import ALIAS_FIELDS as t

class Factor(FactorBase):

    def __init__(self):
        super(Factor,self).__init__()
        self.neutral = False
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.HIGH, t.LOW, t.CLOSE,t.VWAP,t.OPEN,t.ADJFCT, t.VOLUME,t.TRADES_COUNT,t.TURN]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjClose = (needData[t.CLOSE] * needData[t.ADJFCT])
        adjVolume= (needData[t.TRADES_COUNT])
        distrib1= adjClose/self.calculator.Delay(adjClose,10)  #10
        distrib=(distrib1>0.8)*adjVolume-(distrib1<0.8)*adjVolume #0.8
        factor= -self.calculator.Sma(distrib,30,17)  #30 17

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()