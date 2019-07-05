#CORR(SMA(((HIGH+LOW)/2),5，1),SMA(MEAN(VOLUME,14),5，1),10)- (CLOSE-TSMIN(CLOSE,30))
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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.ADJFCT,t.OPEN,t.VOLUME,t.VWAP ,t.TRADES_COUNT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjLow = needData[t.LOW] * needData[t.ADJFCT]
        adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjOpen = needData[t.OPEN] * needData[t.ADJFCT]
        #adjVolume = needData[t.VOLUME] * needData[t.ADJFCT]
        adjVolume = needData[t.TRADES_COUNT] * needData[t.ADJFCT]

        distrib1 = (adjClose - self.calculator.TsToMin(adjClose, 30)) #30
        distrib21=self.calculator.Sma(((adjHigh+adjLow)/2),5,1)
        distrib22=self.calculator.Sma(self.calculator.Decaylinear(adjVolume,14),5,1) #14
        distrib2=self.calculator.Corr(distrib21,distrib22,10)
        factor = distrib2-distrib1

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()