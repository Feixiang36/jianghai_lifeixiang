#CORR(((CLOSE-MEAN(LOW,30))/(MEAN(HIGH,30)-MEAN(LOW,30))),TRADES_COUNT,4)
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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.VOLUME, t.VWAP ,t.TURN,t.TRADES_COUNT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据


        adjLow = needData[t.LOW]
        adjHigh = needData[t.HIGH]
        adjClose = needData[t.CLOSE]
        adjVolume = needData[t.TRADES_COUNT]

        distrib11 = adjClose - self.calculator.Mean(adjLow,30)
        distrib12=self.calculator.Mean(adjHigh,30)-self.calculator.Mean(adjLow,30)
        distrib1=distrib11/distrib12
        distrib2=adjVolume
        factor = self.calculator.Corr(distrib1,distrib2,4)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()

fct = Factor()
fct.run_factor()