# Testing pystout
import statsmodels.api as sm
import pystout
from pystout import pystout

dta = sm.datasets.webuse('auto')
dta.loc[:,'const'] = 1

X = dta[['const','mpg','displacement']]

y = dta.price
model1 = sm.OLS(y,X).fit()

X = dta[['const','mpg','displacement','turn']]
model2 = sm.OLS(y,X).fit()

X = dta[['displacement','const','turn']]
model3 = sm.OLS(y,X).fit()


pystout(models=[model1,model2,model3],
        file='testing/test_table.tex',
        addnotes=['Here is a little note','And another one'],
        digits=2,
        endog_names=['Custom','Header','Please'],
        varlabels={'const':'Constant','displacement':'Disp','mpg':'MPG'},
        addrows={'Test':['A','Test','Row']},
        mgroups={'Group 1':1,'Group 2':[2,3]},
        modstat={'nobs':'Obs','rsquared_adj':'Adj. R\sym{2}'}
        )
