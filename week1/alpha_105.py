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
        self.neutral = True                                          ###是否需要中性化
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.ADJFCT,t.VOLUME,t.HIGH,t.LOW,t.CLOSE]  ###设置需要的字段

    def factor_definition(self):                                          ###
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        #adjOpen = needData[t.OPEN] * needData[t.ADJFCT]
        adjVolume = needData[t.VOLUME] * needData[t.ADJFCT]
        #adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        #adjLow = needData[t.LOW] * needData[t.ADJFCT]
        factor=-1*(self.calculator.Corr(np.log(adjHigh)*adjHigh,np.log(adjVolume)*adjVolume,13))

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()

fct = Factor()
fct.run_factor()
