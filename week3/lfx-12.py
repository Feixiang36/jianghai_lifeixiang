#DECAYLINEAR(-(RANK(CORR(SUM(((CLOSE*0.25)+(VWAP*0.75)),22),SUM(MEAN(VOLUME,40),22),6))+RANK(CORR(VWAP,VOLUME,6)))*(CLOSE>MEAN(CLOSE,3),3)
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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.ADJFCT, t.TRDSTAT,t.VWAP,t.VOLUME,t.OPEN]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjClose = needData[t.CLOSE]
        adjVwap = needData[t.VWAP]
        adjVolume = needData[t.VOLUME]

        distrib0=0.25*adjClose+0.75*adjVwap
        distrib11=self.calculator.Sum(distrib0,22)
        distrib12=self.calculator.Sum(self.calculator.Mean(adjVolume,40),22)
        distrib1=self.calculator.Corr(distrib11,distrib12,6)

        distrib2 = self.calculator.Corr(adjVwap, adjVolume, 6)
        distrib= -(self.calculator.Rank(distrib1)+self.calculator.Rank(distrib2))*(adjClose>self.calculator.Mean(adjClose,3))
        factor=self.calculator.Decaylinear(distrib,3)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()
