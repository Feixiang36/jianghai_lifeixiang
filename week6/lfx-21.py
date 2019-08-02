#(SMA(((LOW^2-DECAYLINEAR(LOW^2,3))/(DECAYLINEAR(LOW^2,3)))^2),5,1)^(1/5)
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
        self.needFields = [t.LOW,t.ADJFCT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据
        adjLow = (needData[t.LOW]* needData[t.ADJFCT])**2

        distrib1 = self.calculator.Decaylinear(adjLow,3)
        distrib2 = (adjLow-distrib1)/distrib1
        distrib3 = self.calculator.Sma(distrib2 ** 2,5,1)
        factor = (distrib3)**(1/5)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()