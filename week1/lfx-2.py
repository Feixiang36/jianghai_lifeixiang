#SMA((-1*RANK(CLOSE-SMA(HIGH,3,2)))*RANK(CLOSE-SMA(CLOSE,3,2))*RANK(CLOSE-SMA(LOW,3,2)),2,1)
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
        self.neutral = True
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.OPEN,t.VWAP]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjLow = needData[t.LOW]
        adjHigh = needData[t.HIGH]
        adjClose = needData[t.CLOSE]
        adjOpen = needData[t.OPEN]
        adjVwap = needData[t.VWAP]
        distrib1 = -self.calculator.Rank(adjClose - self.calculator.Sma(adjHigh, 3, 2))
        distrib2 = self.calculator.Rank(adjClose - self.calculator.Sma(adjClose, 3, 2))
        distrib3 = self.calculator.Rank(adjClose - self.calculator.Sma(adjLow, 3, 2))
        factor = self.calculator.Sma(distrib1 * distrib2 * distrib3, 2, 1)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()