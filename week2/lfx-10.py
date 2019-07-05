#-DELTA((((((HIGH + LOW) / 2) * 0.2) + (VWAP * 0.8))),4)
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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.ADJFCT, t.TRDSTAT,t.VWAP,t.OPEN]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        Low = needData[t.LOW]
        High = needData[t.HIGH]
        Close = needData[t.CLOSE]
        Vwap = needData[t.VWAP]
        Open = needData[t.OPEN]


        distrib=(((Close+Open)/2)*0.2 + Vwap*0.8)     #构建量价指标
        factor = -self.calculator.Diff(distrib,4)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()

fct = Factor()
fct.run_factor()