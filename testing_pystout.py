# Testing pystout
import statsmodels.api as sm
import pandas as pd
import pystout
from pystout import pystout

dta = sm.datasets.webuse('auto')

X = sm.add_constant(dta[['mpg','displacement']])

y = dta.price
model1 = sm.OLS(y,X).fit()

X = sm.add_constant(dta[['mpg','displacement','turn']])
model2 = sm.OLS(y,X).fit()

X = sm.add_constant(dta[['displacement','turn']])
model3 = sm.OLS(y,X).fit()


pystout(models=[model1,model2,model3],
        file='testing/test_table.tex',
        addnotes=['Here is a little note'],
        digits=2,
        endog_names=['Custom','Header','Please'],
        varlabels={'const':'Constant','displacement':'Disp','mpg':'MPG'}
        )
