#-SMA(STD(VOLUME^3-DELAY(VOLUME^3,1),4),7,1)/SMA(ABS(VOLUME^3-DELAY(VOLUME^3,1)),7,1)
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
        self.needFields = [t.ADJFCT,t.VOLUME]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjVolume = (needData[t.VOLUME] * needData[t.ADJFCT])**3

        distrib1=adjVolume-self.calculator.Delay(adjVolume,1)
        distrib2=self.calculator.Std(distrib1,4)
        distrib3=(distrib1>=0)*distrib1 + (distrib1<0)*(-distrib1)
        distrib4=self.calculator.Sma(distrib2,7,1)
        distrib5=self.calculator.Sma(distrib3,7,1)
        factor = (- distrib4 / distrib5)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()

fct = Factor()
fct.run_factor()