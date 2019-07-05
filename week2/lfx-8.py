# DECAYLINEAR((CLOSE>DECAYLINEAR(CLOSE,4)?TRADES_COUNT:(CLOSE<DECAYLINEAR(CLOSE,4)? -TRADES_COUNT:0)),8)
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
        self.needFields = [t.CLOSE,t.ADJFCT,t.TURN,t.TRADES_COUNT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjClose = needData[t.CLOSE]* needData[t.ADJFCT]
        adjTrades_count = needData[t.TRADES_COUNT]* needData[t.ADJFCT]
        weightClose = self.calculator.Decaylinear(adjClose, 4)  # decaylinear加权求和

        distrib=(adjClose>weightClose)*(adjTrades_count)+(adjClose<weightClose)*(-adjTrades_count)+(adjClose==weightClose)*0
        factor = self.calculator.Rank(self.calculator.Decaylinear(distrib,8))

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()

fct = Factor()
fct.run_factor()