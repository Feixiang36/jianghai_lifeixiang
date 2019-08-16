#RANK(DELTA(CORR(SQRT(LOW),VOLUME^2,5),5)*(STD(SQRT(CLOSE),20))))
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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.OPEN,t.VWAP,t.ADJFCT,t.VOLUME,t.TURN,t.TRADES_COUNT,t.VOLUME_DIFF_LARGE_TRADER,t.VOLUME_DIFF_SMALL_TRADER]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjVolume = (needData[t.TURN]* needData[t.ADJFCT])**2
        adjLow = (needData[t.LOW] * needData[t.ADJFCT])**(1/2)
        adjClose = (needData[t.CLOSE]* needData[t.ADJFCT])**(1/2)

        distrib1 = self.calculator.Corr(adjLow,adjVolume,5)
        distrib2 = self.calculator.Decaylinear(distrib1,5)
        distrib3 = self.calculator.Std(adjClose,20)   #20
        factor =self.calculator.Rank(-(distrib2*distrib3))

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()