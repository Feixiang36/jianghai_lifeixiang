#DECAYLINEAR((RANK(MAX((VWAP-CLOSE),3))+RANK(MIN((VWAP-CLOSE),3)))*(LOG(RANK(DELTA(VOLUME, 3)))^1/2),3)

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
        self.needFields = [t.OPEN,t.VOLUME, t.HIGH,t.LOW,t.CLOSE,t.VWAP,t.ADJFCT,t.TURN,t.TRADES_COUNT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjClose = needData[t.CLOSE]* needData[t.ADJFCT]
        adjVwap=needData[t.VWAP]*needData[t.ADJFCT]
        adjVolume=needData[t.VOLUME]*needData[t.ADJFCT]

        distrib0=adjVwap-adjClose
        distrib1=self.calculator.Rank(self.calculator.Max(distrib0,3))
        distrib2=self.calculator.Rank(self.calculator.Min(distrib0,3))
        distrib3=self.calculator.Rank(self.calculator.Diff(adjVolume,3))
        factor = self.calculator.Decaylinear((distrib1+distrib2)*(np.sqrt(np.log(distrib3))),3) #3

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()

fct = Factor()
fct.run_factor()