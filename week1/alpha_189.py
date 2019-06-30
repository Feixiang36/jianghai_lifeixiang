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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.OPEN, t.ADJFCT, t.VWAP]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjVwap = needData[t.VWAP] * needData[t.ADJFCT]
        #adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        #distrib=(adjClose>=self.calculator.Mean(adjClose,6))*(adjClose-self.calculator.Mean(adjClose,6))+(adjClose<self.calculator.Mean(adjClose,6))*(self.calculator.Mean(adjClose,6)-adjClose)
        #distrib=(adjClose>=self.calculator.Decaylinear(adjVwap,6))*(adjClose-self.calculator.Decaylinear(adjVwap,6))+(adjClose<self.calculator.Decaylinear(adjVwap,6))*(self.calculator.Decaylinear(adjVwap,6)-adjClose)
        distrib=adjClose-self.calculator.Sma(adjVwap,5,1)
        factor = self.calculator.Mean(distrib,3)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()