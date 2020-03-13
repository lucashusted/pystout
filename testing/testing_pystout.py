# Testing pystout
import statsmodels.api as sm
import linearmodels as ln
from pystout import pystout

dta = sm.datasets.webuse('auto')
dta.loc[:,'const'] = 1

y = dta.price

# =============================================================================
# First three models are from statsmodels
# =============================================================================
X = dta[['const','mpg','displacement']]
model1 = sm.OLS(y,X).fit()

X = dta[['const','mpg','displacement','turn']]
model2 = sm.OLS(y,X).fit()

X = dta[['displacement','const','turn']]
model3 = sm.OLS(y,X).fit()

# =============================================================================
# Next 2 are an ols and a tsls from linearmodels
# =============================================================================
X = dta[['displacement','const','turn','gear_ratio']]
model4 = ln.OLS(y,X).fit()

model5 = ln.IV2SLS(dependent=dta.price,endog=dta.mpg,
                   exog=dta.filter(['const','turn','displacement']),
                   instruments=dta.length).fit()

# =============================================================================
# Print result
# =============================================================================
pystout(models=[model1,model2,model3,model4,model5],
        file='test_table.tex',
        addnotes=['Here is a little note','And another one'],
        digits=2,
        endog_names=['Custom','Header','Please','Thanks','Again'],
        varlabels={'const':'Constant','displacement':'Disp','mpg':'MPG'},
        addrows={'Test':['A','Test','Row','Here','Too']},
        mgroups={'Statsmodels':[1,3],'L OLS':4,'L TSLS':5},
        modstat={'nobs':'Obs','rsquared_adj':'Adj. R\sym{2}','fvalue':'F-stat'}
        )
