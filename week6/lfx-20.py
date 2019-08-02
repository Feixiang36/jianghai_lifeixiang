#DECAYLINEAR(-(RANK(CLOSE**2-MIN(CLOSE**2,5))^(CORR(HIGH**2,MEAN(VOLUME,200),6))),3)
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
        self.needFields = [ t.CLOSE,t.HIGH,t.ADJFCT, t.TRDSTAT,t.VOLUME]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjClose =(needData[t.CLOSE] * needData[t.ADJFCT])**2
        adjVolume = (needData[t.VOLUME] * needData[t.ADJFCT])
        adjHigh= (needData[t.HIGH] * needData[t.ADJFCT])**2

        distrib1=adjClose-self.calculator.Min(adjClose,5)
        distrib2=self.calculator.Rank(distrib1)
        distrib3=self.calculator.Mean(adjVolume,200)   #120
        distrib4=self.calculator.Corr(adjHigh,distrib3,6)  #6
        factor = self.calculator.Decaylinear(-(distrib2**distrib4),3)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()