# coding=utf8
__author__ = 'lifx'
# DECAYLINEAR(STD(ABS((LOW/DELAY(CLOSE,1)-1))/TRADES_COUNT,5)/MEAN(ABS((LOW/DELAY(CLOSE,1)-1))/TRADES_AOUNT,5),3)

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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.ADJFCT, t.VOLUME,t.VWAP,t.TRADES_COUNT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjLow = needData[t.LOW] * needData[t.ADJFCT]
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjTrades_count = needData[t.TRADES_COUNT] * needData[t.ADJFCT]
        preClose = self.calculator.Delay(adjClose,1)

        distrib1=(adjLow>=preClose)*(adjLow/preClose-1)+(adjLow<preClose)*(1-adjLow/preClose)
        distrib2=distrib1/adjTrades_count
        factor = self.calculator.Decaylinear(self.calculator.Std(distrib2,5)/self.calculator.Mean(distrib2,5),3)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()