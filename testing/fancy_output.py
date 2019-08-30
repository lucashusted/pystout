#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:13:34 2019

@author: whiskey
"""

import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col

p = sm.datasets.statecrime.load_pandas().data

p['const'] = 1

reg0 = sm.OLS(p['murder'],p[['const','poverty']]).fit()
reg1 = sm.OLS(p['murder'],p[['const','poverty','urban']]).fit()
reg2 = sm.OLS(p['murder'],p[['const','poverty','urban','white']]).fit()

print(summary_col([reg0,reg1,reg2],stars=True,float_format='%0.2f',
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared),
                             '$R^{2}$ Adj.':lambda x: "{:.2f}".format(x.rsquared_adj)}))

tbl = summary_col([reg0],stars=True,float_format='%0.2f',
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared),
                             'R2 Adj.':lambda x: "{:.2f}".format(x.rsquared_adj)}).as_latex()
f = open('temp.tex','w')
f.write(tbl)
f.close()
