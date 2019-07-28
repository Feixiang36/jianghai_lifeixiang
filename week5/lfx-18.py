#DECAYLINEAR((((VOLUME/LOW)/MEAN(VOLUME,6))*((HIGH *RANK(HIGH-LOW))/(MEAN(HIGH,5))))/RANK((CLOSE-DELAY(CLOSE,5))),5)
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
        self.needFields = [t.HIGH, t.LOW,t.OPEN,t.VWAP,t.VOLUME, t.CLOSE, t.ADJFCT, t.TRADES_COUNT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjLow = needData[t.LOW] * needData[t.ADJFCT]
        adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        adjVolume=needData[t.VOLUME] * needData[t.ADJFCT]
        adjClose=needData[t.CLOSE] * needData[t.ADJFCT]

        distrib1 = (1 / adjLow) * adjVolume
        distrib2=self.calculator.Mean(adjVolume,6)  #5
        distrib3=adjHigh-self.calculator.Rank(adjHigh-adjLow)
        distrib4=self.calculator.Mean(adjHigh,5) #5
        distrib5=self.calculator.Rank(adjClose-self.calculator.Delay(adjClose,5)) #5
        factor = self.calculator.Decaylinear(-distrib1/distrib2*distrib3/distrib4/distrib5,5)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()

fct = Factor()
fct.run_factor()