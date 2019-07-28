#
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

        adjClose = (needData[t.CLOSE] * needData[t.ADJFCT])
        adjTrades_count=(needData[t.TRADES_COUNT] * needData[t.ADJFCT])
        adjVwap=(needData[t.VWAP] * needData[t.ADJFCT])

        distrib1=self.calculator.Mean(adjTrades_count,80)   #80
        distrib2=self.calculator.Corr(adjVwap,distrib1,5) #17
        distrib3=self.calculator.Decaylinear(distrib2,30)  #20
        distrib4=self.calculator.Rank(distrib3)
        distrib5=0.5 * adjClose+adjVwap * 0.5        #0.5 0.5
        distrib6=self.calculator.Diff(distrib5,20)  #3
        distrib7=self.calculator.Decaylinear(distrib6,16) #16
        distrib8=self.calculator.Rank(distrib7)
        factor = distrib4/distrib8

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()