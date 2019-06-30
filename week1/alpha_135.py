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
        self.neutral = False                                           ###是否需要中性化
        self.factorName = __name__.split('.')[-1]
        self.needFields = [
                        t.CLOSE, t.ADJFCT,t.OPEN,t.VOLUME,t.HIGH]  ###设置需要的字段

    def factor_definition(self):                                          ###
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjOpen = needData[t.Open] * needData[t.ADJFCT]
        adjVolume = needData[t.VOLUME] * needData[t.ADJFCT]
        preClose = self.calculator.Delay(x=adjClose, num=1)
        distrib=self.calculator.Rank(adjClose/self.calculator.Delay(adjClose,19),1)
        factor = self.calculator.Sma(distrib,12,1)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()

fct = Factor()
fct.run_factor()
