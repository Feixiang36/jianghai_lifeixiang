#SMA(VOLUME,13,2)-SMA(VOLUME,27,2)-SMA(SMA(VOLUME,13,2)-SMA(VOLUME,27,2),10,2)
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
        self.needFields = [t.VOLUME,t.ADJFCT,t.CLOSE]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据
        adjVolume= (needData[t.VOLUME]**2)
        adjClose=needData[t.CLOSE]


        distrib1=self.calculator.Sma(adjVolume,9,2)
        distrib2=self.calculator.Sma(adjVolume,15,2)   #15 2
        distrib=distrib1/distrib2
        factor = distrib/self.calculator.Sma(distrib,5,2) * (adjClose<self.calculator.Mean(adjClose,5))

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()