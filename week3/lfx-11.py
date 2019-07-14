#DECAYLINEAR(RANK(-((OPEN<DELAY(OPEN,4)?(OPEN-DELAY(OPEN,4))/DELAY(OPEN,4):(OPEN =DELAY(OPEN,4)?0:( OPEN -DELAY(OPEN,4))/ OPEN))),2)
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
        self.needFields = [t.OPEN]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjOpen = needData[t.OPEN]
        delayOpen=self.calculator.Delay(adjOpen,4)
        distrib=adjOpen-delayOpen
        factor = self.calculator.Rank(-((distrib<0)*(distrib/delayOpen) + (distrib==0)*0 + (distrib>0)*(distrib/adjOpen)))
        factor = self.calculator.Decaylinear(factor,2) #4

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()
