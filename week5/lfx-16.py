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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE,t.OPEN,t.VOLUME,t.ADJFCT,t.TRADES_COUNT,t.VWAP]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据
        adjClose= needData[t.CLOSE] * needData[t.ADJFCT]
        adjVwap = np.log(needData[t.VWAP] * needData[t.ADJFCT])

        distrib1=self.calculator.Std(adjVwap,3)
        distrib2=self.calculator.Std(adjVwap,6)
        distrib3=self.calculator.Std(adjVwap,12)
        distrib4=self.calculator.Std(adjVwap,24)
        distrib=distrib1+distrib2+distrib3+distrib4
        factor = self.calculator.Sma(distrib,6,1)*(adjClose>self.calculator.Mean(adjClose,3))

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()