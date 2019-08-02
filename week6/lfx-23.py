#DECAYLINEAR(RANK((((LOG(HIGH/LOW)-SUM(LOG(HIGH/LOW),20))/SUM(LOG(HIGH/LOW),20)))),5)
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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE,t.VWAP,t.OPEN]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjHigh = np.log(needData[t.HIGH])
        adjLow = np.log(needData[t.LOW])

        distrib1= adjHigh-adjLow
        distrib2 = self.calculator.Sum(distrib1,5) #20
        factor=self.calculator.Decaylinear(self.calculator.Rank((distrib1-distrib2)/distrib2),3) #100

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()