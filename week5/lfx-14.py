#SMA(((CLOSE-LOW)-(HIGH-CLOSE))/(HIGH-LOW)*VOLUME,30,17)
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


        adjLow = needData[t.LOW] * needData[t.ADJFCT]
        adjHigh = needData[t.OPEN] *needData[t.ADJFCT]
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjVolume= needData[t.VOLUME] * needData[t.ADJFCT]

        distrib = ((adjClose-adjLow)-(adjHigh-adjClose))/(adjHigh-adjLow)
        factor = self.calculator.Sma(distrib * adjVolume,30,17)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()