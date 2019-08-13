#DECAYLINEAR(MAX(0,LOG(HIGH)-DELAY(LOG(CLOSE),1)),4)-DECAYLINEAR(MAX(0,DELAY(LOG(CLOSE),1)-LOG(LOW)),4)
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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.OPEN,t.VWAP,t.ADJFCT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjLow = np.log(needData[t.LOW] * needData[t.ADJFCT])
        adjHigh = np.log(needData[t.HIGH] * needData[t.ADJFCT])
        adjClose = np.log(needData[t.CLOSE] * needData[t.ADJFCT])

        distrib1= self.calculator.Delay(adjClose,1)
        distrib2=adjHigh-distrib1
        distrib3=(distrib2>0)*distrib2
        distrib4=self.calculator.Decaylinear(distrib3,4)
        distrib5=distrib1-adjLow
        distrib6=(distrib5>0)*distrib5
        distrib7=self.calculator.Decaylinear(distrib6,4)
        factor = distrib4-distrib7

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()